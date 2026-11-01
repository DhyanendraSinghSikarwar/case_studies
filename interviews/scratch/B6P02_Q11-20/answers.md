### Q11 ⭐⭐⭐ 🟡 Weekly forecast error for an e-commerce demand model rose from a MAPE of 12% to 22% in the Diwali sale weeks, then returned toward 13% the week after. The data science lead asks whether the model has drifted. Explain how you would separate a predictable seasonal or event effect from real drift, and what you would change, if anything, in the model or its monitoring.
**Asked at:** No interview page located; forecast-monitoring practitioner pages (demandplanning.net MAPE and bias, John Galt Solutions, 42signals forecast-drift post) describe bias, structural breaks and MAPE blind spots, so editor-designed; search snippets only, not opened
**Say this first (1 line):** Not yet drift: a 22% error that recurs in the same sale weeks every year and drops back to 13% the week after is a predictable event effect the model was never told about, so I fix the features and the monitoring, not the whole model.

**Clarifying questions:**
- Is the sale a known, calendared event, and did the model have a sale or Diwali feature? Why: if it had none, the miss is a modelling gap and not drift.
- What was the error in the same sale weeks last year (and the year before)? Why: the right baseline for a sale week is a sale week, not an ordinary week.
- Is the error signed (under-forecast) or both ways? Why: a consistent under-forecast points at an unmodelled uplift; two-sided error points at noise or a broken feature.
- Is the error concentrated in a few categories or in the promo-heavy ones? Why: it tells me whether to add a category-level uplift or fix a pipeline for a few items.
- What does the business do with the forecast in sale weeks (stock, staffing)? Why: it decides how much a 22% error costs and whether a manual override is acceptable now.

**Approach:**
1. Say what "drift" would look like: error that stays high after the event, or bias that persists in ordinary weeks. Here error came back to 13%, close to the usual 12%.
2. Compare like with like: this sale versus the same sale weeks in earlier years, same segments. If last year was also about 20%, nothing new happened.
3. Look at signed error (bias) as well as MAPE. A sale lifts demand, so the model under-forecasts; that is one-directional and repeats.
4. Check the weeks around the event: the week before (pull-forward of demand), the sale weeks, the week after (a hangover dip). The "13%" week after matters because a dip after a sale can inflate error in the other direction.
5. Fix the cause: add an event calendar feature (sale intensity, discount depth, ad spend) or a post-hoc uplift multiplier learned from past sale weeks. Test it on the latest sale as a held-out event.
6. Fix monitoring: alert on error versus the event-adjusted expectation, keep a separate "event weeks" panel, and track rolling bias in ordinary weeks as the drift signal.
7. Keep a real-drift trip wire: if ordinary-week bias stays beyond a limit for several weeks, treat it as drift and investigate (see Q24 in this part for a structural break).

**Metrics:**
- MAPE = mean(|actual - forecast| / actual) over SKU-weeks. Weak spot: it blows up on small actuals; also report WAPE = sum(|error|) / sum(actual) next to it.
- Bias = mean((forecast - actual) / actual). Negative means under-forecasting.
- Event-matched ratio = MAPE this sale / MAPE same sale last year. Around 1 means no new problem.
- Guardrails: stock-out rate and overstock rate in the sale weeks; the retrained or adjusted model must not worsen ordinary-week MAPE.

**Risks:**
- Two or three sale weeks a year is a tiny sample. Pool across many SKUs and several years before concluding.
- An uplift learned from one sale can be wrong if this year's discount depth was different. Model the driver, not only a flag.
- Averaging hides the pull-forward and hangover weeks; look week by week.
- Retraining on the sale weeks without an event feature teaches the model that demand is simply high, and it will over-forecast the next normal weeks.

**What the interviewer scores:**
- Strong: separates a recurring, one-directional, short event effect from a persistent shift, and compares like-for-like (same event, last year).
- Strong: looks at signed bias, not only MAPE, and proposes a feature fix plus separate event monitoring.
- Strong: keeps a real-drift trip wire so the fix does not blind the monitor.
- Weak: says "retrain on recent data" or "the model drifted" with no seasonal comparison.
- Weak: treats the 13% the next week as proof that all is well, without checking ordinary-week bias.

**Example:** Illustrative numbers. A normal week has actual 1,000 and forecast 880, MAPE 12.0%. A sale week has actual 1,000 and forecast 780, MAPE 22.0%, signed error -22%. The week after is forecast 870, MAPE 13.0%. In a simulation with 40 SKUs per week, three years of data and a 25% sale uplift that the model does not know about, sale-week MAPE is 18.8%, 19.2% and 20.1% in the three years while ordinary weeks stay near 12%. So this year's 20.1% against last year's 19.2% is no drift signal. After learning the uplift from the first two years (1.25x), year-3 sale-week MAPE falls from 20.1% to 11.0%. A true +15% permanent demand shift looks different: rolling 4-week bias is about -12% in ordinary weeks and does not come back.
- Weak answer: "Error doubled, so retrain the model on the Diwali weeks."
- Strong answer: "Compare with last Diwali, check the sign of the error, add an event feature, and keep a bias monitor for ordinary weeks that would catch real drift."

**Code:**
```python
# Q11: seasonal/event error versus real drift (all numbers illustrative, seeded)
import numpy as np
rng = np.random.default_rng(11)

# Hand-check table: MAPE = |actual - forecast| / actual
for name, a, f, want in [("normal week", 1000, 880, 12.0), ("sale week", 1000, 780, 22.0), ("week after", 1000, 870, 13.0)]:
    m = 100 * abs(a - f) / a
    assert abs(m - want) < 1e-9
    print(f"{name:12} actual={a} forecast={f} MAPE={m:.1f}%  signed error={100*(f-a)/a:+.1f}%")

weeks = np.arange(156)                       # 3 years
event = np.isin(weeks % 52, [42, 43])        # two sale weeks a year
baseline = 1000 * (1 + 0.1 * np.sin(2 * np.pi * weeks / 52))   # known trend+season
S = 40                                       # 40 SKUs per week, error pooled across SKUs
noise = rng.lognormal(0, 0.15, size=(weeks.size, S))
uplift = np.where(event, 1.25, 1.0)          # sale lifts demand 25%
actual = (baseline * uplift)[:, None] * noise
fc_old = np.repeat(baseline[:, None], S, axis=1)                            # model without an event feature

def mape(a, f): return 100 * np.mean(np.abs(a - f) / a)
def bias(a, f): return 100 * np.mean((f - a) / a)

for y in range(3):
    s = slice(52 * y, 52 * (y + 1))
    ev, nev = event[s], ~event[s]
    print(f"year {y+1}: MAPE normal weeks {mape(actual[s][nev], fc_old[s][nev]):.1f}%, "
          f"sale weeks {mape(actual[s][ev], fc_old[s][ev]):.1f}%, bias in sale weeks {bias(actual[s][ev], fc_old[s][ev]):+.1f}%")

# Event-aware fix: learn the uplift from PAST sale weeks only (years 1-2), test on year 3
past = (weeks < 104) & event
learned = np.mean(actual[past] / baseline[past][:, None])
fc_new = (baseline * np.where(event, learned, 1.0))[:, None] * np.ones((1, S))
y3 = slice(104, 156)
ev3 = event[y3]
mo, mn = mape(actual[y3][ev3], fc_old[y3][ev3]), mape(actual[y3][ev3], fc_new[y3][ev3])
print(f"learned sale uplift = {learned:.2f}x; year-3 sale-week MAPE old {mo:.1f}% -> new {mn:.1f}%")
assert 1.15 < learned < 1.35 and mn < mo - 5

# Contrast: real drift = permanent +15% demand level shift from week 130 (not tied to an event)
actual_d = actual.copy()
actual_d[130:] *= 1.15
def rolling_bias(a, f, k=4):
    e = 100 * ((f - a) / a).mean(axis=1)
    return np.array([e[max(0, i - k + 1):i + 1].mean() for i in range(len(e))])
rb = rolling_bias(actual_d, fc_new)
post_event_weeks = [i for i in range(104, 130) if (i - 1) % 52 not in (42, 43) and i % 52 not in (42, 43, 44, 45)]
print(f"rolling 4-wk bias, quiet weeks before shift: mean {np.mean(rb[post_event_weeks]):+.1f}%")
print(f"rolling 4-wk bias, weeks 140-155 after shift: mean {np.mean(rb[140:156]):+.1f}%")
assert abs(np.mean(rb[post_event_weeks])) < 3 and np.mean(rb[140:156]) < -8
# Decision rule: sale-week error compared with same sale weeks last year, normal-week error compared with normal weeks
last_year = mape(actual[52:104][event[52:104]], fc_old[52:104][event[52:104]])
this_year = mape(actual[104:156][event[104:156]], fc_old[104:156][event[104:156]])
print(f"same-event comparison, old model: last year {last_year:.1f}% vs this year {this_year:.1f}% -> "
      f"{'no drift signal' if abs(this_year-last_year) < 6 else 'investigate'}")
assert abs(this_year - last_year) < 6
```

**Output (my run):**
```text
normal week  actual=1000 forecast=880 MAPE=12.0%  signed error=-12.0%
sale week    actual=1000 forecast=780 MAPE=22.0%  signed error=-22.0%
week after   actual=1000 forecast=870 MAPE=13.0%  signed error=-13.0%
year 1: MAPE normal weeks 12.0%, sale weeks 18.8%, bias in sale weeks -18.1%
year 2: MAPE normal weeks 11.9%, sale weeks 19.2%, bias in sale weeks -18.4%
year 3: MAPE normal weeks 12.3%, sale weeks 20.1%, bias in sale weeks -18.9%
learned sale uplift = 1.25x; year-3 sale-week MAPE old 20.1% -> new 11.0%
rolling 4-wk bias, quiet weeks before shift: mean +1.0%
rolling 4-wk bias, weeks 140-155 after shift: mean -12.4%
same-event comparison, old model: last year 19.2% vs this year 20.1% -> no drift signal
```

**Follow-ups:**
- What if last year's sale error was only 14%? Then this year is worse than the same event a year ago and I look at discount depth, new categories and competitor activity before blaming the model.
- How would you model the sale? An event calendar with discount depth and ad spend as regressors, or a multiplicative uplift on a baseline forecast; see Book 1 Part 6, Q13 ("How do you model holidays, promotions and other external regressors").
- Which metric next to MAPE? WAPE and bias; Book 1 Part 6, Q11 ("Which forecast metric would you choose (MAE, RMSE, MAPE, sMAPE, MASE, WAPE) and why?") covers the trade-offs.

**Common mistakes:** Comparing a sale week with an ordinary week. Looking at MAPE only and missing the sign. Retraining on the event weeks with no event feature. Removing the sale weeks from monitoring altogether, so real drift in them is never seen.

### Q12 ⭐⭐⭐ 🟡 Alerts show the population stability index (PSI) is above 0.25 for the age and city features, yet the model's labelled AUC is unchanged this month. A stakeholder wants an immediate retrain. Explain what the alert does and does not prove, which type of shift (covariate, prior, concept) you suspect, and how you would decide whether to act.
**Asked at:** Drift and monitoring-without-labels guides (techinterview.org MLOps guides, a DataDome write-up on monitoring models without labels, KodeKloud and NannyML-style material); commonly reported in public guides for MLOps and ML-system-design loops; search snippets only, not opened
**Say this first (1 line):** PSI above 0.25 proves the inputs moved, not that the model got worse; with AUC unchanged I suspect covariate shift the model handles fine, I check whether it matters, and I do not retrain on an alert alone.

**Clarifying questions:**
- Are the labels in "AUC unchanged" matured, and how many are there? Why: a small or immature sample could hide a real fall.
- What are the age and city features' importance in the model? Why: a big shift in an unimportant feature changes little.
- Did anything change upstream (a new acquisition channel, a new city launch, a binning change)? Why: a pipeline change makes PSI jump without any real population change.
- How was PSI computed (bins from the training data, number of bins, treatment of empty bins)? Why: bad bins create false alarms; see Book 4 Part 8, Q3 ("Population Stability Index from scratch").
- Does the business care about performance in the new mix (new cities, older users) specifically? Why: overall AUC can be unchanged while one slice is worse.

**Approach:**
1. Confirm the alert is real: same bins, no schema or encoding change, enough rows.
2. Decide the shift type. Inputs moved and the model's score distribution is stable: covariate shift. Positive rate moved: prior shift. Same inputs, different outcomes: concept drift. PSI alone only sees the first.
3. Check what the model does with the shifted features: feature importance, and PSI of the model score (the thing the business sees).
4. Estimate performance in the new mix without waiting: reweight the old validation set to the new age and city mix and recompute AUC. If the reweighted AUC matches the observed AUC, the model is robust to this shift.
5. Slice the labelled data by the shifted groups (new cities, older ages) and check calibration and AUC per slice.
6. Act on evidence: if slices and calibration are fine, document and tighten the alert; if a slice is worse, retrain with more of that population or add regional features; always keep the alert on a watch list.
7. Pair PSI with a performance monitor on matured labels, since input drift cannot see concept drift.

**Metrics:**
- PSI = sum over bins of (actual share - expected share) x ln(actual share / expected share), with reference bins from training quantiles. Common rule of thumb: below 0.10 small, 0.10 to 0.25 moderate, above 0.25 large; these cut-offs are conventions, not laws.
- Labelled AUC and calibration (observed versus predicted rate) overall and per shifted slice.
- Reweighted-reference AUC, as the expected AUC under the new mix.
- Guardrail: score-distribution PSI and positive rate.

**Risks:**
- PSI depends on bin count and sample size; a large n makes small shifts look alarming.
- Unchanged AUC can hide a calibration change or a worse slice.
- Reweighting only fixes shift in the variables you reweight on; hidden variables stay hidden.
- Retraining on a few weeks of the new mix can throw away useful older data.

**What the interviewer scores:**
- Strong: states that PSI measures input movement only, names covariate shift, and uses the score distribution and labelled slices to judge impact.
- Strong: has a decision rule and a way to estimate the effect of the shift (reweighting) before acting.
- Strong: says what would change the decision (a slice that is worse, calibration decay, an importance-heavy feature).
- Weak: "PSI above 0.25 means retrain", or "AUC is the same so ignore it forever".

**Example:** Illustrative numbers. Expected bin shares 50%, 30%, 20% against actual 30%, 30%, 40%: PSI = (0.3 - 0.5) ln(0.3/0.5) + 0 + (0.4 - 0.2) ln(0.4/0.2) = 0.1022 + 0.1386 = 0.2408, a moderate shift, just under the usual 0.25 line. In the simulation the mean age moves from 35 to 42 and the city mix moves toward tier 3, giving PSI about 0.70 for age and about 0.55 for city, while the score PSI is 0.004 and AUC stays at 0.824 in both periods. Reweighting the old data to the new mix predicts AUC 0.826 against 0.824 observed, so no retrain is needed. The contrast case has PSI near 0 for age but AUC 0.697, because the relationship changed: PSI would never have caught it.
- Weak answer: "PSI is 0.25, so retrain now."
- Strong answer: "The inputs moved, the score and AUC did not; I will reweight to the new mix, check slices and calibration, and retrain only if a slice shows harm."

**Code:**
```python
# Q12: PSI alert with unchanged AUC (illustrative simulation, seeded, numpy+scipy only)
import numpy as np
from scipy.stats import rankdata
rng = np.random.default_rng(12)

def auc(y, s):
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)

def psi(ref, cur, edges):
    e = np.histogram(ref, edges)[0] / len(ref)
    a = np.histogram(cur, edges)[0] / len(cur)
    e = np.clip(e, 1e-4, None); a = np.clip(a, 1e-4, None)
    return float(np.sum((a - e) * np.log(a / e)))

# PSI by hand on 3 bins: expected 50/30/20, actual 30/30/40
exp, act = np.array([.5, .3, .2]), np.array([.3, .3, .4])
hand = float(np.sum((act - exp) * np.log(act / exp)))
print(f"hand-check PSI = {hand:.4f}")
assert abs(hand - (-0.2*np.log(.6) + 0.2*np.log(2))) < 1e-12 and 0.10 < hand < 0.25

# Fixed "model": score driven by x1, x2 (strong) and weakly by age and city tier
def make(n, age_mean, tier_p):
    age = rng.normal(age_mean, 8, n)
    tier = rng.choice([1, 2, 3], n, p=tier_p)
    x1, x2 = rng.normal(size=n), rng.normal(size=n)
    logit = -1.0 + 1.3 * x1 + 0.9 * x2 + 0.01 * (age - 35) + 0.05 * (tier - 2)
    y = (rng.random(n) < 1 / (1 + np.exp(-logit))).astype(int)
    return age, tier, x1, x2, y
def score(age, tier, x1, x2):
    return -1.0 + 1.3 * x1 + 0.9 * x2 + 0.01 * (age - 35) + 0.05 * (tier - 2)

ref = make(60000, 35, [.5, .3, .2])
cur = make(60000, 42, [.2, .3, .5])          # older users, more tier-3 cities, same relationship
age_edges = np.quantile(ref[0], np.linspace(0, 1, 11)); age_edges[0], age_edges[-1] = -1e9, 1e9
p_age = psi(ref[0], cur[0], age_edges)
p_city = psi(ref[1], cur[1], np.array([0.5, 1.5, 2.5, 3.5]))
s_ref, s_cur = score(*ref[:4]), score(*cur[:4])
sc_edges = np.quantile(s_ref, np.linspace(0, 1, 11)); sc_edges[0], sc_edges[-1] = -1e9, 1e9
p_score = psi(s_ref, s_cur, sc_edges)
a_ref, a_cur = auc(ref[4], s_ref), auc(cur[4], s_cur)
print(f"PSI age={p_age:.3f} city={p_city:.3f} score={p_score:.3f}")
print(f"AUC reference={a_ref:.3f} current={a_cur:.3f}")
assert p_age > 0.25 and p_city > 0.25 and abs(a_ref - a_cur) < 0.01

# Does the shift matter? Reweight the reference to the NEW age/tier mix and recompute expected AUC
age_bin = lambda a: np.digitize(a, np.quantile(ref[0], np.linspace(0, 1, 11))[1:-1])
cell = lambda a, t: age_bin(a) * 3 + (t - 1)
c_ref, c_cur = cell(ref[0], ref[1]), cell(cur[0], cur[1])
w_cell = np.bincount(c_cur, minlength=30) / len(c_cur) / (np.bincount(c_ref, minlength=30) / len(c_ref))
w = w_cell[c_ref]
def wauc(y, s, w):
    o = np.argsort(s); y, s, w = y[o], s[o], w[o]
    wp, wn = w * (y == 1), w * (y == 0)
    cn = np.cumsum(wn) - wn
    return float(np.sum(wp * cn) / (wp.sum() * wn.sum()))
a_rw = wauc(ref[4], s_ref, w)
print(f"reweighted-reference AUC (expected under new mix) = {a_rw:.3f}; observed current = {a_cur:.3f}")
assert abs(a_rw - a_cur) < 0.01

# Contrast: concept drift with NO input shift (PSI ~ 0) but AUC falls
x1c, x2c = rng.normal(size=60000), rng.normal(size=60000)
agec, tierc = rng.normal(35, 8, 60000), rng.choice([1, 2, 3], 60000, p=[.5, .3, .2])
lg = -1.0 + 0.4 * x1c + 0.9 * x2c                 # x1 matters much less now
yc = (rng.random(60000) < 1 / (1 + np.exp(-lg))).astype(int)
sc = score(agec, tierc, x1c, x2c)
print(f"concept drift contrast: PSI age={psi(ref[0], agec, age_edges):.3f}, AUC={auc(yc, sc):.3f}")
assert psi(ref[0], agec, age_edges) < 0.02 and auc(yc, sc) < a_ref - 0.03
```

**Output (my run):**
```text
hand-check PSI = 0.2408
PSI age=0.699 city=0.547 score=0.004
AUC reference=0.824 current=0.824
reweighted-reference AUC (expected under new mix) = 0.826; observed current = 0.824
concept drift contrast: PSI age=0.000, AUC=0.697
```

**Follow-ups:**
- Which shift would hurt AUC most? Concept drift, because the learned relationship is wrong; covariate shift only hurts if the model extrapolates or the shifted region is where it is weak. Book 4 Part 8, Q9 ("Detecting concept drift") covers detection.
- Why not use a statistical test instead of PSI? With large n a test flags tiny, harmless shifts; an effect-size measure such as PSI plus a performance check is more useful.
- Could the alert be a data bug? Yes, check the pipeline first; Q20 in this part shows a silent default value that looks like drift.

**Common mistakes:** Retraining on every alert. Setting 0.25 as a law. Ignoring calibration and slices. Computing PSI with bins fitted on the current data. Forgetting that PSI cannot see concept drift.

### Q13 ⭐⭐⭐ 🔴 A loan-approval model was trained on past decisions and now only approved applicants ever produce repayment outcomes, so its own monitoring shows excellent default prediction on approved loans while losses on a new borrower segment rise. Explain how this feedback loop biases both retraining and monitoring, and what exploration, holdout or reject-inference options you would consider and their costs.
**Asked at:** Recommender feedback-loop and popularity-bias literature (Mansoury et al. 'Feedback Loop and Bias Amplification in Recommender Systems', a popularity-bias survey on arXiv) plus a Prachub ranking-debugging page; no public interview page for this exact prompt, so editor-designed from the literature; search snippets only, not opened
**Say this first (1 line):** The model only ever sees outcomes for loans it approved, so both retraining and monitoring are blind to the people it rejects and to extrapolation beyond the approved range; I would pay for a small, controlled slice of real outcomes there.

**Clarifying questions:**
- How were past approvals decided (a model, rules, officer judgement), and is the cut-off known? Why: if the approval rule is known, selection is modelled; if officers used extra information, it is hidden.
- What is the new borrower segment (thin-file, new city, new channel) and what share of applications is it? Why: it tells me how far outside the old approved range we are.
- Do we have any outcomes on rejected or withdrawn applicants (other lenders' data, bureau performance later)? Why: it is the cheapest proxy for reject outcomes.
- Is there a regulatory or risk-appetite limit on deliberately lending to rejected profiles? Why: it limits exploration design and caps cost.
- How long do outcomes take to mature? Why: it sets how long the exploration slice runs before it tells me anything.

**Approach:**
1. Name the bias: selection bias. Outcomes exist only where the old policy said yes, so the training set is a truncated sample, and monitoring on approved loans looks good by construction.
2. Show it with numbers: compare predicted and observed default on the approved book (looks calibrated) with any available information on the low end, such as bureau-later performance or the explored slice.
3. Stop trusting approved-only metrics for the new segment. Track the share of applicants outside the approved feature range, and the losses by segment with cohort age.
4. Collect unbiased data: randomised exploration. Approve a small random slice of applicants just below the cut-off, with caps on loan size and exposure, and track their outcomes. Weight each explored case by the inverse of its selection probability when retraining.
5. Use reject inference only as a supplement: parcelling or augmentation with bureau-later performance helps if its assumptions hold; labelling rejects with the model's own guess adds no new information.
6. Make the policy safer meanwhile: tighten limits or price higher on the new segment, and keep a champion policy with a holdout.
7. Report the cost and the value of the information to risk leadership, and review the slice size every quarter.

**Metrics:**
- Default rate = defaulted loans / loans past the maturity window, by segment and by cohort.
- Calibration gap = observed default rate - mean predicted PD per score band, on explored loans only.
- Exploration cost = defaults in the slice x loan size x loss given default (ignore interest for a worst case).
- Guardrails: share of book in exploration (a small percent), exposure cap per borrower, and loss budget for the slice.

**Risks:**
- Approved-only AUC can be fine because the approved range is narrow; AUC is not the problem here, extrapolation is.
- Exploration costs real money and has fairness and compliance implications; it needs sign-off.
- Naive reject inference with the model's own labels reinforces the model's beliefs.
- A loan-size cap lowers the cost but can change borrower behaviour, so results may not transfer.

**What the interviewer scores:**
- Strong: names selection bias and shows why monitoring on approved loans is blind; separates the effect on retraining from the effect on monitoring.
- Strong: proposes randomised exploration with inverse-probability weights, sizes it, and states the cost honestly.
- Strong: knows reject inference's limits.
- Weak: "just retrain more often" or "add more features".

**Example:** Illustrative numbers. Applicants have a credit-quality score x; the old policy approves x above -0.3 (about 62% of applicants). In the simulation the approved book has 2.7% defaults, the model's mean predicted PD is 2.7% too, and monitoring looks fine. The true default rate among all applicants is 12.5%. In the band x from -2.0 to -1.2 the model predicts 34% but the truth is 51%; in the band below -2.0 it predicts 64% against 91%. A random slice of 1,000 rejected applicants gives a default estimate with a 95% half-width of about 2.8 points at a 30% default rate (the sample's estimate was 26.7% against a true 28.3%). At Rs 1 lakh per loan and 60% loss given default the slice costs about Rs 160 lakh in losses, or about Rs 16 lakh with a Rs 10,000 cap, interest ignored. Refitting with the explored slice weighted by inverse probability brings the predicted PD in the band to 0.48 against a true 0.51; the naive reject-inference refit gives 0.155.
- Weak answer: "Monitoring shows good default prediction, so the model is fine."
- Strong answer: "Monitoring is blind outside the approved range; I would buy a small randomised slice, weight it correctly, and treat that cost as the price of information."

**Code:**
```python
# Q13: selection bias in a loan model (illustrative simulation, seeded, numpy+scipy)
import numpy as np
from scipy.stats import rankdata, norm
rng = np.random.default_rng(13)
sig = lambda z: 1 / (1 + np.exp(-z))

def auc(y, s):
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)

def fit_logit(X, y, it=30):
    X1 = np.c_[np.ones(len(X)), X]; b = np.zeros(X1.shape[1])
    for _ in range(it):
        p = sig(X1 @ b); W = p * (1 - p)
        b += np.linalg.solve(X1.T @ (X1 * W[:, None]) + 1e-9 * np.eye(len(b)), X1.T @ (y - p))
    return b
pred = lambda b, X: sig(np.c_[np.ones(len(X)), X] @ b)

# x = credit-quality score (higher = safer). True default risk rises sharply (non-linearly) at low x.
N = 400_000
x = rng.normal(0, 1, N)
true_logit = -3.0 - 1.5 * x + 0.5 * np.maximum(0, -x - 0.3) ** 2
pd_true = sig(true_logit)
default = (rng.random(N) < pd_true).astype(int)

# Old policy: approve only if x > -0.3 (about 62% approved). Outcomes exist only for approved.
approved = x > -0.3
print(f"approval rate {approved.mean():.3f}; default rate among approved {default[approved].mean():.3f}; "
      f"true default rate among ALL applicants {default.mean():.3f}")
assert default[approved].mean() < default.mean()

b = fit_logit(x[approved, None], default[approved])
p_hat = pred(b, x[:, None])
print(f"approved book: mean predicted PD {p_hat[approved].mean():.3f} vs observed {default[approved].mean():.3f} (looks calibrated)")
assert abs(p_hat[approved].mean() - default[approved].mean()) < 0.01
print(f"AUC on approved (what monitoring sees) = {auc(default[approved], p_hat[approved]):.3f}")
print(f"AUC on the rejected region (unobserved)  = {auc(default[~approved], p_hat[~approved]):.3f}")

# Calibration in the unseen region: x in bins below the cut
edges = [-3.5, -2.0, -1.2, -0.7, -0.3]
print("x-bin            n   mean predicted PD   true PD")
for lo, hi in zip(edges[:-1], edges[1:]):
    m = (x >= lo) & (x < hi)
    print(f"[{lo:5.1f},{hi:5.1f})  {m.sum():6d}   {p_hat[m].mean():.3f}               {default[m].mean():.3f}")
m_low = (x >= -2.0) & (x < -1.2)
assert p_hat[m_low].mean() < default[m_low].mean() - 0.10   # model badly under-predicts in the unseen region

# Option: random-approval exploration slice among would-be rejects
n_target = 1000
half_width = 1.96 * np.sqrt(0.30 * 0.70 / n_target)
print(f"exploration slice of {n_target} loans: 95% half-width on a ~30% default rate = +/-{100*half_width:.1f} points")
assert 0.027 < half_width < 0.030
rejected_idx = np.flatnonzero(~approved)
pick = rng.choice(rejected_idx, n_target, replace=False)
est = default[pick].mean()
print(f"measured default rate in explored slice = {est:.3f} (true default rate among rejects = {default[~approved].mean():.3f})")
loan, lgd = 100_000, 0.6                      # Rs 1 lakh loan, 60% loss given default (illustrative)
cost = default[pick].sum() * loan * lgd
print(f"expected exploration cost (losses only, ignoring interest earned) = Rs {cost/1e5:.1f} lakh")
small = default[pick].sum() * 10_000 * lgd
print(f"same slice with a Rs 10,000 loan cap: Rs {small/1e5:.1f} lakh")
assert abs(small * 10 - cost) < 1e-6
share = n_target / (~approved).sum()
print(f"slice is {100*share:.2f}% of rejected applicants ({(~approved).sum()} rejects)")

# Option: naive reject inference (label every reject with the model's own prediction) just echoes the model
y_aug = np.r_[default[approved], (p_hat[~approved] > 0.5).astype(int)]
X_aug = np.r_[x[approved], x[~approved]][:, None]
b2 = fit_logit(X_aug, y_aug)
low2 = pred(b2, x[:, None])[m_low].mean()
print(f"naive reject-inference refit: mean PD in the unseen bin = {low2:.3f} vs true {default[m_low].mean():.3f}")
assert low2 < default[m_low].mean() - 0.05    # still under-predicts: it learned nothing new
# Option: refit using explored slice (inverse-probability weight each explored reject)
w_each = (~approved).sum() / n_target
Xe = np.r_[x[approved], x[pick]][:, None]; ye = np.r_[default[approved], default[pick]]
we = np.r_[np.ones(approved.sum()), np.full(n_target, w_each)]
# weighted Newton
X1 = np.c_[np.ones(len(Xe)), Xe]; b3 = np.zeros(2)
for _ in range(40):
    p = sig(X1 @ b3); W = we * p * (1 - p)
    b3 += np.linalg.solve(X1.T @ (X1 * W[:, None]) + 1e-9 * np.eye(2), X1.T @ (we * (ye - p)))
low3 = pred(b3, x[:, None])[m_low].mean()
print(f"refit with weighted exploration slice: mean PD in the unseen bin = {low3:.3f} vs true {default[m_low].mean():.3f}")
assert abs(low3 - default[m_low].mean()) < abs(low2 - default[m_low].mean())
```

**Output (my run):**
```text
approval rate 0.619; default rate among approved 0.027; true default rate among ALL applicants 0.125
approved book: mean predicted PD 0.027 vs observed 0.027 (looks calibrated)
AUC on approved (what monitoring sees) = 0.709
AUC on the rejected region (unobserved)  = 0.798
x-bin            n   mean predicted PD   true PD
[ -3.5, -2.0)    9058   0.639               0.905
[ -2.0, -1.2)   37146   0.341               0.511
[ -1.2, -0.7)   50684   0.173               0.203
[ -0.7, -0.3)   55440   0.097               0.099
exploration slice of 1000 loans: 95% half-width on a ~30% default rate = +/-2.8 points
measured default rate in explored slice = 0.267 (true default rate among rejects = 0.283)
expected exploration cost (losses only, ignoring interest earned) = Rs 160.2 lakh
same slice with a Rs 10,000 loan cap: Rs 16.0 lakh
slice is 0.66% of rejected applicants (152434 rejects)
naive reject-inference refit: mean PD in the unseen bin = 0.155 vs true 0.511
refit with weighted exploration slice: mean PD in the unseen bin = 0.481 vs true 0.511
```

**Follow-ups:**
- How large should the slice be? Enough for the confidence width you need in the riskiest band; 1,000 loans give about +/-2.8 points at a 30% default rate, and the loan cap and exposure limits set the affordable upper bound.
- Is there a free alternative? Bureau performance of rejected applicants who borrowed elsewhere, or a policy that randomly relaxes the cut-off only for small loans.
- Does the same loop exist elsewhere? Yes, recommenders and moderation (see Q21 and Q38 in this part).

**Common mistakes:** Calling approved-only AUC proof of health. Labelling rejects with the model's own output. Exploring without weights, then training as if the sample were random. Ignoring regulators and fairness. Hiding the exploration cost from finance.

### Q14 ⭐⭐⭐ 🔴 A binary classifier's ranking quality is fine (AUC stable at 0.82), but predicted probabilities average 0.10 while the observed positive rate on matured data is 0.14, and a fixed 0.5 decision threshold now misses many positives. Explain how you would diagnose calibration decay, choose between recalibration, threshold change and retraining, and how often you would re-check it.
**Asked at:** Calibration, prior-shift and threshold-review material (an arXiv paper on calibrating metrics under class-prior change, a futureagi model-versus-data-drift post, a fraud-score vendor page on reviewing thresholds); no interview page for the exact scenario, so editor-designed; search snippets only, not opened
**Say this first (1 line):** Ranking is fine, probabilities are not: the model now under-predicts by a factor of 1.4, so I recalibrate on matured data first, fix the threshold from costs or capacity, and only retrain if ranking or a slice has gone bad.

**Clarifying questions:**
- How were the 0.5 threshold and the model's probabilities used (a decision, a ranking, a bid)? Why: a ranking use is unaffected, a decision or a price use is hit.
- Why did the base rate move from 10% to 14% (seasonality, a new population, a labelling change)? Why: prior shift is fixed by a shift in the intercept; changed relationships need retraining.
- How many matured labels per week do we have? Why: it limits how often and how precisely I can recalibrate.
- Is the 0.5 threshold a business choice or a default? Why: with a base rate near 14%, 0.5 is rarely the cost-optimal threshold anyway.
- Are the probabilities consumed downstream (expected loss, bidding)? Why: then calibration matters directly and the fix should be shipped everywhere.

**Approach:**
1. Diagnose on matured data only: mean predicted versus observed (here 0.10 versus 0.14, a ratio of 1.40), a reliability diagram, ECE, and calibration slope and intercept from a logistic fit of outcome on logit(score).
2. Check ranking separately (AUC stable at 0.82) and by slice; if ranking is fine and the miss is mostly intercept, it is prior or base-rate shift.
3. Recalibrate: a Platt (logistic) or isotonic map fitted on a recent matured window, evaluated on a later window. Monotone maps leave AUC unchanged.
4. Re-choose the threshold from a business rule, not from 0.5: a cost ratio (flag if p >= cost of false alarm / (cost of false alarm + cost of miss)) or a review capacity (flag the top k%).
5. Retrain only if the calibration slope moves away from 1, a segment is bad, or AUC falls; recalibration cannot add information.
6. Re-check on a schedule: weekly on matured data with a confidence interval on observed/predicted; alert if the interval excludes 1 by a set margin for several weeks.
7. Log the calibration map version with each score.

**Metrics:**
- Calibration-in-the-large = observed rate / mean predicted probability (here 0.14 / 0.10 = 1.40).
- ECE = sum over bins of (bin share) x |observed rate - mean prediction|, with 10 equal-count bins. Report the bin count: it changes the value.
- Calibration slope and intercept from logistic regression of y on logit(p); slope near 1 and intercept near 0 is ideal.
- Guardrail: AUC and recall at the capacity point must not fall after recalibration (a monotone map keeps AUC exactly).

**Risks:**
- Recalibrating on a short window can chase noise; evaluate on a later window.
- A fit on immature labels is biased (see Q28 in this part).
- Recalibration fixes level, not ranking; if the new population is ordered differently, only retraining helps.
- If the threshold was set by capacity, the calibration change does not alter who is flagged at all.

**What the interviewer scores:**
- Strong: separates discrimination from calibration, quotes the ratio and checks it on matured data, and chooses the fix by what is broken.
- Strong: challenges the fixed 0.5 threshold and derives one from costs or capacity.
- Strong: gives a re-check cadence with statistics (sample size for the interval).
- Weak: "retrain" with no diagnosis, or "AUC is fine so nothing is wrong".

**Example:** Illustrative numbers. Mean prediction 0.10 versus observed 0.14, ratio 1.40, gap 4 points. In a simulation on 200,000 matured rows, ECE is 0.038 before recalibration and 0.002 after (fit on one half, scored on the other), and AUC is 0.8095 both times. At a fixed 0.5 threshold the old scores flag 2.0% of cases with recall 10.3%; recalibrated scores at 0.5 flag 4.2% with recall 18.7%, still low because 0.5 is far above a 14% base rate. A top-10% capacity rule gives recall 36.0%. With a miss costing 5 and a false alarm 1 the threshold is 1/6 = 0.167: on recalibrated scores that flags 28.1% with recall 67.9%, while the same 0.167 on the uncalibrated scores flags 18.4% with recall 53.8%. Re-check size: 0.14 +/- 0.048 (95%) at 200 matured cases does not exclude 0.10, +/- 0.030 at 500 does.
- Weak answer: "AUC is stable, so the model is fine."
- Strong answer: "The base rate moved, so I recalibrate, set the threshold from cost, and monitor observed over predicted with a confidence interval."

**Code:**
```python
# Q14: calibration decay with stable AUC (illustrative, seeded, numpy+scipy)
import numpy as np
from scipy.stats import rankdata
rng = np.random.default_rng(14)
sig = lambda z: 1 / (1 + np.exp(-z))
logit = lambda p: np.log(p / (1 - p))
def auc(y, s):
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)

# Hand-check: ratio and gap
pred_mean, obs = 0.10, 0.14
print(f"observed/predicted = {obs/pred_mean:.2f}, gap = {100*(obs-pred_mean):.0f} points")
assert abs(obs / pred_mean - 1.4) < 1e-12

# Build matured data: the model's logit is offset by -0.46 relative to the truth, ranking untouched
N = 200_000
z = rng.normal(0, 1.0, N)                         # latent signal
y = (rng.random(N) < sig(-2.40 + 1.4 * z)).astype(int)
p_model = sig(-2.86 + 1.4 * z)                    # model under-predicts after drift in base rate
print(f"mean predicted {p_model.mean():.3f}, observed positive rate {y.mean():.3f}, AUC {auc(y, p_model):.3f}")
assert abs(p_model.mean() - 0.10) < 0.01 and abs(y.mean() - 0.14) < 0.01

def ece(y, p, bins=10):
    edges = np.quantile(p, np.linspace(0, 1, bins + 1)); edges[-1] += 1e-9
    idx = np.digitize(p, edges[1:-1]); tot = 0
    for b in range(bins):
        m = idx == b
        tot += m.mean() * abs(y[m].mean() - p[m].mean())
    return tot

# Split matured data: fit fixes on first half, judge on second half
h = N // 2
ytr, ptr, yte, pte = y[:h], p_model[:h], y[h:], p_model[h:]

def fit_platt(y, p, it=30):
    x = logit(p); X = np.c_[np.ones(len(x)), x]; b = np.array([0., 1.])
    for _ in range(it):
        q = sig(X @ b); W = q * (1 - q)
        b += np.linalg.solve(X.T @ (X * W[:, None]), X.T @ (y - q))
    return b
b = fit_platt(ytr, ptr)
p_recal = sig(b[0] + b[1] * logit(pte))
print(f"Platt fit: intercept {b[0]:+.3f}, slope {b[1]:.3f}")
print(f"ECE before {ece(yte, pte):.4f} -> after recalibration {ece(yte, p_recal):.4f}; AUC {auc(yte, pte):.4f} -> {auc(yte, p_recal):.4f}")
assert ece(yte, p_recal) < ece(yte, pte) / 3
assert abs(auc(yte, pte) - auc(yte, p_recal)) < 1e-9      # monotone map leaves AUC unchanged

def prf(y, flag):
    tp = (flag & (y == 1)).sum()
    return tp / max(flag.sum(), 1), tp / y.sum(), flag.mean()
pr, rc, fr = prf(yte, pte >= 0.5)
print(f"fixed 0.5 on old scores: precision {pr:.3f}, recall {rc:.3f}, flagged {fr:.3f}")
pr2, rc2, fr2 = prf(yte, p_recal >= 0.5)
print(f"fixed 0.5 on recalibrated scores: precision {pr2:.3f}, recall {rc2:.3f}, flagged {fr2:.3f}")
# Threshold from a business rule: review capacity = flag the top 10% by score (rank-based, immune to calibration shift)
k = np.quantile(pte, 0.90)
pr3, rc3, fr3 = prf(yte, pte >= k)
print(f"top-10% capacity rule: precision {pr3:.3f}, recall {rc3:.3f}, flagged {fr3:.3f}")
# Cost-based threshold: a missed positive costs 5, a false alarm costs 1 -> flag if p >= 1/6 on CALIBRATED scores
t = 1 / (1 + 5)
pr4, rc4, fr4 = prf(yte, p_recal >= t)
pr5, rc5, fr5 = prf(yte, pte >= t)
print(f"cost threshold p>={t:.3f}: recalibrated flagged {fr4:.3f} recall {rc4:.3f}; uncalibrated flagged {fr5:.3f} recall {rc5:.3f}")
assert rc4 > rc5 and rc2 > rc

# How much matured data per weekly check to see a 1.4x ratio? Standard error of observed rate
for n in (200, 500, 2000):
    se = np.sqrt(0.14 * 0.86 / n)
    print(f"n={n:6d}: observed 0.14 +/- {1.96*se:.4f} (95%), excludes 0.10: {bool(0.14 - 1.96*se > 0.10)}")
assert not (0.14 - 1.96 * np.sqrt(0.14 * 0.86 / 200) > 0.10)
assert 0.14 - 1.96 * np.sqrt(0.14 * 0.86 / 500) > 0.10
```

**Output (my run):**
```text
observed/predicted = 1.40, gap = 4 points
mean predicted 0.100, observed positive rate 0.138, AUC 0.811
Platt fit: intercept +0.453, slope 1.005
ECE before 0.0381 -> after recalibration 0.0023; AUC 0.8095 -> 0.8095
fixed 0.5 on old scores: precision 0.712, recall 0.103, flagged 0.020
fixed 0.5 on recalibrated scores: precision 0.621, recall 0.187, flagged 0.042
top-10% capacity rule: precision 0.498, recall 0.360, flagged 0.100
cost threshold p>=0.167: recalibrated flagged 0.281 recall 0.679; uncalibrated flagged 0.184 recall 0.538
n=   200: observed 0.14 +/- 0.0481 (95%), excludes 0.10: False
n=   500: observed 0.14 +/- 0.0304 (95%), excludes 0.10: True
n=  2000: observed 0.14 +/- 0.0152 (95%), excludes 0.10: True
```

**Follow-ups:**
- Platt or isotonic? Platt has two parameters and is stable with little data; isotonic is flexible but needs thousands of matured labels and can create ties. Book 1 Part 3, Q14 ("What is model calibration and why can a model with great AUC still be badly calibrated?") has the background.
- How do you derive the cost threshold? Book 1 Part 3, Q41 ("Derive the Bayes-optimal threshold for a given cost matrix and explain why it needs calibrated probabilities.").
- What if only the base rate moved? Adjust the intercept by the log-odds change (prior-shift correction); Q41 in this part uses a related label-shift estimate.

**Common mistakes:** Retraining to fix a pure level shift. Fitting and scoring the recalibration on the same rows. Keeping 0.5 out of habit. Calibrating on immature labels. Forgetting that capacity-based thresholds ignore calibration.

### Q15 ⭐⭐⭐ 🔴 You have a retrained model that looks 1.2% better on a recent offline test set, and it will affect revenue-critical decisions. Explain how you would validate it through shadow mode, a canary and an A/B test, what each stage can and cannot show, which guardrails would trigger an automatic rollback, and how label delay changes the plan.
**Asked at:** Safe-rollout and shadow/canary guides (Qwak shadow-versus-canary post, Atlan shadow-deployment page, a NerdLevelTech MLOps-interview deployment-strategies lesson, a datainterview.com safe-rollout drill); commonly reported in public MLOps guides; search snippets only, not opened
**Say this first (1 line):** An offline gain of 1.2% is a reason to test, not to ship: I would run shadow, then a small canary, then a proper A/B test, and each stage answers a different question, with automatic rollback on guardrails and proxy metrics while labels are late.

**Clarifying questions:**
- What does "1.2% better" mean: which metric, absolute or relative, and with what confidence interval? Why: the prompt does not say, and a 1.2% relative change in AUC is not a 1.2% change in revenue.
- Does the model's decision change what outcomes we observe (approvals, blocks)? Why: if yes, an offline set is already biased and only an online test is trustworthy.
- How late are labels, and what proxies exist? Why: label delay decides which guardrails can act in hours and which only after weeks.
- What is the traffic per day and the baseline rate of the key metric? Why: it sets how long the A/B test must run for a 1.2% effect.
- What is the cost of a wrong decision and who can approve a rollback? Why: it sets guardrail thresholds and ownership.

**Approach:**
1. Offline check first: paired bootstrap confidence interval for the difference on the same rows; is the 1.2% beyond noise, and does it hold in time-split and segment views?
2. Shadow mode: the new model scores live traffic, its output is logged and not used. This tests latency, errors, feature availability, score distribution and how many decisions would differ from the champion. It cannot show outcomes, because the new model's decisions were never acted on.
3. Canary: send a small share (say 5%) to the new model, ramp on schedule. It shows breakage (error rate, latency, approval or flag rate shifts) quickly; it is too small to see a 1.2% outcome gain.
4. A/B test: random split of users or requests, run to the planned sample size on the primary outcome, with guardrails. It is the only stage that can show a causal revenue effect.
5. Automatic rollback guardrails: error rate and p99 latency over a limit, flag or approval rate outside a band versus champion, score distribution PSI over a limit, and a loss or complaint proxy over a limit for a sustained window.
6. Label delay: use proxies in the first weeks (approval rate, early-payment or early-dispute signals), keep the A/B read at label maturity, and keep the champion as an instant fallback.
7. Decide with a pre-written rule: ship, hold or roll back, based on the confidence interval and the guardrails, not on a single week.

**Metrics:**
- Primary: revenue (or loss) per decision, with the A/B difference and its 95% confidence interval.
- Offline: paired bootstrap interval for the difference in AUC on the same rows.
- Shadow: decision disagreement rate = decisions that differ / requests; latency p99; feature-missing rate.
- Canary guardrails: error rate, p99 latency, approval or flag rate relative to champion.
- Sample size per arm for a conversion test: n = 2 (z_alpha/2 + z_power)^2 p (1 - p) / delta^2 (pooled approximation).

**Risks:**
- Offline sets are historical and can hide drift and selection effects.
- A canary that is too small gives false reassurance about small effects.
- Peeking at the A/B early inflates false positives (see Book 1 Part 10, Q7).
- Interference between buckets and novelty effects (Q47 in this part).
- Rollback that needs a deploy is too slow; make it a flag.

**What the interviewer scores:**
- Strong: says what each stage can and cannot show, and does not use the canary as an effectiveness test.
- Strong: computes or reasons about sample size for a small lift and says how long it takes.
- Strong: sets explicit auto-rollback guardrails and proxies for label delay.
- Weak: lists the three stage names with no purpose, or ships on the offline number.

**Example:** Illustrative numbers. Offline AUC goes from 0.8076 to 0.8178, a relative gain of 1.26%; the paired bootstrap 95% interval for the difference is 0.0094 to 0.0109, so the offline gain is not noise on that test set, but it is still historical. For the A/B test take conversion 4.0% and a 1.2% relative lift (0.048 percentage points): about 2.63 million users per arm, which at 100,000 users a day is 53 days and at 500,000 a day is 11 days. A canary of 20,000 decisions can only detect an approval-rate change of about 1.4 points, so it cannot see the 1.2% lift, but it flags a 10% relative drop in approval with probability near 1. In shadow, the top-10% decisions differ on 1.5% of requests.
- Weak answer: "Offline is better by 1.2%, so roll it out."
- Strong answer: "Shadow for safety, canary for breakage, A/B for the effect, with a rollback rule and proxies while labels are late."

**Code:**
```python
# Q15: how much can offline, shadow, canary and A/B each show about a "1.2% better" model? (illustrative, seeded)
import numpy as np
from scipy.stats import rankdata, norm
rng = np.random.default_rng(15)
def auc(y, s):
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)

# (1) Offline: is a 1.2% relative AUC gain (0.800 -> about 0.81) distinguishable from noise on a 30,000-row test set?
n = 30_000
z = rng.normal(size=n)
y = (rng.random(n) < 1 / (1 + np.exp(-(-1.5 + 2.4 * z)))).astype(int)
old = z + rng.normal(0, 0.75, n)                    # old model's score
new = old + 0.10 * (z - old) + rng.normal(0, 0.12, n)   # correlated, slightly better
a_old, a_new = auc(y, old), auc(y, new)
print(f"offline AUC old {a_old:.4f}, new {a_new:.4f}, relative gain {100*(a_new/a_old-1):.2f}%")
diffs = []
for _ in range(300):
    i = rng.integers(0, n, n)
    diffs.append(auc(y[i], new[i]) - auc(y[i], old[i]))
lo, hi = np.percentile(diffs, [2.5, 97.5])
print(f"paired bootstrap 95% CI for AUC difference: [{lo:.4f}, {hi:.4f}]")
assert lo > 0 and a_new > a_old

# (2) Online A/B: sample size to see a 1.2% RELATIVE lift in a 4.0% conversion rate
p0, rel = 0.04, 0.012
p1 = p0 * (1 + rel); d = p1 - p0
za, zb = norm.ppf(0.975), norm.ppf(0.80)
n_arm = 2 * (za + zb) ** 2 * (p0 * (1 - p0) + p1 * (1 - p1)) / 2 / d ** 2
print(f"A/B: lift {100*d:.3f} points; users needed per arm = {n_arm:,.0f}")
assert 2.5e6 < n_arm < 2.8e6
for per_day in (100_000, 500_000):
    print(f"  at {per_day:,} users/day split 50/50: {np.ceil(n_arm / (per_day / 2)):.0f} days")
assert np.ceil(n_arm / 50_000) > 50

# (3) Canary: 5% of traffic for a day cannot see 1.2% but should catch a breakage. Detect a 10% relative drop in approval?
base = 0.60                       # approval rate of the old model (illustrative)
n_can = 20_000                    # canary decisions in the first hours
se = np.sqrt(base * (1 - base) / n_can)
mde = (za + zb) * se * np.sqrt(2)
print(f"canary of {n_can:,} decisions: smallest approval-rate change detectable ~ {100*mde:.2f} points (80% power)")
broken = 0.60 * 0.90
power = 1 - norm.cdf((za * np.sqrt(2) * se - (base - broken)) / (np.sqrt(2) * se))
print(f"chance to flag a 10% relative approval drop: {power:.3f}")
assert power > 0.99 and mde > 0.01      # catches breakage, cannot see 1.2% relative of 4% conversion

# (4) Shadow: both models score the same requests; compare decisions. No effect on users, no outcome for the new model's own choices.
thr_old = np.quantile(old, 0.9); thr_new = np.quantile(new, 0.9)
flip = ((old >= thr_old) != (new >= thr_new)).mean()
print(f"shadow: top-10% decisions differ on {100*flip:.2f}% of requests")
# (5) Label delay: with 45-day label delay, outcome metrics for a canary started day 0 are first mature on day 45
print("label delay 45 days: use proxy guardrails (approval rate, score shift, latency) until day 45; outcome A/B read at day 45+window")
```

**Output (my run):**
```text
offline AUC old 0.8076, new 0.8178, relative gain 1.26%
paired bootstrap 95% CI for AUC difference: [0.0094, 0.0109]
A/B: lift 0.048 points; users needed per arm = 2,631,329
  at 100,000 users/day split 50/50: 53 days
  at 500,000 users/day split 50/50: 11 days
canary of 20,000 decisions: smallest approval-rate change detectable ~ 1.37 points (80% power)
chance to flag a 10% relative approval drop: 1.000
shadow: top-10% decisions differ on 1.53% of requests
label delay 45 days: use proxy guardrails (approval rate, score shift, latency) until day 45; outcome A/B read at day 45+window
```

**Follow-ups:**
- How long is the A/B test with a 45-day label delay? The outcome read comes after the label window; I would run on a proxy that matures early, and confirm on the real outcome later, with the champion kept as a holdout.
- What if the A/B is too long to be practical? Variance reduction (CUPED), a larger effect target, or accept a non-inferiority test for a refresh. Book 4 Part 6, Q13 ("Safe rollout of a new model: shadow, canary, A/B test and blue-green.") covers the mechanics.
- Sample size inputs? Book 1 Part 10, Q5 ("How do you decide how long to run an experiment and how many users you need?") covers them.

**Common mistakes:** Treating the canary as proof of improvement. Skipping shadow and finding feature or latency bugs in production. Using offline accuracy as the decision metric. Rollback criteria written after seeing the data. Forgetting that label delay delays the real readout.

### Q16 ⭐⭐⭐ 🔴 You discover a feature has been computed incorrectly for three weeks, so about 600,000 predictions made in that time may be wrong, and the logged feature values were also used to build this month's training data. Explain how you would contain the damage, decide which past decisions to re-score or revisit, and make sure the bug does not leak into the next retrain.
**Asked at:** Upstream schema and silent feature-pipeline failure write-ups (Towards AI schema-migration post, RisingWave feature-pipeline observability, ActiveWizards Kafka schema-evolution post, dataexpert.io schema-drift post); practitioner posts rather than interview banks, so scenario is editor-designed; search snippets only, not opened
**Say this first (1 line):** First stop the bleeding by fixing or bypassing the feature, then size the damage by re-scoring with the corrected feature to find which decisions would change, and repair the training data from raw sources before the next retrain.

**Clarifying questions:**
- What exactly is wrong with the feature (a unit, a join, a window, a default) and since which deploy? Why: it sets the exact date range and the correction rule.
- What decisions did the 600,000 predictions drive, and which are reversible (a hold, a limit, a flag) versus final? Why: only some can be revisited.
- Can the raw inputs for the three weeks be recomputed (retained raw tables, event logs)? Why: it decides whether I can repair or must drop rows.
- Which downstream systems consumed the scores (models, reports, finance)? Why: the damage may have spread beyond the first decision.
- Is there a regulatory duty to notify or remediate (credit, insurance)? Why: it changes who must be told and how fast.

**Approach:**
1. Contain: fix the feature or switch the model to a fallback, freeze retrains and any job that reads the logged values, and quarantine the bad training table.
2. Fix the root cause and prove the fix: a unit test with known values, and a comparison of the live feature against a recomputation from raw data on a sample.
3. Bound the damage: define the affected window by logs and deploy time, count affected predictions (600,000 over 21 days is about 28,571 a day) and recompute the feature from raw data for them.
4. Re-score with the corrected feature and find the decisions that flip at the production threshold. Prioritise: flipped decisions, ranked by score change and cost of error, and reversible ones first.
5. Act on the flipped set: reverse or review what can be reversed, report what cannot, and estimate the business effect from flip counts and unit costs.
6. Protect the next retrain: rebuild the training table from raw data with the corrected code (or drop affected rows), add a data version and a date-range exclusion list, and compare candidate models on a clean holdout.
7. Prevent: feature-level checks (range, unit, distribution versus recomputation), a canary comparison of old and new feature code, and a post-incident review.

**Metrics:**
- Flip rate = decisions that change after re-scoring / predictions in the window.
- Wrong-flag count (live yes, true no) and missed count (live no, true yes), valued by unit cost.
- Share of training rows affected = affected rows / training rows (here 21 / 28 = 75%).
- Candidate model AUC on a clean holdout built from raw data; coefficient of the repaired feature against its expected value.
- Guardrail: the repaired table must reproduce the pre-bug features on a control period.

**Risks:**
- Logged feature values are the bug's fingerprints; recomputing from raw only works if raw data was kept.
- Re-scoring with today's model is not what the decision-maker would have done; the right comparison is the model that was live.
- Reversing decisions can harm customers a second time; legal and customer teams must be involved.
- A fix without a regression test lets the bug return.

**What the interviewer scores:**
- Strong: contains first, then sizes damage with a re-score, and prioritises by flips and reversibility.
- Strong: sees the second harm: the corrupted logged values flow into the next retrain, and repairs them from raw data.
- Strong: adds preventive checks and a post-incident review.
- Weak: "retrain on the latest data" (which uses the corrupted values) or a vague "I would investigate".

**Example:** Illustrative numbers. 600,000 predictions over 21 days is 28,571 per day. A feature scaled by 3 in the live path flags 39.4% of cases, but 26.2% with the correct feature; 98,672 decisions (16.4%) would change on re-score: 89,135 wrongly flagged and 9,537 missed. AUC on the three weeks is 0.791 live against 0.822 corrected. The 10,000 flips with the biggest score gap cover 10.1% of the flips (mean score gap 0.607), so a ranked queue is a way to start, not to finish; a rule-based bulk reversal for the rest is needed. This month's training table has 75% affected rows. A retrain on the logged values gets AUC 0.7850 on a clean holdout (feature coefficient 0.43), a retrain on recomputed-from-raw gets 0.8206 (coefficient 1.20), and dropping the bad rows gets 0.8206 (1.19). The old model scores 0.8206 on the same holdout.
- Weak answer: "I will retrain with this month's data."
- Strong answer: "Fix the feature, re-score the window to find which decisions flip, and rebuild the training table from raw before any retrain."

**Code:**
```python
# Q16: a feature computed wrongly for three weeks; contain, re-score, do not poison the retrain (illustrative, seeded)
import numpy as np
from scipy.stats import rankdata
rng = np.random.default_rng(16)
sig = lambda z: 1 / (1 + np.exp(-z))
def auc(y, s):
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
def fit(X, y, it=25):
    X1 = np.c_[np.ones(len(X)), X]; b = np.zeros(X1.shape[1])
    for _ in range(it):
        p = sig(X1 @ b); W = p * (1 - p)
        b += np.linalg.solve(X1.T @ (X1 * W[:, None]) + 1e-6 * np.eye(len(b)), X1.T @ (y - p))
    return b
pred = lambda b, X: sig(np.c_[np.ones(len(X)), X] @ b)

# Volume arithmetic
days, total = 21, 600_000
per_day = total / days
print(f"{total:,} predictions over {days} days = {per_day:,.0f} per day")
assert round(per_day) == 28571

# Truth: f1 = recency (correct), f2 = spend. Bug: spend is scaled x3 (a unit-mix error) for 3 of the last 4 weeks.
def gen(n):
    f1, f2 = rng.normal(size=n), rng.normal(size=n)
    y = (rng.random(n) < sig(-1.0 + 1.0 * f1 + 1.2 * f2)).astype(int)
    return f1, f2, y
# Old model trained on clean history
f1h, f2h, yh = gen(100_000)
b_old = fit(np.c_[f1h, f2h], yh)

# Three weeks of live traffic (600,000 predictions) with the bug in f2
f1, f2, y = gen(total)
f2_bug = f2 * 3.0
s_live = pred(b_old, np.c_[f1, f2_bug]); s_true = pred(b_old, np.c_[f1, f2])
thr = 0.5
dec_live, dec_true = s_live >= thr, s_true >= thr
flip = dec_live != dec_true
print(f"approved/flagged live {dec_live.mean():.3f} vs with correct feature {dec_true.mean():.3f}")
print(f"decisions that change on re-score: {flip.sum():,} of {total:,} ({100*flip.mean():.1f}%)")
print(f"  flagged wrongly (live yes, true no): {(dec_live & ~dec_true).sum():,};  missed (live no, true yes): {(~dec_live & dec_true).sum():,}")
assert flip.sum() > 0 and flip.mean() < 0.5
print(f"AUC live {auc(y, s_live):.3f} vs corrected {auc(y, s_true):.3f}")
# Triage: only re-visit flipped decisions, ranked by how far the score moved
gap = np.abs(s_live - s_true)
rank = np.argsort(-(gap * flip))
top = rank[:10_000]
print(f"revisit queue: all flips {flip.sum():,}; first 10,000 by score gap cover {100*flip[top].sum()/flip.sum():.1f}% of flips, mean gap {gap[top].mean():.3f}")

# Training data: this month's table logged the buggy f2 for 21 of 28 days
frac_bad = 21 / 28
print(f"share of this month's training rows with the bad feature = {100*frac_bad:.0f}%")
assert abs(frac_bad - 0.75) < 1e-12
n_tr = 200_000
a1, a2, ay = gen(n_tr)
bad = rng.random(n_tr) < frac_bad
a2_logged = np.where(bad, a2 * 3.0, a2)
t1, t2, ty = gen(100_000)                         # clean holdout, correct feature
variants = {
  "retrain on logged (bug included)": fit(np.c_[a1, a2_logged], ay),
  "retrain on recomputed-from-raw":   fit(np.c_[a1, a2], ay),
  "retrain on clean rows only":       fit(np.c_[a1[~bad], a2_logged[~bad]], ay[~bad]),
}
res = {}
for k, b in variants.items():
    res[k] = auc(ty, pred(b, np.c_[t1, t2])); print(f"{k:36} AUC on clean holdout {res[k]:.4f}   coef spend {b[2]:.2f}")
print(f"old model on clean holdout                 AUC {auc(ty, pred(b_old, np.c_[t1, t2])):.4f}")
r = list(res.values())
assert r[1] >= r[0] and r[1] >= r[2] - 0.003
# a retrain on logged rows would also see a mixed-scale feature
assert abs(variants["retrain on logged (bug included)"][2] - variants["retrain on recomputed-from-raw"][2]) > 0.2
```

**Output (my run):**
```text
600,000 predictions over 21 days = 28,571 per day
approved/flagged live 0.394 vs with correct feature 0.262
decisions that change on re-score: 98,672 of 600,000 (16.4%)
  flagged wrongly (live yes, true no): 89,135;  missed (live no, true yes): 9,537
AUC live 0.791 vs corrected 0.822
revisit queue: all flips 98,672; first 10,000 by score gap cover 10.1% of flips, mean gap 0.607
share of this month's training rows with the bad feature = 75%
retrain on logged (bug included)     AUC on clean holdout 0.7850   coef spend 0.43
retrain on recomputed-from-raw       AUC on clean holdout 0.8206   coef spend 1.20
retrain on clean rows only           AUC on clean holdout 0.8206   coef spend 1.19
old model on clean holdout                 AUC 0.8206
```

**Follow-ups:**
- How do you prevent recurrence? Compare the live feature with an independent recomputation on a sample, and test units and ranges; Book 4 Part 6, Q35 ("Training-serving skew and preprocessing in the serving path.") covers skew checks.
- What if raw data is gone? Drop the affected rows and shorten the training window, or model the bug as a known transformation if it is invertible; say what the loss of data costs.
- Who do you tell? The model owner, the business owner of the decisions, risk and compliance for regulated decisions, and the downstream consumers.

**Common mistakes:** Fixing the code but retraining on the corrupted table. Re-scoring everything with no triage. Reversing customer decisions without legal input. Assuming the fix is done without recomputing a sample. No data versioning, so nobody knows which table was poisoned.

### Q17 ⭐⭐ 🟢 A weekly dashboard shows model accuracy of 93.1% one week and 92.4% the next, each from 20,000 scored cases, and a manager asks if the model is degrading. Explain how you decide whether a change this size is signal or noise, and what monitoring design avoids both false alarms and missed slow declines.
**Asked at:** Production-degradation question banks (Dataford pages such as 'if a model's performance drops in production, what is your step-by-step diagnostic process', a Prepfully 'diagnose and fix a model deployed to production that underperformed' answer page, a TryExponent production-ML course page); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** With 20,000 cases a week the 0.7-point drop is just beyond pure sampling noise (z about 2.7), but one weekly step tells me little, so I judge it against the history and watch the trend with a control chart plus a pooled window.

**Clarifying questions:**
- Are the 20,000 cases a fresh random sample each week, or the same users and a different mix? Why: a changed mix can move accuracy with no change in the model.
- What was the week-to-week spread over the last three months? Why: the real noise includes mix and seasonality, not only binomial noise.
- Is accuracy the right metric, given class imbalance and different costs of errors? Why: a stable accuracy can hide worse recall.
- Are labels complete for both weeks (no maturation lag)? Why: immature labels fake a drop (Q28 in this part).
- What would a decline of this size cost? Why: it sets how much alerting noise is acceptable.

**Approach:**
1. Compute the sampling noise: SE of the difference = sqrt(p1 (1 - p1) / n + p2 (1 - p2) / n) = 0.259 points; z = 0.7 / 0.259 = 2.70; two-sided p = 0.007.
2. Read that honestly: it is not just random noise at the usual level, but it is one of 51 weekly comparisons a year; at p < 0.05 you expect about 2.6 false alarms a year on a stable model.
3. Check history: is a 0.7-point move unusual compared with the last 12 to 26 weeks, once mix and calendar effects are controlled?
4. Check segments and inputs for what changed (mix, one segment, a feature), before calling it model decay.
5. Design the monitor: a control chart (limits at 3 standard errors around a baseline from a stable reference period) for sudden change, a pooled multi-week window (or CUSUM) for slow declines, alert only on a sustained or large movement, and a segment panel.
6. Decide actions by tiers: log, investigate, page.
7. Review the baseline and limits every quarter.

**Metrics:**
- Accuracy = correct / scored cases, with a binomial 95% interval (+/- 0.35 points at 93.1% and n = 20,000).
- Minimum detectable week-over-week change at 80% power = (1.96 + 0.84) x SE = about 0.73 points.
- False-alarm rate per week and expected alarms per year on a stable model; detection delay on a slow decline.
- Guardrail: recall or cost-weighted error next to accuracy.

**Risks:**
- Comparing only adjacent weeks makes every normal wobble look like news.
- Binomial noise understates real noise because mix and seasonality add variance.
- A slow decline of 0.05 points a week is invisible to week-over-week tests.
- A rule tuned on one stable stretch alarms often after a promotion or holiday.

**What the interviewer scores:**
- Strong: computes the standard error and z, says what the test does and does not prove, and notes the multiple-looks problem.
- Strong: separates sudden change from slow drift and uses a different tool for each.
- Strong: checks mix and labels before blaming the model.
- Weak: "0.7 points is small, it's noise" with no calculation, or "p < 0.05 so it's degrading".

**Example:** Illustrative numbers. p1 = 0.931, p2 = 0.924, n = 20,000 each: SE = 0.259 points, z = 2.70, p = 0.0069, and the smallest change detectable at 80% power is 0.73 points. One week alone is 93.1% +/- 0.35 points. In a simulation of a stable 92.8% model over 52 weeks the "week-over-week p < 0.05" rule fires on 5.0% of weeks (about 2.6 a year), a 3-sigma control limit fires on 0.47% of weeks, and the pooled 4-week rule fires on 0.77% of windows with a 13.1% chance of at least one false alarm in the year. When accuracy actually loses 0.05 points a week, the week-over-week rule fires on 4.9% of weeks, which is no different from its false-alarm rate of 5.0%, so it cannot see the decline; the 3-sigma limit detects it in all runs with a mean delay of 8.6 weeks and the pooled 4-week rule with 7.3 weeks.
- Weak answer: "Accuracy dropped, so the model is degrading," or "it's within noise."
- Strong answer: "That step has z of 2.7 on sampling noise alone, so I check it against history and segments, and use a control chart plus a pooled window for slow decline."

**Code:**
```python
# Q17: is 93.1% -> 92.4% (n=20,000 each) signal or noise, and what monitoring design? (illustrative, seeded)
import numpy as np
from scipy.stats import norm
rng = np.random.default_rng(17)

p1, p2, n = 0.931, 0.924, 20_000
se = np.sqrt(p1 * (1 - p1) / n + p2 * (1 - p2) / n)
z = (p1 - p2) / se
pval = 2 * (1 - norm.cdf(z))
print(f"two-proportion test: SE = {100*se:.3f} points, z = {z:.2f}, two-sided p = {pval:.4f}")
assert abs(se - 0.002593) < 1e-5 and 2.6 < z < 2.8 and 0.005 < pval < 0.009
mde = (norm.ppf(0.975) + norm.ppf(0.8)) * se
print(f"smallest week-over-week change detectable with 80% power at this n: {100*mde:.2f} points")
assert 0.0070 < mde < 0.0077
# Single-sample 95% interval for one week
hw = 1.96 * np.sqrt(p1 * (1 - p1) / n)
print(f"one week 93.1% +/- {100*hw:.2f} points (binomial noise alone)")

# Simulation: stable model at 92.8% for 52 weeks, n=20,000 per week
W, runs, base = 52, 4000, 0.928
wk = rng.binomial(n, base, size=(runs, W)) / n
# Rule A: alert whenever this week differs from last week at p<0.05 (two-proportion z)
zA = (wk[:, 1:] - wk[:, :-1]) / np.sqrt(2 * base * (1 - base) / n)
fa_A = (np.abs(zA) > 1.96).mean()
# Rule B: Shewhart 3-sigma limits around the baseline measured in a 8-week reference window
ref_mu = wk[:, :8].mean(axis=1, keepdims=True)
sd = np.sqrt(ref_mu * (1 - ref_mu) / n)
fa_B = (np.abs(wk[:, 8:] - ref_mu) > 3 * sd).mean()
# Rule C: pooled 4-week window (80,000 cases) against the same baseline, 3-sigma limit on the pooled rate
roll = np.stack([wk[:, t - 3:t + 1].mean(axis=1) for t in range(11, W)], axis=1)   # windows fully after the reference period
sdC = sd / 2
fa_C = (roll < ref_mu - 3 * sdC).mean()
fa_C_runs = (roll < ref_mu - 3 * sdC).any(axis=1).mean()
print(f"stable model, 52 weeks: week-on-week p<0.05 rule false alarms/week = {100*fa_A:.1f}% (about {fa_A*51:.1f} per year)")
print(f"  3-sigma control limit false alarms/week = {100*fa_B:.2f}% ; pooled 4-week rule: false alarms/window = {100*fa_C:.2f}%, chance of any false alarm in the year = {100*fa_C_runs:.1f}%")
assert 0.04 < fa_A < 0.06 and fa_B < 0.01 and fa_C_runs < 0.20

# Slow decline: 0.05 points lost per week starting at week 9 (index 8)
decl = base - 0.0005 * np.maximum(0, np.arange(W) - 8)
wk_d = rng.binomial(n, decl, size=(runs, W)) / n
ref2 = wk_d[:, :8].mean(axis=1, keepdims=True); sd2 = np.sqrt(ref2 * (1 - ref2) / n)
# week-on-week rule: alert if drop vs last week significant; slow decline moves 0.15 pts a week, below its MDE
zD = (wk_d[:, 1:] - wk_d[:, :-1]) / np.sqrt(2 * base * (1 - base) / n)
alerts_A = ((zD < -1.96)[:, 8:]).mean()
first_B = np.full(runs, -1)
for t in range(8, W):
    hit = (wk_d[:, t] < ref2[:, 0] - 3 * sd2[:, 0]) & (first_B < 0); first_B[hit] = t
rollD = np.stack([wk_d[:, t - 3:t + 1].mean(axis=1) for t in range(11, W)], axis=1)
first_C = np.full(runs, -1)
for j, t in enumerate(range(11, W)):
    hit = (rollD[:, j] < ref2[:, 0] - 3 * sd2[:, 0] / 2) & (first_C < 0); first_C[hit] = t
def delay(f):
    ok = f >= 0
    return ok.mean(), (f[ok] - 8).mean()
dB, dC = delay(first_B), delay(first_C)
print(f"slow decline 0.05 pt/week from week 9: weekly drop alert fires in {100*alerts_A:.1f}% of those weeks (looks like noise level {100*fa_A:.1f}%)")
print(f"  3-sigma limit: detected in {100*dB[0]:.0f}% of runs, mean delay {dB[1]:.1f} weeks;  pooled 4-week: detected {100*dC[0]:.0f}%, mean delay {dC[1]:.1f} weeks")
assert dC[0] > 0.95 and dC[1] < dB[1] and alerts_A < 0.08
```

**Output (my run):**
```text
two-proportion test: SE = 0.259 points, z = 2.70, two-sided p = 0.0069
smallest week-over-week change detectable with 80% power at this n: 0.73 points
one week 93.1% +/- 0.35 points (binomial noise alone)
stable model, 52 weeks: week-on-week p<0.05 rule false alarms/week = 5.0% (about 2.6 per year)
  3-sigma control limit false alarms/week = 0.47% ; pooled 4-week rule: false alarms/window = 0.77%, chance of any false alarm in the year = 13.1%
slow decline 0.05 pt/week from week 9: weekly drop alert fires in 4.9% of those weeks (looks like noise level 5.0%)
  3-sigma limit: detected in 100% of runs, mean delay 8.6 weeks;  pooled 4-week: detected 100%, mean delay 7.3 weeks
```

**Follow-ups:**
- Which test? A two-proportion z-test for accuracy with paired data being better if the same cases are scored twice; Book 1 Part 10, Q20 ("Which statistical test do you use for conversion-rate metrics vs continuous metrics like revenue per user?") covers the setup.
- How do you avoid alert fatigue? Require a sustained breach (N of M windows) and tier the alerts; Book 4 Part 8, Q11 ("Alerting design for ML monitoring.") covers alert design.
- Is a larger sample the fix? It narrows binomial noise, but mix and seasonality noise remain.

**Common mistakes:** Calling it noise without computing anything. Using week-over-week p-values as an alarm. Ignoring mix changes. Alerting on a single point. Using accuracy alone on an imbalanced problem.

### Q18 ⭐⭐ 🟢 A support-ticket router's accuracy is stable, but the company has just launched a new product line that generates tickets with categories the model never saw. Explain what failure mode this is, how you would detect that such tickets are being misrouted, and what you would do in the short and long term.
**Asked at:** No public page found, editor-designed from standard production-ML judgement themes that the degradation guides describe in general terms; search snippets only, not opened
**Say this first (1 line):** This is an open-set (novel-class) failure: the model is forced to pick one of its old categories for tickets that belong to none of them, so accuracy on known categories stays high while the new line is silently misrouted.

**Clarifying questions:**
- What label does a ticket from the new product line get in our accuracy data (a new category, "other", nothing)? Why: if new-line tickets are excluded from the metric, stable accuracy is no evidence.
- How many tickets does the new line produce, and what does a misroute cost (hours of delay, escalations)? Why: it sets urgency and the acceptable triage load.
- Can the model say "I don't know", and is there a human triage queue? Why: it decides whether a reject option is possible this week.
- Is there product metadata (a product ID) on each ticket? Why: a rule can route the new line immediately.
- How soon can we get labelled new-line tickets? Why: it sets the retraining plan.

**Approach:**
1. Name it: novel classes and covariate shift in the input; accuracy on known categories cannot see tickets that have no correct known label.
2. Detect misrouting without labels: share of tickets with a new product ID or new vocabulary, low model confidence, large distance from known category centres in embedding space, reopen and re-route rates, and handling time by queue.
3. Short term: a rule on product ID or keyword routes the new line to a human or a temporary queue; set a reject threshold so low-confidence or far-from-known tickets go to triage.
4. Measure the reject rule: of known tickets, what share would be flagged (cost of extra triage), and of new-line tickets, what share is caught.
5. Collect labels for the new line from the triage queue (a few hundred per category) and keep them as a separate evaluation set.
6. Long term: add the new categories and retrain, with a "none of the above" class and a novelty detector; monitor per-category volume and the share of flagged tickets.
7. Put the launch calendar in the process: product launches notify the ML team in advance.

**Metrics:**
- Known-category accuracy = correct known-category tickets / known-category tickets (what the dashboard shows).
- True routing correctness = correct routes / all tickets (new-line tickets count as wrong unless routed correctly).
- Novel-ticket catch rate = flagged new-line tickets / new-line tickets; false-flag rate = flagged known tickets / known tickets.
- Triage precision = new-line tickets in the flagged queue / flagged tickets.
- Guardrail: triage queue size versus staffing.

**Risks:**
- Softmax confidence is a weak novelty detector: models can be confident about things they have never seen.
- A reject threshold floods the queue with hard but known tickets.
- Relabelling after the fact can leak into evaluation.
- A rule on product ID breaks when the product line renames things.

**What the interviewer scores:**
- Strong: identifies that the metric is blind to unseen classes and proposes unlabelled detection signals.
- Strong: gives short-term (rule, triage) and long-term (retrain, novelty detection) actions and measures the cost of the reject rule.
- Strong: asks how new-line tickets appear in the accuracy metric.
- Weak: "accuracy is stable, so nothing is wrong" or "just retrain" with no new labels.

**Example:** Illustrative numbers. Of 10,000 weekly tickets 12% (1,200) are from the new line and 8,800 are known. In a simulation, accuracy on the known tickets is 96.4%, but all 1,200 new-line tickets are forced into a known category with mean confidence 0.65 (known tickets 0.89), so true routing correctness is 84.8% of all tickets. A confidence rule at the known tickets' 5th percentile (0.58) catches only 38.3% of the new tickets, while flagging 5.0% of known; a distance-to-nearest-category rule at the 95th percentile catches 78.8%, with the same 5.0% false-flag rate. The weekly triage queue is then 1,386 tickets, of which 946 are new-line (68% precision).
- Weak answer: "Accuracy is stable at 96%, so the router is fine."
- Strong answer: "Accuracy only covers known classes; I would add a novelty flag, a product-ID rule and a human queue now, and retrain with the new categories after I have labels."

**Code:**
```python
# Q18: unseen ticket categories (open-set problem). Illustrative simulation, seeded, numpy only.
import numpy as np
rng = np.random.default_rng(18)

D, K = 6, 5
centroids = rng.normal(0, 3.0, size=(K, D))              # 5 known categories
novel_centre = rng.normal(0, 3.0, size=D)                # new product line: a region the model never saw
def tickets(n, centre): return centre + rng.normal(0, 1.2, size=(n, D))

def softmax_conf(X, T=2.0):
    d2 = ((X[:, None, :] - centroids[None]) ** 2).sum(-1)
    logits = -d2 / (2 * T * T)
    e = np.exp(logits - logits.max(1, keepdims=True)); p = e / e.sum(1, keepdims=True)
    return p.argmax(1), p.max(1), d2.min(1)

# Traffic: 10,000 tickets/week, 12% from the new line
n_total, share = 10_000, 0.12
n_new = int(n_total * share); n_known = n_total - n_new
assert n_new == 1200 and n_known == 8800
Xk_list, yk = [], []
for k in range(K):
    m = n_known // K + (1 if k < n_known % K else 0)
    Xk_list.append(tickets(m, centroids[k])); yk += [k] * m
Xk, yk = np.vstack(Xk_list), np.array(yk)
Xn = tickets(n_new, novel_centre)
pk, ck, dk = softmax_conf(Xk); pn, cn, dn = softmax_conf(Xn)
acc_known = (pk == yk).mean()
print(f"accuracy on KNOWN categories (what the dashboard measures) = {100*acc_known:.1f}%")
print(f"all {n_new} new-line tickets get a known-category label anyway: mean confidence {cn.mean():.2f} (known: {ck.mean():.2f})")
print(f"true overall routing correctness = {100*(pk == yk).sum()/n_total:.1f}% of all tickets (new-line tickets are all misrouted)")
assert acc_known > 0.9 and (pk == yk).sum() / n_total < acc_known * 0.9

# Detection 1: max-softmax confidence threshold at the 5th percentile of KNOWN tickets
thr = np.quantile(ck, 0.05)
print(f"confidence rule (flag if < {thr:.2f}): catches {100*(cn < thr).mean():.1f}% of new-line tickets, flags {100*(ck < thr).mean():.1f}% of known")
# Detection 2: distance to nearest category centre (embedding-distance rule) at the 95th percentile of KNOWN
dthr = np.quantile(dk, 0.95)
print(f"distance rule (flag if > {dthr:.1f}): catches {100*(dn > dthr).mean():.1f}% of new-line tickets, flags {100*(dk > dthr).mean():.1f}% of known")
assert (dn > dthr).mean() > (cn < thr).mean() - 1e-9 and (dn > dthr).mean() > 0.7
# What the flag volume looks like in the weekly queue
flag_known = (dk > dthr).sum(); flag_new = (dn > dthr).sum()
print(f"weekly human-triage queue: {flag_new + flag_known} tickets, of which {flag_new} are new-line ({100*flag_new/(flag_new+flag_known):.0f}% precision)")
# Share-of-flagged trend as a launch monitor: the novel share of flagged tickets rises from 0% to ~12% of traffic
```

**Output (my run):**
```text
accuracy on KNOWN categories (what the dashboard measures) = 96.4%
all 1200 new-line tickets get a known-category label anyway: mean confidence 0.65 (known: 0.89)
true overall routing correctness = 84.8% of all tickets (new-line tickets are all misrouted)
confidence rule (flag if < 0.58): catches 38.3% of new-line tickets, flags 5.0% of known
distance rule (flag if > 17.8): catches 78.8% of new-line tickets, flags 5.0% of known
weekly human-triage queue: 1386 tickets, of which 946 are new-line (68% precision)
```

**Follow-ups:**
- Why not just add classes? You need labelled examples first, and the triage queue is how you get them.
- How do you keep the reject rule honest over time? Track the share flagged and the precision of the queue weekly, and recalibrate the threshold as the new categories get added.
- Which general theory? Book 4 Part 8, Q1 ("Why do ML models degrade after deployment?") lists the failure types.

**Common mistakes:** Trusting softmax confidence alone. Computing accuracy only on categories the model knows. Waiting for complaints. Forcing every ticket to a known queue. Forgetting that new labels must come from somewhere.

### Q19 ⭐⭐ 🟢 An engineer proposes retraining a pricing-support classifier every night so it never goes stale. Explain what you would check before agreeing, such as whether performance actually decays, the cost and risk of each retrain, and what you would want as a trigger instead of a blind schedule.
**Asked at:** No interview question page located for this exact scenario; practitioner fraud and retraining guides (a Firstsource fraud-model post, a datainterview.com 'when to retrain' course page) describe the retrain-versus-rollback and adaptive-fraud themes, so editor-designed; search snippets only, not opened
**Say this first (1 line):** I would not agree to a nightly retrain until I have measured how fast this model actually decays and what each retrain costs and risks, because a blind nightly schedule adds cost and the chance of shipping a bad model for a gain that may be tiny.

**Clarifying questions:**
- What does a stale model cost per day of age, in accuracy and in rupees? Why: it is the benefit side of the trade-off and I have no number yet.
- How fast does the data change (new pricing plans, new products, seasonality)? Why: a stable classifier needs far fewer retrains than a fast-moving one.
- What does a retrain cost (compute, labelling, review) and what checks run before deploy? Why: cost and the gate decide how often we can afford to retrain.
- How are labels produced and how late? Why: nightly retraining on yesterday's immature labels trains on noise.
- Who owns the model if a bad retrain ships at 2 a.m.? Why: automation needs an owner and a rollback.

**Approach:**
1. Measure decay first: evaluate old model versions on recent matured data (a "model age" curve). If accuracy barely moves in a week, nightly buys nothing.
2. Price the options: schedule every 1, 7 and 30 days versus a trigger. Mean model age under a T-day schedule is (T - 1) / 2 days, so the average decay loss is (T - 1) / 2 x daily decay.
3. Count the downside: each retrain has run-to-run noise and some chance of training on a bad extract. A nightly retrain means 365 chances a year.
4. Require a gate for any automatic retrain: champion-challenger comparison on a fixed, time-split holdout, data validation, and an approval step for large changes. A rollback must be one click.
5. Prefer triggers: retrain when matured-label performance or calibration falls beyond a limit, or when drift alerts and a performance check agree, plus a slow safety-net schedule.
6. Define the review: track retrains per quarter, models blocked by the gate, and accuracy gained per retrain.
7. Revisit the cadence every quarter as decay changes.

**Metrics:**
- Decay rate = accuracy points lost per day of model age, from the age curve.
- Mean accuracy over the period and share of days below an accuracy floor, by policy.
- Retrains per period, and glitch models deployed per period.
- Cost per retrain and gain per retrain = (accuracy points gained) x (value per point) / cost.
- Guardrail: the challenger must not lose more than a small margin to the champion on the holdout.

**Risks:**
- Nightly retraining chases noise and can overwrite a good model with a worse one.
- Training on immature labels or a partial day.
- Lack of reproducibility: if the model changes every night, a bug cannot be traced to a version.
- Gates measure with noise too, so they block some good models and pass some bad ones.

**What the interviewer scores:**
- Strong: asks for the decay curve and cost, and quantifies the benefit of a shorter cadence.
- Strong: names the risks of automated retraining (bad data, noise, no owner) and requires a gate and rollback.
- Strong: proposes a trigger plus a slow schedule.
- Weak: "more retraining is always better" or "never automate".

**Example:** Illustrative numbers, with an assumed decay of 0.03 accuracy points a day. A schedule of T days has mean age (T - 1) / 2: 7 days gives 3.0 days and 0.090 points lost, 30 days gives 14.5 days and 0.435 points lost, nightly gives 0. In a 180-day simulation with run-to-run retrain noise (sd 0.25 points), a 2% chance a retrain is trained on a corrupted extract (costing 3 points), and a noisy deploy gate: nightly with no gate ships 3.68 glitch models over 180 days and has 2.0% of days below the 88.5% floor; nightly with a gate ships none and averages 90.13% (it also tends to keep the luckier candidates); weekly with a gate averages 89.93% on 25 retrains; monthly with a gate averages 89.54% on 6 retrains with 0.8% of days below the floor; a trigger policy averages 89.60% on 5.7 retrains. So the gate matters more than the cadence, and nightly buys about 0.2 points over weekly for 155 extra retrains; it is worth it only if a point of accuracy is worth more than 155 retrains cost.
- Weak answer: "Nightly retraining keeps the model fresh."
- Strong answer: "I would measure the decay, price a retrain, require a gate, and pick a trigger with a slow schedule as backup."

**Code:**
```python
# Q19: nightly retrain versus schedule versus trigger (illustrative simulation, seeded, numpy only)
import numpy as np
rng = np.random.default_rng(19)

DAYS, RUNS = 180, 400
FRESH = 90.0          # accuracy (%) of a freshly trained model, before retrain noise
DECAY = 0.03          # accuracy points lost per day of model age (illustrative; the real value is the thing to measure)
RETRAIN_SD = 0.25     # run-to-run noise of one retrain, in accuracy points (data sampling + seed)
GLITCH_P = 0.02       # chance a retrain is trained on a corrupted extract
GLITCH_HIT = 3.0      # accuracy points lost by a glitch model
COST = 1.0            # cost units per retrain run (compute + review); report counts as well
GATE_SD = 0.3         # the champion-challenger gate measures accuracy with this noise (points)

def simulate(policy, gate):
    acc_log = np.zeros((RUNS, DAYS)); retrains = np.zeros(RUNS); bad_live = np.zeros(RUNS)
    for r in range(RUNS):
        level = FRESH + rng.normal(0, RETRAIN_SD)      # the live model's accuracy when deployed
        age = 0; last_obs = level
        for d in range(DAYS):
            acc = level - DECAY * age
            acc_log[r, d] = acc
            obs = acc + rng.normal(0, 0.15)            # matured-label weekly estimate (noisy)
            retrain = (policy == "nightly") or \
                      (policy == "weekly" and d % 7 == 6) or \
                      (policy == "monthly" and d % 30 == 29) or \
                      (policy == "trigger" and obs < FRESH - 1.0)
            if retrain:
                retrains[r] += 1
                cand = FRESH + rng.normal(0, RETRAIN_SD)
                glitch = rng.random() < GLITCH_P
                if glitch: cand -= GLITCH_HIT
                # gate: deploy only if candidate looks at least as good as the live model, measured with noise
                deploy = True
                if gate:
                    deploy = (cand + rng.normal(0, GATE_SD)) >= (acc + rng.normal(0, GATE_SD)) - 0.2
                if deploy:
                    level, age = cand, 0
                    if glitch: bad_live[r] += 1
                else:
                    age += 1
            else:
                age += 1
    return acc_log, retrains, bad_live

rows = []
for policy, gate in [("nightly", False), ("nightly", True), ("weekly", True), ("monthly", True), ("trigger", True)]:
    a, rt, bl = simulate(policy, gate)
    rows.append((policy, gate, a.mean(), (a < 88.5).mean(), rt.mean(), bl.mean()))
print("policy   gate  mean acc  days below 88.5  retrains/180d  glitch models deployed")
for p, g, m, f, rt, bl in rows:
    print(f"{p:8} {str(g):5} {m:8.3f}  {100*f:12.1f}%  {rt:12.1f}  {bl:10.2f}")
R = {(p, g): (m, f, rt, bl) for p, g, m, f, rt, bl in rows}
# Claims that go into the answer
assert R[("nightly", False)][3] > 1.0                      # nightly without a gate ships glitch models
assert R[("nightly", True)][3] < R[("nightly", False)][3]  # a gate removes most of them
assert R[("weekly", True)][0] > R[("monthly", True)][0]    # some retraining beats too little
print(f"nightly+gate vs weekly+gate: mean accuracy difference {R[('nightly', True)][0]-R[('weekly', True)][0]:+.3f} points for {R[('nightly', True)][2]-R[('weekly', True)][2]:.0f} extra retrains")
# Back-of-envelope: average age under a schedule of T days is (T-1)/2 days (age 0 right after training)
for T in (1, 7, 30):
    print(f"schedule every {T:2d} days: mean age {(T-1)/2:.1f} days -> average decay loss {(T-1)/2*DECAY:.3f} points")
assert abs((7 - 1) / 2 * DECAY - 0.09) < 1e-12 and abs((30 - 1) / 2 * DECAY - 0.435) < 1e-12
```

**Output (my run):**
```text
policy   gate  mean acc  days below 88.5  retrains/180d  glitch models deployed
nightly  False   89.941           2.0%         180.0        3.68
nightly  True    90.130           0.0%         180.0        0.00
weekly   True    89.930           0.0%          25.0        0.00
monthly  True    89.543           0.8%           6.0        0.00
trigger  True    89.602           0.0%           5.7        0.00
nightly+gate vs weekly+gate: mean accuracy difference +0.200 points for 155 extra retrains
schedule every  1 days: mean age 0.0 days -> average decay loss 0.000 points
schedule every  7 days: mean age 3.0 days -> average decay loss 0.090 points
schedule every 30 days: mean age 14.5 days -> average decay loss 0.435 points
```

**Follow-ups:**
- What would make nightly the right answer? A fast-moving domain (fraud tactics, prices), cheap and well-gated automation, and mature labels each day. Q25 in this part covers adversarial change.
- What triggers would you use? Matured-label performance, calibration, and drift signals that agree; Book 4 Part 8, Q12 ("Retraining triggers and policy") compares the options.
- What if the gate is noisy? Use a larger holdout, repeated seeds, and require a margin before deploy.

**Common mistakes:** Assuming decay without measuring. Ignoring the retrain's failure modes. Retraining on immature labels. No rollback plan. Confusing a fresh model with a better model.

### Q20 ⭐⭐ 🟡 An upstream team renamed a column and changed its type, and a default of 0 is now silently filled in where the model expects order_value in rupees. Labelled AUC falls from 0.85 to 0.82 over a week before anyone notices. Explain how you would find the cause quickly and what checks (schema, range, null, contract) would have caught it on day one.
**Asked at:** Upstream schema and silent feature-pipeline failure write-ups (Towards AI schema-migration post, RisingWave feature-pipeline observability, ActiveWizards Kafka schema-evolution post, dataexpert.io schema-drift post); practitioner posts rather than interview banks, so scenario is editor-designed; search snippets only, not opened
**Say this first (1 line):** I would split live traffic by the day and the ingestion path to find the moment the feature changed, confirm that order_value is suddenly zero for a share of rows, and note that a default of 0 passes null checks, so only range, zero-share and contract checks would have caught it on day one.

**Clarifying questions:**
- When did the AUC start to fall, and what deployed upstream that day? Why: the first bad day names the change and the owner.
- What share of rows now carries a zero order_value and is it tied to one source or path? Why: it separates a full break from a partial one.
- Is there a data contract or schema registry for this table, and who owns it? Why: it decides whether the fix is a contract enforcement or a patch.
- Can we re-compute order_value from the raw order table for the affected days? Why: it decides whether past scores and training data can be repaired.
- Do other features come from the same upstream change? Why: a rename rarely breaks only one column.

**Approach:**
1. Plot the daily feature statistics (zero share, null share, median, quantiles) for the last month; look for a step change.
2. Find the first day of the step, then match it to upstream deploys and schema changes.
3. Confirm by slicing: AUC and feature values for rows through the new path versus the old path.
4. Fix: map the new column name and type, backfill the affected days from raw data, and re-score what matters (see Q16 in this part for the sizing and retrain protection).
5. Add day-one checks: schema (column name and type present), null rate, range (minimum above 0, maximum sane), zero share (a default 0 shows up here), distribution versus a reference (PSI, median) and a freshness check.
6. Add a contract: the upstream team owns the schema, publishes changes with notice, and a breaking change fails their CI; the model service rejects or quarantines a batch that violates the contract rather than filling defaults.
7. Make defaults loud: never silently fill a missing numeric feature with 0; use null plus a missing-indicator, or fail.

**Metrics:**
- Zero share = rows with order_value = 0 / rows. Normal is near 0%; an abrupt step is the signal.
- Null rate = null rows / rows (a default of 0 hides here, so it passes).
- Range and distribution: minimum, median, and PSI against a reference period.
- Labelled AUC by ingestion path and by day.
- Guardrail: time to detection (days from the break to the alert) and number of bad predictions before detection.

**Risks:**
- A type change plus a default can pass a loose schema check.
- Averaged AUC falls slowly if only a minority of rows are affected, so a performance-only monitor is days late.
- Backfilling with a "typical value" hides the problem and distorts training.
- Fixing the feature without repairing the logged values poisons the next retrain.

**What the interviewer scores:**
- Strong: bisects on time and path, and explains why null-rate checks miss a zero default.
- Strong: lists schema, range, zero-share, distribution and contract checks, and says which would fire on day one.
- Strong: asks who owns the contract and proposes quarantine over silent defaults.
- Weak: "retrain the model" or waits for AUC to fall.

**Example:** Illustrative numbers. In a 14-day simulation the upstream change hits 6% of rows from day 8. Zero share jumps from 0.000 to about 0.060 on day 8, the null share stays 0.000, and the median order_value drops from about 400 to about 380. Mean AUC falls from 0.852 before to 0.808 after; on day 8 the rows through the new path have AUC 0.792 against 0.849 for the old path. A day-one check set gives: column present passes, dtype passes, null rate passes, minimum above 0 fails, zero share above 0.5% fails, median in range passes. So the cheap checks that would have caught it are range and zero-share (and a contract on the upstream change); the null-rate check would not.
- Weak answer: "AUC fell, retrain the model."
- Strong answer: "Find the day the zero share stepped up, tie it to the upstream change, and add range, zero-share and contract checks so this fails on day one."

**Code:**
```python
# Q20: renamed column + silent default 0 for order_value (illustrative simulation, seeded, numpy+scipy)
import numpy as np
from scipy.stats import rankdata
rng = np.random.default_rng(20)
sig = lambda z: 1 / (1 + np.exp(-z))
def auc(y, s):
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)

# Fixed model: score uses log(order_value) and one other feature
def model(order_value, other):
    return 1.6 * (np.log1p(order_value) - 6.0) / 0.8 * 0.55 + 1.6 * other
def day_data(n, bad_share):
    ov = rng.lognormal(6.0, 0.8, n)                       # order value in rupees, median about Rs 400
    other = rng.normal(size=n)
    true_logit = -1.0 + 1.6 * (np.log1p(ov) - 6.0) / 0.8 * 0.55 + 1.6 * other
    y = (rng.random(n) < sig(true_logit)).astype(int)
    bad = rng.random(n) < bad_share                        # rows served by the new upstream path
    ov_seen = np.where(bad, 0.0, ov)                       # new column not read -> default 0
    return ov_seen, other, y, bad

DAYS, BREAK, N = 14, 7, 20_000                             # break on day index 7 (day 8)
print("day  zero_share  null_share  median_ov   AUC")
zs, aucs = [], []
for d in range(DAYS):
    share = 0.0 if d < BREAK else 0.06                    # 6% of rows go through the new path
    ov, oth, y, bad = day_data(N, share)
    s = model(ov, oth)
    z = (ov == 0).mean(); zs.append(z); aucs.append(auc(y, s))
    print(f"{d+1:3d}  {z:9.3f}  {0.0:9.3f}  {np.median(ov):9.1f}  {aucs[-1]:.4f}")
pre, post = np.mean(aucs[:BREAK]), np.mean(aucs[BREAK:])
print(f"mean AUC before break {pre:.3f}, after break {post:.3f}")
assert pre - post > 0.015
assert max(zs[:BREAK]) < 0.001 and min(zs[BREAK:]) > 0.04

# Day-one checks, written as code
def checks(ov, expected_cols, cols, dtypes):
    out = {}
    out["schema: column present"] = "order_value" in cols
    out["schema: dtype float"] = dtypes.get("order_value") == "float64"
    out["null rate <= 1%"] = np.isnan(ov).mean() <= 0.01
    out["range: min > 0"] = np.nanmin(ov) > 0
    out["zero share <= 0.5%"] = (ov == 0).mean() <= 0.005
    out["median in [200, 800]"] = 200 <= np.nanmedian(ov) <= 800
    return out
ov_ok, _, _, _ = day_data(N, 0.0)
ov_bad, _, _, _ = day_data(N, 0.06)
good = checks(ov_ok, None, ["order_value"], {"order_value": "float64"})
# renamed column: the model-facing frame has the old name filled by default, so schema check on the new name catches it
bad_res = checks(ov_bad, None, ["order_value"], {"order_value": "float64"})
print("check                       healthy day   break day")
for k in good: print(f"{k:27} {str(good[k]):11}   {bad_res[k]}")
assert all(good.values()) and not bad_res["range: min > 0"] and not bad_res["zero share <= 0.5%"] and bad_res["null rate <= 1%"] and bad_res["median in [200, 800]"]
print("note: the null-rate check PASSES on the break day; range and zero-share checks fail (the median check also passes), because the default 0 is a valid number")

# Bisect to the cause with the logged data: AUC by 'served through new path' flag on day 8
ov, oth, y, bad = day_data(N, 0.06)
s = model(ov, oth)
print(f"day 8 AUC overall {auc(y, s):.3f}; rows via new path {auc(y[bad], s[bad]):.3f}; rows via old path {auc(y[~bad], s[~bad]):.3f}")
assert auc(y[~bad], s[~bad]) - auc(y[bad], s[bad]) > 0.02
```

**Output (my run):**
```text
day  zero_share  null_share  median_ov   AUC
  1      0.000      0.000      400.9  0.8530
  2      0.000      0.000      404.6  0.8505
  3      0.000      0.000      402.6  0.8474
  4      0.000      0.000      402.9  0.8484
  5      0.000      0.000      400.4  0.8563
  6      0.000      0.000      397.5  0.8540
  7      0.000      0.000      402.2  0.8572
  8      0.061      0.000      377.2  0.8093
  9      0.058      0.000      378.0  0.8081
 10      0.058      0.000      376.8  0.8091
 11      0.062      0.000      378.4  0.8086
 12      0.060      0.000      375.2  0.8082
 13      0.060      0.000      376.5  0.8099
 14      0.060      0.000      381.5  0.8034
mean AUC before break 0.852, after break 0.808
check                       healthy day   break day
schema: column present      True          True
schema: dtype float         True          True
null rate <= 1%             True          True
range: min > 0              True          False
zero share <= 0.5%          True          False
median in [200, 800]        True          True
note: the null-rate check PASSES on the break day; range and zero-share checks fail (the median check also passes), because the default 0 is a valid number
day 8 AUC overall 0.807; rows via new path 0.792; rows via old path 0.849
```

**Follow-ups:**
- Why did AUC fall only a little? Only a minority of rows were affected and the other features still worked; a small share of badly scored rows still drags the overall metric.
- Where do you run the checks? At ingestion (contract and schema), in the feature pipeline (range, null, zero share) and in the monitor (distribution), so a bad batch is stopped early; Book 4 Part 8, Q14 ("Scenario: your drift dashboard fires an alert for feature X.") covers the alert-triage order.
- Contract tooling? At concept level a schema registry or data-contract test in the producer's CI; Q12 in this part shows why PSI alone is not enough.

**Common mistakes:** Filling missing numerics with 0. Trusting a passing schema check. Alerting only on AUC. Fixing the model before the data. No named owner for the upstream schema.
