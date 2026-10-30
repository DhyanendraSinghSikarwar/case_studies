# Book 6 — Part 2: Model Performance Degraded in Production

**Topic:** Scenario-based "what do you do when..." questions for Data Scientist and ML Engineer loops on a model that gets worse after launch: accuracy, precision, recall or AUC falling, silent data, concept, label and prior drift, label delay and monitoring without labels, training-serving skew, feature-pipeline bugs and null or unit changes, upstream schema changes, feedback loops, seasonality, a model good offline but bad online, threshold and calibration decay, segment-level degradation, retrain versus rollback versus patch, shadow, canary and A/B validation of a fix, adversarial and fraud adaptation, recommender and ranking degradation, forecasting drift, and AI-era twists (LLM and RAG quality degradation, LLM-as-judge drift, agent tool changes).

**Target:** 50  |  **Actual:** 50 (⭐⭐⭐ 16, ⭐⭐ 23, ⭐ 11)  |  **Date:** 2026-10-30  |  **Status:** Complete (answers merged, checked, reviewed)

**Scope note:** this part owns the judgement angle (what do you do, in what order, with what evidence). It does not repeat the concept coverage in Book 1 (for example Part 1 on a model good offline but poor in production, Part 11 on training-serving skew, monitoring and retraining, Part 5 on drift and feedback loops in fraud, Part 6 on forecast monitoring) or the tooling in Book 4 Part 8 (drift tests, monitoring layers, late labels); Wave B answers should cross-reference those only by checked headings. Book 6 Part 1 owns product-metric drops (a business dashboard number fell); here the object is the model. Book 2 owns LLM internals, and here only the production-quality angle appears. All numbers in the prompts are invented illustrative numbers, not data from any company. Stars: 3 means reported in most loops, 2 regular, 1 senior or niche; they are editorial judgements.

**Evidence limits:** WebFetch was unavailable, so no page was opened; every source is a WebSearch snippet or result summary only (see research_notes/Book6_Part02_sources.md). Searches returned production-degradation question banks (Dataford, Prepfully, TryExponent), MLOps and system-design guides on drift, skew and monitoring without labels, practitioner posts on fraud, calibration, schema changes, RAG degradation and shadow or canary rollout, and recommender feedback-loop papers. Forecasting-drift and adversarial-fraud searches found practitioner pages, not interview pages. No result tied a scenario to a named employer, so 'Asked at' lines name guide families only ('commonly reported in public guides'); scenarios marked editor-designed have no located public page. Star counts and difficulty tags are editorial. No salary figures appear anywhere in this part.

---

### Q1 ⭐⭐⭐ 🟢 A fraud classifier launched with an offline AUC of 0.86 and a month later a labelled sample of 30,000 recent transactions gives an AUC of 0.79. Nobody has changed the model code. Walk through what you check first, in order, before deciding whether the model itself is at fault.
**Asked at:** Production-degradation question banks (Dataford pages such as 'if a model's performance drops in production, what is your step-by-step diagnostic process', a Prepfully 'diagnose and fix a model deployed to production that underperformed' answer page, a TryExponent production-ML course page); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Before I blame the model I check the measurement, then the data pipeline, then who is being scored, and only then the model itself; a 0.86 to 0.79 AUC drop can come from any of those four.

**Clarifying questions:**
- How was the 30,000 sample drawn, and are all its labels matured? If it holds only quickly-labelled cases, the sample is biased and the AUC is not comparable.
- How was 0.86 measured: a time split or a random split? A random split is usually optimistic, so part of the gap may be the offline number, not the model.
- How many frauds are in the 30,000? AUC noise depends on positives, not rows.
- Did anything change upstream (feature pipeline, data source, new merchant or country, new payment product)? Code unchanged does not mean inputs unchanged.
- Is there a rule layer or review step that filters transactions before scoring? It changes who the model sees.

**Approach:**
1. Check the number itself. Is 0.79 outside noise? Compute the interval for AUC from the positive count. Recompute AUC with the same code used for 0.86 (same label definition, same time window rules).
2. Check the labels. Matured? Same definition as training (chargeback versus analyst-confirmed)? A label-window mismatch shifts AUC on its own.
3. Check the data pipeline. Null rates, ranges, category levels and feature distributions versus the launch week, then the score distribution. A broken feature shows up here first. See Book 4 Part 8 Q7 (training-serving skew).
4. Check who is being scored. Split AUC by segment (country, channel, amount band, new versus old cards). If segment AUCs are stable but the mix moved, the pooled AUC moved without the model changing.
5. Compare like with like: AUC on the launch month's data scored by the same model, if available, to separate the model from the world.
6. Only now ask whether the world changed against the model: concept drift or adversaries adapting (Book 1 Part 11 Q33, how to handle concept drift and adversaries adapting in a fraud system). Decide: fix pipeline, re-weight or re-slice evaluation, or retrain.

**Metrics:**
- AUC = P(a random fraud scores above a random non-fraud). Numerator: concordant pairs (ties count half), denominator: positives times negatives.
- AUC standard error (Hanley-McNeil) from the positive and negative counts; report the interval, not a point.
- Per-segment AUC and segment share of traffic; pooled AUC change split into "mix" and "within-segment" parts.
- Guardrails: label maturity share of the sample, null rate of each top feature, score-distribution PSI versus launch.

**Risks:**
- Comparing a random-split offline AUC with a live time-split AUC. Not like with like.
- Immature labels: recent frauds not yet confirmed lower recall and AUC artificially.
- A small positive count: 0.79 may have a wide interval.
- Retraining first and hiding a pipeline bug inside the new model.

**What the interviewer scores:**
- Strong: an ordered checklist that starts with measurement and data. Weak: "retrain it" or "it is drift".
- Strong: quantifies noise (the interval) and a mix effect. Weak: says "the drop looks big".
- Strong: asks about label definition and maturity. Weak: assumes labels are clean.
- Strong: ends with a decision rule per finding. Weak: lists causes with no action.

**Example:** (illustrative numbers) 30,000 transactions, 2% fraud, so 600 frauds. The AUC interval for 0.79 is about 0.768 to 0.812, so 0.86 is far outside it; the drop is not noise. Next, two segments: domestic (AUC 0.92) and cross-border (AUC 0.68). At launch cross-border was 10% of traffic and the pooled AUC was 0.846; now it is 30% and the pooled AUC is 0.769, with both segment AUCs unchanged. The pooled drop of 0.077 is almost exactly the reported 0.07 and the model did not change.
- Weak: "AUC dropped, drift, retrain."
- Strong: "The drop is real, but segment AUCs are flat and cross-border tripled its share, so I would fix the evaluation view and watch cross-border separately before touching the model."

**Code:**
```python
# Q1 fraud AUC 0.86 -> 0.79: is the drop noise, a mix shift, or real decay? (illustrative numbers)
import numpy as np
from scipy.stats import rankdata, norm

def auc(y, s):
    r = rankdata(s)
    n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)

def hanley_se(a, n1, n0):
    q1 = a / (2 - a); q2 = 2 * a * a / (1 + a)
    v = (a * (1 - a) + (n1 - 1) * (q1 - a * a) + (n0 - 1) * (q2 - a * a)) / (n1 * n0)
    return v ** 0.5

# Step 1: is a 0.07 drop on 30,000 rows just noise? Assume 2% fraud -> 600 positives.
n, pos = 30_000, 600
se = hanley_se(0.79, pos, n - pos)
print(f"SE of AUC 0.79 with {pos} positives: {se:.4f}; 95% CI [{0.79-1.96*se:.3f}, {0.79+1.96*se:.3f}]")
assert 0.010 < se < 0.014
assert 0.79 + 1.96 * se < 0.86          # 0.86 is far outside the interval

# Step 2: a pure mix shift. Two segments with FIXED within-segment quality.
rng = np.random.default_rng(7)
def seg(n_rows, rate, d):                # binormal: positives shifted by d; AUC = Phi(d/sqrt2)
    y = (rng.random(n_rows) < rate).astype(int)
    s = rng.normal(size=n_rows) + d * y
    return y, s
d_dom, d_xb = norm.ppf(0.92) * 2**0.5, norm.ppf(0.68) * 2**0.5     # segment AUCs 0.92 and 0.68
def pooled(share_xb, total=400_000):
    nx = int(total * share_xb); nd = total - nx
    y1, s1 = seg(nd, 0.01, d_dom); y2, s2 = seg(nx, 0.04, d_xb)
    return (auc(y1, s1), auc(y2, s2),
            auc(np.r_[y1, y2], np.r_[s1, s2]))
res = {}
for label, share in [("launch mix (10% cross-border)", 0.10), ("now (30% cross-border)", 0.30)]:
    res[share] = pooled(share)
    a1, a2, ap = res[share]
    print(f"{label:30s} domestic {a1:.3f}  cross-border {a2:.3f}  pooled {ap:.3f}")
drop = res[0.10][2] - res[0.30][2]
print(f"pooled AUC drop from mix alone: {drop:.3f}")
assert 0.05 < drop < 0.10               # same size as the reported 0.07 drop, with no model change
# Segment AUCs did not move, only the mix did, so the model is not the first suspect
assert abs(res[0.10][0] - res[0.30][0]) < 0.01 and abs(res[0.10][1] - res[0.30][1]) < 0.02
```

**Output (my run):**
```text
SE of AUC 0.79 with 600 positives: 0.0111; 95% CI [0.768, 0.812]
launch mix (10% cross-border)  domestic 0.923  cross-border 0.677  pooled 0.846
now (30% cross-border)         domestic 0.923  cross-border 0.677  pooled 0.769
pooled AUC drop from mix alone: 0.077
```

**Follow-ups:**
- What if segment AUCs also dropped? Then it is real within-segment decay: check features and labels, then concept drift or adversaries, then retrain on recent data with a time-split validation.
- What if the interval had included 0.86? Then wait for more labels; do not act on noise.

**Common mistakes:** Retraining before checking labels and pipeline. Quoting AUC with no interval. Comparing different label definitions. Ignoring mix shift. Treating "no code change" as "no change".

### Q2 ⭐⭐⭐ 🟢 A churn model flagged the top 5% of customers with 40% precision at launch, and three months later the same top 5% has 31% precision on newly matured outcomes. The retention team asks whether the model is broken. Explain what you would look at to separate a genuinely worse model from a change in who is being scored or how outcomes are recorded.
**Asked at:** Production-degradation question banks (Dataford pages such as 'if a model's performance drops in production, what is your step-by-step diagnostic process', a Prepfully 'diagnose and fix a model deployed to production that underperformed' answer page, a TryExponent production-ML course page); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Precision at the top 5% equals lift times the base churn rate, so a fall from 40% to 31% could be a weaker ranking, a lower base rate, or the retention team saving the people the model flagged; I separate those three before saying the model is broken.

**Clarifying questions:**
- Did the retention team contact the flagged customers? If yes, precision falls when the campaign works, which is a success, not a failure.
- Has the definition of churn, or the observation window, changed? Different outcome recording moves precision with no model change.
- Did the scored population change (new acquisition channel, new plan, a price change)? It changes both base rate and lift.
- How many customers were scored, and are the three months of outcomes fully matured? It sets the noise.
- Is the top 5% still a fixed share, or a fixed score cut-off? The two behave differently when the score distribution moves.

**Approach:**
1. Compute the base churn rate now versus launch. Precision at top-k is lift times base rate, so report both.
2. Compute lift (precision at top 5% divided by base rate). If lift is stable, the ranking is not worse; the base rate moved.
3. Check treatment. Split flagged customers into contacted and not contacted (or use a held-out group). If untreated flagged customers still have about 40% precision, the model ranks fine and the campaign changed outcomes.
4. Check the outcome definition and recording: churn window, late-recorded cancellations, status codes, a billing change.
5. Check population mix: scored-customer segments, tenure, plan; recompute precision within segments (same idea as Q1).
6. Add a noise check: interval on 31% with the flagged count.
7. Then decide: nothing, change the evaluation to hold out a no-contact control, or retrain if within-segment lift really fell.

**Metrics:**
- Precision at top 5% = churners among flagged / flagged customers.
- Base rate = churners / all scored customers. Lift = precision / base rate.
- Recall at top 5% = churners among flagged / all churners (shows how much churn the flag set covers).
- Guardrails: contacted share, outcome-window definition, scored population size, label maturity.

**Risks:**
- Reading a fall in precision as model decay when the intervention is working. Treated customers should churn less.
- Comparing launch precision (no campaign) with now (campaign running): not like with like.
- A shorter outcome window now, so fewer churns have been recorded.
- Evaluating on contacted customers only, which mixes model quality with campaign effect.

**What the interviewer scores:**
- Strong: writes precision as lift times base rate and tests each piece. Weak: "the model drifted, retrain".
- Strong: names the intervention effect (performativity) unprompted. Weak: treats outcomes as untouched by the campaign.
- Strong: proposes a holdout or untreated comparison. Weak: relies on the same contaminated precision.
- Strong: gives a noise estimate. Weak: reacts to a point change.

**Example:** (illustrative numbers) 100,000 customers, 5,000 flagged. At launch the base rate was 10% and top-5% precision 40%, a lift of 4.0x. Now precision is 31%, with a 95% interval of about 29.7% to 32.3% (standard error 0.65 points), so the fall is real. Three readings give the same 31%: (A) the base rate fell to 7.75% with lift still 4.0x; (B) the base rate is 10% and lift fell to 3.1x; (C) the team saved 22.5% of would-be churners among the flagged. In my simulation, 60% of flagged customers were contacted: precision was 25.8% in the contacted group and 42.9% in the untouched group, so the ranking is fine and the campaign worked.
- Weak: "Precision fell 9 points, the model is broken."
- Strong: "Precision is lift times base rate. I will check the base rate, the lift, and the untreated flagged group before I call it a model problem."

**Code:**
```python
# Q2 churn model: top-5% precision 40% -> 31% (illustrative numbers)
import numpy as np
rng = np.random.default_rng(11)

# Identity: precision at top-k = lift x base churn rate
base0, prec0 = 0.10, 0.40
lift0 = prec0 / base0
print(f"launch: base rate {base0:.1%}, top-5% precision {prec0:.0%}, lift {lift0:.1f}x")
assert round(lift0, 2) == 4.0

# Reading A: ranking unchanged (lift stays 4x), the base rate fell
base1 = 0.0775
print(f"A) same lift 4.0x, base rate {base1:.2%} -> precision {lift0*base1:.1%}")
assert round(lift0 * base1, 3) == 0.31
# Reading B: base rate unchanged, ranking got worse
lift1 = 0.31 / base0
print(f"B) same base {base0:.0%}, precision 31% -> lift {lift1:.1f}x (ranking weaker)")
assert round(lift1, 2) == 3.1

# Reading C: the retention team contacted flagged customers and saved some
save_rate = 1 - 0.31 / 0.40
print(f"C) precision falls to 31% if {save_rate:.1%} of would-be churners are saved")
assert round(save_rate, 3) == 0.225

# Noise check: 100,000 customers scored -> 5,000 flagged
n_flag = 5_000
se = (0.31 * 0.69 / n_flag) ** 0.5
print(f"standard error of 31% on {n_flag} flagged: {se*100:.2f} pts; 95% CI [{(0.31-1.96*se)*100:.1f}, {(0.31+1.96*se)*100:.1f}]")
assert 0.006 < se < 0.007 and 0.31 + 1.96 * se < 0.40

# A check that separates A from B without labels shifting: precision among UNTREATED flagged customers
treated = rng.random(n_flag) < 0.6
true_p = np.where(treated, 0.40 * (1 - 0.375), 0.40)          # invented: saves only work in the treated group
churn = rng.random(n_flag) < true_p
p_t, p_u = churn[treated].mean(), churn[~treated].mean()
print(f"treated flagged precision {p_t:.1%}, untreated flagged precision {p_u:.1%}")
assert p_u > p_t + 0.05                  # holdback shows the model ranking is fine; the campaign changes outcomes
mix = 0.6 * 0.40 * (1 - 0.375) + 0.4 * 0.40
print(f"expected blended precision {mix:.1%}")
assert round(mix, 3) == 0.31
```

**Output (my run):**
```text
launch: base rate 10.0%, top-5% precision 40%, lift 4.0x
A) same lift 4.0x, base rate 7.75% -> precision 31.0%
B) same base 10%, precision 31% -> lift 3.1x (ranking weaker)
C) precision falls to 31% if 22.5% of would-be churners are saved
standard error of 31% on 5000 flagged: 0.65 pts; 95% CI [29.7, 32.3]
treated flagged precision 25.8%, untreated flagged precision 42.9%
expected blended precision 31.0%
```

**Follow-ups:**
- How do you keep measuring the model if retention keeps working? Keep a small random no-contact control (say 5% of flagged) so you can always see untreated precision.
- Would you change the metric? Consider uplift or "saved revenue", since the goal is changed behaviour, not predicting churn. Book 1 Part 11 Q8 (Design a customer churn prediction and retention system) covers the design.

**Common mistakes:** Not splitting precision into base rate and lift. Ignoring the intervention. Not checking the outcome window. Judging on contacted customers only.

### Q3 ⭐⭐⭐ 🟢 A ranking model scored an offline AUC of 0.91 and was approved, but the live A/B test shows no lift in conversion. Your manager asks what could explain a model that is excellent offline and flat online. List the causes you would investigate and the order in which you would test them.
**Asked at:** Training-serving skew and offline-versus-online question pages (DesignGurus 'Grokking the AI System Design Interview', techinterview.org MLOps drift and feature-store guide, a Prachub ML-serving concept page); commonly reported in public guides; search snippets only, not opened
**Say this first (1 line):** An offline AUC only says the model separates labelled examples in old data; I would first check whether the A/B test could even see a lift, then whether the offline number was inflated by leakage or bias, and only then question the model.

**Clarifying questions:**
- How many users per arm, for how long, and what lift did the test plan to detect? It tells me if "no lift" means "no effect" or "not enough power".
- What was the offline label (click, purchase, a human rating) and how was the validation split made? A random split of logs, or labels created by the old ranker, inflate AUC.
- Which features are in the model, and are they all available at serving time? Leakage and skew are the top suspects for a too-good offline number.
- What does the ranker change on the page (top 3 only, whole list)? AUC counts all pairs; conversion depends on the top few positions.
- Was the arm split checked for sample ratio mismatch and were both arms logged the same way?

**Approach (in the order I test, cheapest and most likely first):**
1. Test validity: SRM check, same logging in both arms, the right model really served, no bug in the experiment setup.
2. Power: minimum detectable effect for the sample. If the test could only see an 8% lift and the realistic gain is 2%, "flat" is expected.
3. Training-serving skew and leakage: compare online feature values and score distributions with offline; look for any feature built from information not available at decision time. See Book 4 Part 8 Q7 (training-serving skew) and Book 1 Part 11 Q18 (prevent data leakage when building training data).
4. Metric mismatch: AUC is a pairwise whole-list metric; compute NDCG@k, precision at the top positions, and the offline gain over the incumbent, not over random.
5. Label and selection bias: the training labels came from what the old ranker showed (position bias), so the model learns the old ranker. Book 1 Part 11 Q49 (correct position bias and evaluate a ranker offline using logged data) covers fixes.
6. Ceiling and funnel: maybe conversion depends little on ranking (price, delivery time, stock) so even a perfect ranking moves little.
7. Time effects: novelty, seasonality or a campaign overlapping the test.

**Metrics:**
- Primary online metric (conversion = orders / sessions) with confidence interval; guardrails (latency, revenue per session).
- Offline: AUC, NDCG@k, and gain versus the incumbent on the same data.
- Power quantities: baseline rate, per-arm sample, minimum detectable relative lift.
- Health: SRM chi-square, feature-parity check (offline versus online values for the same rows).

**Risks:**
- Declaring the model bad when the test was underpowered.
- Shipping on a leaky offline number.
- Re-running the test until something is significant.
- Fixing the model while the real problem is the experiment setup.

**What the interviewer scores:**
- Strong: starts with test validity and power, then leakage and skew. Weak: jumps to "overfitting".
- Strong: orders causes by cost to test and likelihood. Weak: unordered list.
- Strong: knows AUC is not a top-k or revenue metric. Weak: treats AUC as business value.
- Strong: puts numbers on power. Weak: says "need more data".

**Example:** (illustrative numbers) Baseline conversion is 4%, 50,000 users per arm. A realistic gain is 2% relative (4.00% to 4.08%). Power to detect that is only about 9%; the test could only reliably see a lift of about 8.7% relative; 80% power at +2% needs about 942,000 users per arm. In my simulation a feature known only after the click (like dwell time) lifts AUC from 0.695 to 0.925, so a 0.91-style number is easy to get from leakage while the online model, without that feature, is far weaker. A split of 50,000 versus 50,900 gives a chi-square of 8.03, above the 3.84 cut-off, which would flag a sample ratio problem.
- Weak: "AUC is 0.91, so the A/B test must be wrong or the model overfit."
- Strong: "First: was it powered, was the split clean, and were all offline features available online? Only then the model."

**Code:**
```python
# Q3 offline AUC 0.91 but flat online conversion (illustrative numbers)
import numpy as np
from scipy.stats import rankdata, norm
rng = np.random.default_rng(3)

def auc(y, s):
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)

# (1) Leakage: a feature that is only known after the click lifts offline AUC but is missing online
n = 200_000
true_signal = rng.normal(size=n)
y = (rng.random(n) < 1 / (1 + np.exp(-(true_signal * 1.1 - 3)))).astype(int)
leak = y * 2.5 + rng.normal(size=n)                 # e.g. 'dwell time after click'
honest = true_signal + rng.normal(scale=1.0, size=n)
auc_honest = auc(y, honest)
auc_leaky = auc(y, honest + leak)
print(f"AUC without leak {auc_honest:.3f}; with post-click feature {auc_leaky:.3f}")
assert auc_leaky - auc_honest > 0.10
assert 0.90 < auc_leaky < 0.97

# (2) Power: could this A/B test even see a lift?
base = 0.04                                       # 4% conversion
n_arm = 50_000
rel = 0.02                                       # a 2% relative lift
d = base * rel
se = (2 * base * (1 - base) / n_arm) ** 0.5
power = 1 - norm.cdf(1.96 - d / se)
print(f"power to detect +2% relative with {n_arm} users/arm: {power:.2f}")
assert power < 0.15
# users per arm for 80% power
need = 2 * (1.96 + 0.8416) ** 2 * base * (1 - base) / d ** 2
print(f"users per arm for 80% power at +2% relative: {int(np.ceil(need)):,}")
assert 900_000 < need < 1_000_000
# smallest relative lift that 50,000/arm can detect at 80% power
mde = (1.96 + 0.8416) * se / base
print(f"minimum detectable relative lift at 50,000/arm: {mde:.1%}")
assert 0.08 < mde < 0.09

# (3) SRM check: does the split look like 50/50?
a, b = 50_000, 50_900
chi = (a - (a + b) / 2) ** 2 / ((a + b) / 2) + (b - (a + b) / 2) ** 2 / ((a + b) / 2)
print(f"SRM chi-square for {a} vs {b}: {chi:.2f} (3.84 is the 5% cut-off for 1 df)")
assert 8 < chi < 10
```

**Output (my run):**
```text
AUC without leak 0.695; with post-click feature 0.925
power to detect +2% relative with 50000 users/arm: 0.09
users per arm for 80% power at +2% relative: 941,876
minimum detectable relative lift at 50,000/arm: 8.7%
SRM chi-square for 50000 vs 50900: 8.03 (3.84 is the 5% cut-off for 1 df)
```

**Follow-ups:**
- The test was underpowered; what now? Run longer or on more traffic, use a variance-reduction method such as CUPED, or test on a more sensitive metric first. Book 1 Part 10 owns the experiment theory.
- How do you prevent this next time? Add an offline replay on logged exposures, a feature-parity test, and an expected-lift and power calculation before launch.

**Common mistakes:** Believing offline AUC is business value. Ignoring power. Not checking SRM. Not asking which features exist at serving time. Blaming the experiment before checking the model's inputs, or the reverse.

### Q4 ⭐⭐⭐ 🟡 A card-fraud model launched two weeks ago, and chargeback labels arrive 45 to 60 days after each transaction, so no true label exists yet for anything it has scored. The approval rate and average score look normal on the dashboard. Explain how you would monitor whether the model is degrading during these first weeks, and what each signal can and cannot tell you.
**Asked at:** Drift and monitoring-without-labels guides (techinterview.org MLOps guides, a DataDome write-up on monitoring models without labels, KodeKloud and NannyML-style material); commonly reported in public guides for MLOps and ML-system-design loops; search snippets only, not opened
**Say this first (1 line):** With no labels for 45 to 60 days I monitor in three layers, inputs, scores and fast proxy outcomes, plus a partial-label check as the first cohorts mature; each layer can raise a flag but none can prove accuracy.

**Clarifying questions:**
- What is the fastest partial signal we have (analyst confirmation, customer dispute, card block, review queue outcome)? It becomes my proxy label.
- Is there a human review queue or a rule layer, and do they create labels sooner for a flagged subset? That subset is biased but useful.
- What did the offline score distribution look like at launch? I need a reference to compare with.
- What is the cost of an undetected week (loss per day)? It sets how strict the alert thresholds are.
- Which segments matter most (cross-border, new cards)? Averages hide them, see Q8.

**Approach:**
1. Freeze a reference: the validation or first-week score and feature distributions, per segment.
2. Input checks daily: null rate, range, category levels, feature PSI. Catches pipeline breaks. Book 4 Part 8 Q3 (Population Stability Index from scratch) covers PSI.
3. Output checks daily: score distribution (PSI and quantiles, not only the mean), flag rate at the decision threshold, per-segment flag rate.
4. Fast proxy outcomes: analyst-confirmed share among flagged cases, dispute rate within 3 to 7 days, customer-reported fraud. Track as a time series with intervals.
5. Partial labels: as cohorts mature, score the early-matured slice. Early chargebacks are biased toward quick ones, so say so.
6. Escalation: a rule table: which alert is a page, which is a ticket. Keep a rollback path to the previous model or rules.
7. Book 4 Part 8 Q8 (monitoring performance when labels arrive late or never) covers the tooling side.

**Metrics:**
- Score PSI = sum over bins of (current share minus reference share) times ln(current share / reference share), using reference quantile bins.
- Flag rate = flagged transactions / scored transactions, per segment.
- Proxy precision = analyst-confirmed frauds / flagged cases reviewed.
- Label maturity = share of a cohort whose label has arrived at age t.
- Guardrails: alert volume, review queue load, false-decline complaints.

**Risks:**
- The mean score and approval rate can stay put while the shape of the distribution changes.
- A proxy label is biased (only reviewed or fast cases), so it can move without the model moving.
- Alert fatigue from PSI on large samples; use effect size and persistence.
- Fraud mix changes mean fewer frauds are caught without any distribution alarm.

**What the interviewer scores:**
- Strong: states what each signal cannot tell. Weak: "monitor drift" and stop.
- Strong: uses distributions and proxy outcomes. Weak: only watches average score and approval rate.
- Strong: computes when real labels become available. Weak: ignores the 45 to 60 day wait.
- Strong: has a response plan for an alert. Weak: monitoring with no action.

**Example:** (illustrative numbers) The reference scores have a mean of 0.100. A week later the mean is still 0.100 and the share of transactions under a 0.40 score is 99.92% versus 99.80%, which looks normal. But the score distribution split into two clumps and its PSI is 0.618, well above the common 0.25 alert level. Label timing with a 45 to 60 day delay: 0% of a cohort has labels at age 14 or 30 days, 6% at 45, 38% at 50 and 100% at 60. The first fully labelled week of launch traffic arrives around day 66. A fast proxy helps: analyst-confirmed share among 2,000 flagged cases was 61.3% in the launch week and 44.5% in week 3, each with a standard error of about 1.1 points, so the fall is far outside noise.
- Weak: "Approval rate and mean score are normal, so the model is fine."
- Strong: "Means can hide shape changes. I watch the full score distribution, the flag rate by segment and a fast proxy precision, and I tell the business that real accuracy is unknown until about day 66."

**Code:**
```python
# Q4 monitoring a fraud model with no labels for 45-60 days (illustrative numbers)
import numpy as np
rng = np.random.default_rng(4)

def psi(ref, cur, bins=10):
    edges = np.quantile(ref, np.linspace(0, 1, bins + 1)); edges[0], edges[-1] = -np.inf, np.inf
    r = np.histogram(ref, edges)[0] / len(ref); c = np.histogram(cur, edges)[0] / len(cur)
    r = np.clip(r, 1e-4, None); c = np.clip(c, 1e-4, None)
    return float(np.sum((c - r) * np.log(c / r)))

# Reference: week-1 scores. Current: same MEAN score, but spread into two clumps.
ref = rng.beta(2, 18, 100_000)                      # mean ~0.10
ref_mean = ref.mean()
cur = np.where(rng.random(100_000) < 0.5, rng.beta(1.5, 40, 100_000), rng.beta(4, 12, 100_000))
cur = cur * (ref_mean / cur.mean())                # force same mean
thr = 0.40
print(f"mean score ref {ref.mean():.3f} vs now {cur.mean():.3f}")
print(f"approval rate (score < {thr}) ref {(ref<thr).mean():.2%} vs now {(cur<thr).mean():.2%}")
p = psi(ref, cur)
print(f"score PSI = {p:.3f}")
assert abs(ref.mean() - cur.mean()) < 0.002          # dashboard mean looks normal
assert abs((ref < thr).mean() - (cur < thr).mean()) < 0.01   # approval rate looks normal
assert p > 0.25                                       # the distribution test still sees it

# Label maturity: chargeback delay uniform 45-60 days after the transaction
delay = rng.integers(45, 61, 200_000)
for age in [14, 30, 45, 50, 60]:
    print(f"fraction of a cohort labelled at age {age:>2} days: {(delay <= age).mean():.2f}")
assert (delay <= 44).sum() == 0 and (delay <= 60).mean() == 1.0
# a week of launch traffic (days 0-6) is fully labelled only after day 6 + 60
print("first fully labelled week of traffic: day", 6 + 60)

# Fast proxy: share of flagged transactions confirmed as fraud by an analyst within 3 days
flagged = 2_000
for confirm_rate, name in [(0.60, "launch week"), (0.45, "week 3")]:
    k = rng.binomial(flagged, confirm_rate)
    se = (confirm_rate * (1 - confirm_rate) / flagged) ** 0.5
    print(f"{name}: confirmed {k}/{flagged} = {k/flagged:.1%} (SE {se*100:.1f} pts)")
assert (0.60 - 0.45) / ((0.6*0.4/2000 + 0.45*0.55/2000) ** 0.5) > 8   # a 15-pt fall is far outside noise
```

**Output (my run):**
```text
mean score ref 0.100 vs now 0.100
approval rate (score < 0.4) ref 99.92% vs now 99.80%
score PSI = 0.618
fraction of a cohort labelled at age 14 days: 0.00
fraction of a cohort labelled at age 30 days: 0.00
fraction of a cohort labelled at age 45 days: 0.06
fraction of a cohort labelled at age 50 days: 0.38
fraction of a cohort labelled at age 60 days: 1.00
first fully labelled week of traffic: day 66
launch week: confirmed 1226/2000 = 61.3% (SE 1.1 pts)
week 3: confirmed 890/2000 = 44.5% (SE 1.1 pts)
```

**Follow-ups:**
- What would make you roll back before labels arrive? A pipeline break, a PSI jump with a proxy-precision fall, or a segment spike in complaints; the rule is agreed before launch.
- Can you estimate performance without labels at all? Only under strong assumptions (for example, no concept change); treat it as a hint, not evidence.

**Common mistakes:** Watching only the mean score and approval rate. Treating PSI as accuracy. Ignoring label timing. Using a biased proxy as if it were ground truth. No agreed rollback rule.

### Q5 ⭐⭐⭐ 🟡 After an upstream deploy, the merchant_category feature's null rate jumped from 0.5% to 18% overnight, and a labelled check shows AUC falling from 0.88 to 0.84. The model still returns scores without errors. Explain how you would confirm the cause, what immediate action you would take, and how you would stop this class of failure going unnoticed again.
**Asked at:** Upstream schema and silent feature-pipeline failure write-ups (Towards AI schema-migration post, RisingWave feature-pipeline observability, ActiveWizards Kafka schema-evolution post, dataexpert.io schema-drift post); practitioner posts rather than interview banks, so scenario is editor-designed; search snippets only, not opened
**Say this first (1 line):** Confirm the null jump caused the AUC fall by slicing performance on null versus non-null rows and replaying with the feature restored, then fix it at the source or fall back immediately, and add null-rate and contract alerts so it cannot go silent again.

**Clarifying questions:**
- When exactly did the null rate jump, and does it line up with the upstream deploy time? Timing is the first piece of evidence.
- How does the model treat a null (default fill, a missing-value branch, an imputed mean)? It decides how bad the scores get.
- Are the nulls spread evenly or concentrated (one merchant type, one channel, one region)? Concentration explains a bigger AUC fall.
- Can the true value be recovered (source table, lookup by merchant ID)? If so, I can backfill and replay.
- Is there a previous model or rule set to fall back to, and who owns the upstream pipeline?

**Approach:**
1. Contain first: page the upstream owner, and check whether the deploy can be rolled back. If not, switch on a fallback: a lookup-based fill from the merchant table, or a model version that does not need the feature.
2. Confirm cause with evidence: null timing versus deploy timing; AUC on null rows versus non-null rows; replay the affected window with the feature restored and see AUC recover.
3. Check for other changes in the same deploy: other features, category levels, types. One bug often has neighbours.
4. Fix: restore the upstream field, or (if the model must run) a documented imputation chosen with a validation check, not a silent default.
5. Repair history: mark the bad window in logs; exclude or fix those rows before the next retrain (see Q16).
6. Prevent: a data contract with null-rate and range checks at the feature pipeline, a monitor with a statistical threshold, and a deploy checklist that tests downstream models.

**Metrics:**
- Null rate = null merchant_category rows / total scored rows, per hour and per segment.
- AUC on null rows and on non-null rows separately; overall AUC; replay AUC with restored value.
- Alert threshold for the null rate: baseline plus three standard errors for the batch size, plus an absolute cap.
- Guardrails: scoring volume, latency, default-path share, number of rows scored with fallback.

**Risks:**
- Retraining on the broken window teaches the model to treat "null" as a normal level.
- Mean-imputing hides the problem but gives weak scores on exactly the affected rows.
- Fixing one field and missing a type or category-level change in the same deploy.
- Alert threshold set too wide, so a slow climb passes.

**What the interviewer scores:**
- Strong: separates contain, confirm, fix and prevent. Weak: "retrain the model".
- Strong: slices on null versus non-null and replays with the true value. Weak: assumes the cause from timing alone.
- Strong: gives a threshold with arithmetic. Weak: "set an alert on nulls".
- Strong: protects the next retrain. Weak: forgets the training data is now dirty.

**Example:** (illustrative numbers) In my simulation, with 0.5% nulls the AUC is 0.862, and with 18% nulls it is 0.835. The loss sits in the null rows: AUC is 0.709 on null rows and 0.862 on non-null rows. Replaying with the true feature value restores 0.862, which confirms the cause. An hourly batch of 10,000 rows with a 0.5% baseline has a three-sigma upper bound of 0.71%, so a day-one alert would fire at 18%, which is 25 times that bound. (The prompt's fall of 0.88 to 0.84 is larger than my 0.027; a bigger drop means the nulls hit a more important segment.)
- Weak: "Retrain with the new data."
- Strong: "The AUC loss lives in the null rows. I would restore the field or fall back to a lookup today, replay to confirm, and add a null-rate alert with a data contract."

**Code:**
```python
# Q5 null-rate jump in merchant_category: confirm the cause (illustrative numbers)
import numpy as np
from scipy.stats import rankdata
rng = np.random.default_rng(5)

def auc(y, s):
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)

n = 300_000
mcc_risk = rng.normal(size=n)                    # merchant-category risk (known to the model)
other = rng.normal(size=n)                       # everything else the model uses
logit = -3.2 + 1.5 * mcc_risk + 1.0 * other
y = (rng.random(n) < 1 / (1 + np.exp(-logit))).astype(int)
def score(m, o): return 1.5 * m + 1.0 * o        # the model's score (null filled by 0 = 'average')

def with_nulls(rate):
    is_null = rng.random(n) < rate
    m = np.where(is_null, 0.0, mcc_risk)         # default fill after the deploy
    return is_null, score(m, other)

res = {}
for rate in (0.005, 0.18):
    is_null, s = with_nulls(rate)
    res[rate] = (is_null, s, auc(y, s))
    print(f"null rate {rate:.1%}: AUC {res[rate][2]:.3f}")
is_null, s18, a18 = res[0.18]
a_null = auc(y[is_null], s18[is_null]); a_ok = auc(y[~is_null], s18[~is_null])
print(f"at 18% nulls: AUC on null rows {a_null:.3f}, on non-null rows {a_ok:.3f}")
assert 0.84 < res[0.005][2] < 0.89 and a18 < res[0.005][2] - 0.02
assert a_null < a_ok - 0.04                      # the damage sits in the null rows
# Confirm: replay the 18% nulls with the true value restored -> AUC recovers
s_fixed = score(mcc_risk, other)
print(f"replay with feature restored: AUC {auc(y, s_fixed):.3f}")
assert abs(auc(y, s_fixed) - res[0.005][2]) < 0.01
# Why a threshold alert catches it on day one: 3-sigma upper bound for an hourly batch
base, nh = 0.005, 10_000
ub = base + 3 * (base * (1 - base) / nh) ** 0.5
print(f"3-sigma null-rate bound for {nh:,} rows/hour: {ub:.2%}; 18% is {0.18/ub:.0f}x that")
assert 0.0069 < ub < 0.0072
```

**Output (my run):**
```text
null rate 0.5%: AUC 0.862
null rate 18.0%: AUC 0.835
at 18% nulls: AUC on null rows 0.709, on non-null rows 0.862
replay with feature restored: AUC 0.862
3-sigma null-rate bound for 10,000 rows/hour: 0.71%; 18% is 25x that
```

**Follow-ups:**
- When is a null a legitimate value? When the field is truly unknown for some customers; the model must be trained with that missingness pattern. A sudden change in pattern is the signal.
- Who owns the alert? The pipeline team owns the feature contract; the model team owns the model-impact check. See Book 4 Part 8 Q6 (data quality checks for an ML input table).

**Common mistakes:** Retraining before finding the cause. Imputing silently. Using only an overall null-rate alert with a loose threshold. Not checking neighbouring features. Keeping the bad window in the training data.

### Q6 ⭐⭐⭐ 🟡 A delivery-time model's mean predicted value rose from 28 to 41 minutes the day after a service release, while real delivery times did not change. The offline pipeline computes account_age in days and you suspect the service computes it differently. Explain how you would prove or disprove training-serving skew, and how you would fix it without retraining blindly.
**Asked at:** Training-serving skew and offline-versus-online question pages (DesignGurus 'Grokking the AI System Design Interview', techinterview.org MLOps drift and feature-store guide, a Prachub ML-serving concept page); commonly reported in public guides; search snippets only, not opened
**Say this first (1 line):** I prove skew with a parity test: log the exact feature values the service sent to the model, recompute them with the offline pipeline on the same rows, and compare; then I fix the service function and re-run the parity test, with no retraining.

**Clarifying questions:**
- Do we log the feature vector the service actually sent to the model, with the entity ID and timestamp? Without it I cannot do a row-level comparison.
- How does the offline pipeline define account_age (signup date versus first order, calendar days versus 24-hour blocks, which time zone)? The definition is the test target.
- Did only the mean prediction move, or the feature distribution too? If the account_age distribution moved at release time, the feature is the suspect.
- What else changed in the release (library versions, null handling, feature order)? Skew is often more than one field.
- Did real delivery times stay flat for all cities and hours? Confirms that the model, not the world, moved.

**Approach:**
1. Locate the break: compare the serving feature distributions before and after the release; account_age should jump.
2. Parity test: take 10,000 logged requests, recompute account_age offline for the same entity at the same timestamp, join, and compare row by row.
3. Read the pattern. A constant ratio (here 24) points to a unit change. A constant offset points to an off-by-one or time-zone issue. Random differences point to a different source column. A set of zeros points to a null default.
4. Show the effect: feed the offline value into the model and see whether the mean prediction returns to 28 minutes.
5. Fix the service computation (ideally the same shared function as training, or a feature store), then re-run the parity test until the maximum difference is zero.
6. Prevent: add a unit test with golden examples, a parity check in CI, and a feature-distribution alert. See Book 4 Part 8 Q7 (training-serving skew) and Book 1 Part 11 Q15 (What is training-serving skew and how do you prevent it).

**Metrics:**
- Ratio or difference = service value / offline value (or service minus offline) per row; report min, median, max.
- Mean prediction, before and after, versus mean real delivery time.
- Parity pass rate = rows where |service - offline| <= tolerance / rows compared.
- Guardrails: mean absolute error against real delivery times, prediction latency.

**Risks:**
- Retraining on the service-side feature teaches the model the wrong scale and bakes the bug in.
- Comparing aggregates only: two bugs can cancel in the mean.
- Logged features may themselves be post-processed; log the raw model input.
- Fixing one field and missing a null default or a category order issue.

**What the interviewer scores:**
- Strong: row-level parity test on logged features. Weak: "let me retrain and see".
- Strong: reads the ratio pattern to name the bug type. Weak: guesses.
- Strong: fix by sharing code and a test. Weak: patches only this feature by hand.
- Strong: also proves the alternative (the world changed) is false using real delivery times. Weak: ignores the real-time comparison.

**Example:** (illustrative numbers) The model uses 13.1 + 4.1 times ln(1 + account_age_days). Fed the offline day values, the mean prediction is 28.0 minutes. If the service computes age in hours, every age is 24 times larger, so the prediction rises by about 4.1 times ln(24), which is 13.0 minutes, and the mean becomes 40.9 minutes (observed shift 12.9). The parity test finds service/offline equal to 24.00 on every one of 49,998 rows with age above zero, which proves a unit bug. If the cause were noise, the ratio would spread (my simulated noise case spread from 0.80 to 1.20). After switching the service to days, the maximum absolute difference is 0 and the mean returns to 28.0.
- Weak: "Predictions moved, so retrain on the latest data."
- Strong: "A constant ratio of 24 on the same rows is a unit bug in the service. I fix the function, re-run parity, and no retraining is needed."

**Code:**
```python
# Q6 delivery-time model: prove or disprove training-serving skew on account_age (illustrative numbers)
import numpy as np
rng = np.random.default_rng(6)

n = 50_000
age_days = np.round(rng.lognormal(mean=3.6, sigma=1.0, size=n)).clip(0, 1500)   # offline: days
dist_km = rng.gamma(4, 1.0, size=n)

def model(age, dist):                          # the trained model: log-shaped in age
    return 13.1 + 4.1 * np.log1p(age)

pred_offline = model(age_days, dist_km)
print(f"mean prediction with offline feature (days): {pred_offline.mean():.1f} min")

# Hypothesis: the service computes account_age in HOURS
age_service = age_days * 24
pred_service = model(age_service, dist_km)
print(f"mean prediction with service feature (hours): {pred_service.mean():.1f} min")
assert 27.5 < pred_offline.mean() < 28.5 and 40.5 < pred_service.mean() < 41.5

# Parity test: join the logged service value with the offline value for the SAME rows
ratio = age_service / np.where(age_days == 0, np.nan, age_days)
r = ratio[~np.isnan(ratio)]
print(f"ratio service/offline on {len(r):,} rows: min {r.min():.2f} median {np.median(r):.2f} max {r.max():.2f}")
assert r.min() == r.max() == 24.0              # a constant ratio proves a unit bug

# If the cause were random noise instead, the ratio would not be constant:
noisy = age_days * rng.uniform(0.8, 1.2, n)
r2 = noisy[age_days > 0] / age_days[age_days > 0]
print(f"noise-case ratio spread: {r2.min():.2f} to {r2.max():.2f}")
assert r2.max() - r2.min() > 0.3

# Fix: change the service function to days (shared code), no retrain. Then re-run parity.
age_fixed = age_service / 24
pred_fixed = model(age_fixed, dist_km)
print(f"after fix: mean prediction {pred_fixed.mean():.1f} min, max abs diff vs offline {np.abs(pred_fixed - pred_offline).max():.1e}")
assert np.allclose(pred_fixed, pred_offline)

# Size of the shift explained by the unit: 4.1 * ln(24) minutes on every row with age > 0
shift = 4.1 * np.log(24)
print(f"expected mean shift from the unit alone: about {shift:.1f} min; observed {pred_service.mean() - pred_offline.mean():.1f} min")
assert abs((pred_service.mean() - pred_offline.mean()) - shift) < 1.0
```

**Output (my run):**
```text
mean prediction with offline feature (days): 28.0 min
mean prediction with service feature (hours): 40.9 min
ratio service/offline on 49,998 rows: min 24.00 median 24.00 max 24.00
noise-case ratio spread: 0.80 to 1.20
after fix: mean prediction 28.0 min, max abs diff vs offline 0.0e+00
expected mean shift from the unit alone: about 13.0 min; observed 12.9 min
```

**Follow-ups:**
- What if the ratio is not constant? Look at the column source and the null defaults; check a few rows by hand, then use the pattern of differences to decide.
- Could the unit be right in the service and wrong offline? Yes. Decide from the definition used in training, since the model learned that scale; if the offline code was wrong, the model must be retrained.

**Common mistakes:** Retraining before proving the cause. Comparing means only. Not logging the actual model input. Fixing the service without a regression test. Assuming that production code equals training code because both are "account_age".

### Q7 ⭐⭐⭐ 🟡 Model v2 went live five days ago and the headline business metric is down 4% versus the prior week, but the data distribution also shifted that same week because of a marketing campaign. Version v1 is still deployable. Explain how you would decide between rolling back, retraining and leaving v2 in place, and what evidence you would want inside 24 hours.
**Asked at:** No interview question page located for this exact scenario; practitioner fraud and retraining guides (a Firstsource fraud-model post, a datainterview.com 'when to retrain' course page) describe the retrain-versus-rollback and adaptive-fraud themes, so editor-designed; search snippets only, not opened
**Say this first (1 line):** A week-on-week fall confounded by a campaign cannot decide anything, so inside 24 hours I would get a like-for-like comparison of v1 and v2 on the same traffic, and keep rollback ready as the cheap default if the evidence turns out bad or unclear.

**Clarifying questions:**
- What is the business metric and how fast does it settle (same session, next day)? A metric that settles slowly cannot decide in 24 hours.
- Who did the campaign bring in, and can I tag those users? Segment tags let me standardise the mix.
- Was v2 tested before launch (shadow or A/B)? If it won there, the prior favours v2 and the campaign.
- What does a bad day cost, and what does rollback cost (a redeploy, retraining, lost features)? It sets how much risk I accept.
- Can I split live traffic between v1 and v2 now, and for how long?

**Approach:**
1. Do not trust the week-on-week number. Split the change into a mix effect (who arrived) and a model effect (what v2 did to the same kind of user).
2. Standardise: compare conversion within segments (organic versus campaign), then average at one fixed mix.
3. Get a direct comparison: route a share of traffic back to v1 (a switchback or a 50/50 split for 24 hours) and score both models on the same sessions; shadow-scoring v1 helps for diagnostics but cannot give the business metric.
4. Check pipeline health for v2: feature nulls, score distribution, latency, errors. A bug is a different decision from a weak model.
5. Decide with a rule agreed up front:
   - v2 equal or better within segments: leave it, explain the campaign effect.
   - v2 clearly worse within segments, or a bug: roll back to v1 now, investigate offline.
   - Unclear: keep a v1 holdback and gather more; retrain only if the drift (new campaign audience) is lasting and v1 also degrades there.
6. Retraining is a later step. It is slow and does not tell me whether v2 or v1 is better now.

**Metrics:**
- Overall conversion = conversions / sessions, split by segment.
- Standardised conversion = sum over segments of (fixed share times the segment's conversion).
- Mix effect = (v1 on new mix) / (last week) - 1; model effect = (v2 on new mix) / (v1 on new mix) - 1.
- Guardrails: revenue per session, latency, error rate, complaint volume, a segment-level view.

**Risks:**
- Rolling back because of a mix effect, and giving up a real improvement.
- Leaving v2 in place because of the campaign story, while it truly hurts.
- A 24-hour test that is too small: a small holdback cannot see a 3% change (see the sizing below).
- A novelty effect or a weekday pattern inside the 5 days.

**What the interviewer scores:**
- Strong: decomposes the change into mix and model effects. Weak: reacts to the -4%.
- Strong: designs a 24-hour like-for-like test and sizes it. Weak: "monitor for another week".
- Strong: states a decision rule and a rollback trigger. Weak: no decision.
- Strong: treats retrain as the slow option. Weak: starts with retrain.

**Example:** (illustrative numbers) Last week v1 converted 9.00% at an 80% organic and 20% campaign mix. This week v2 gives 8.63% (down 4.1%) with a 70/30 mix. If v1 had been serving this week's mix it would have given 8.50% (down 5.6%), so the mix explains more than the whole fall and v2's own effect is +1.6%. To see a 3% relative drop at an 8.6% rate you need about 184,552 sessions per arm. At 400,000 sessions a day, a 5% holdback on v1 takes 9.2 days, while a 50/50 split takes 0.9 days. So the 24-hour evidence is a 50/50 switchback, not a thin holdback.
- Weak: "Metric is down 4%, roll back."
- Strong: "Most of the 4% is the new audience. I would run a 24-hour 50/50 against v1 on the same traffic, and roll back only if v2 loses inside segments."

**Code:**
```python
# Q7 v2 live 5 days, metric -4% versus prior week, campaign shifted the mix (illustrative numbers)
import numpy as np
from scipy.stats import norm

# Segments: organic vs campaign-acquired users. Conversion rates per segment and model.
share_prev = {"organic": 0.80, "campaign": 0.20}
share_now = {"organic": 0.70, "campaign": 0.30}
conv_v1 = {"organic": 0.100, "campaign": 0.050}          # what v1 would achieve (known from past)
conv_v2 = {"organic": 0.1015, "campaign": 0.0510}        # v2 is slightly better inside each segment

def overall(share, conv): return sum(share[k] * conv[k] for k in share)
prev = overall(share_prev, conv_v1)
now = overall(share_now, conv_v2)
print(f"last week (v1, old mix): {prev:.4f}; this week (v2, new mix): {now:.4f}; change {now/prev-1:+.1%}")
assert abs(now / prev - 1 + 0.04) < 0.005   # about -4%

# Decompose into mix effect and model effect
mix_only = overall(share_now, conv_v1)                    # v1 on the new mix
print(f"v1 on the new mix would give {mix_only:.4f} ({mix_only/prev-1:+.1%})")
print(f"model effect of v2 on the new mix: {now/mix_only-1:+.1%}")
assert mix_only / prev - 1 < -0.05 and now / mix_only - 1 > 0.01

# Evidence in 24 hours: switch back test. How many sessions per arm to see a 3% relative drop?
p = now
d = 0.03 * p
n_arm = 2 * (1.96 + 0.8416) ** 2 * p * (1 - p) / d ** 2
print(f"sessions per arm to detect a 3% relative drop at p={p:.4f}: {int(np.ceil(n_arm)):,}")
daily = 400_000
for split in (0.05, 0.50):
    days = n_arm / (daily * split)
    print(f"  with {split:.0%} of {daily:,}/day on v1: {days:.1f} days")
assert (n_arm / (daily * 0.05)) > 5 and (n_arm / (daily * 0.5)) < 1.0
```

**Output (my run):**
```text
last week (v1, old mix): 0.0900; this week (v2, new mix): 0.0863; change -4.1%
v1 on the new mix would give 0.0850 (-5.6%)
model effect of v2 on the new mix: +1.6%
sessions per arm to detect a 3% relative drop at p=0.0863: 184,552
  with 5% of 400,000/day on v1: 9.2 days
  with 50% of 400,000/day on v1: 0.9 days
```

**Follow-ups:**
- What if you cannot split traffic? Use the pre-launch shadow or A/B result, a before and after comparison with segment standardisation, and a time-boxed rollback to v1 for one segment.
- When is rollback the right answer? When there is a pipeline bug, a guardrail breach, or a within-segment loss with a credible interval below zero. Book 4 Part 8 Q1 covers why models degrade, and Book 1 Part 11 Q34 (roll out a new model safely) covers the rollout.

**Common mistakes:** Comparing this week with last week when the audience changed. Starting a retrain without a decision on rollback. Splitting too little traffic to see a 3% effect. No pre-agreed trigger for rollback.

### Q8 ⭐⭐⭐ 🟡 A model's accuracy has been flat for a month: 89.6% overall, both before and after a change. Splitting by tenure shows existing users (80% of traffic) improved from 90% to 92% accuracy while new users (20% of traffic) fell from 88% to 80%. Explain why the aggregate hid this, what might cause the new-user drop, and how you would set up segment-level monitoring.
**Asked at:** Production-degradation question banks (Dataford pages such as 'if a model's performance drops in production, what is your step-by-step diagnostic process', a Prepfully 'diagnose and fix a model deployed to production that underperformed' answer page, a TryExponent production-ML course page); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** The aggregate is a traffic-weighted average, and a gain on the large group exactly offset a loss on the small group: 0.8 times 92% plus 0.2 times 80% is 89.6%, the same as 0.8 times 90% plus 0.2 times 88%.

**Clarifying questions:**
- What changed at the "change" (a model release, a new onboarding flow, a data source)? I need it to explain why the groups moved in opposite directions.
- Is tenure the label of the model's population or a feature? If tenure is a feature, new users may now be handled differently.
- Who are the new users now (a new channel, a campaign, another country)? The new-user group may itself have changed.
- What is the cost of an error for each group? A wrong decision on a new user may be much more expensive (churn or fraud at the start).
- Is the new-user share of traffic stable or growing? If it grows, the aggregate will start to fall even with no further change.

**Approach:**
1. Show the arithmetic: aggregate = sum of weight times group accuracy. Existing users add 1.6 points to accuracy (0.8 x 2) and new users subtract 1.6 (0.2 x 8). They cancel exactly.
2. Switch to error counts: existing-user errors fall from 8.0 to 6.4 points of traffic, new-user errors rise from 2.4 to 4.0.
3. Find the new-user cause. Candidates: cold-start (missing history features, nulls filled with defaults), a model change that leans on tenure features, a shift in the new-user population (different acquisition channel), a label problem (new-user labels come later or differently), a feature pipeline break that only affects accounts with no history.
4. Test each with data: new-user feature null rates, score distribution, accuracy by channel and signup cohort, a replay with the old model on the same new users.
5. Fix: a cold-start path (a separate model or rules for no-history users), fix the feature, or retrain with weight on new users.
6. Monitoring design: track accuracy per segment (tenure, channel, region, device) with a minimum sample size, plus a standardised metric at a fixed mix, plus alert on the worst slice, not only the average.

**Metrics:**
- Accuracy per segment = correct predictions in segment / predictions in segment, with interval.
- Contribution to the aggregate = segment share times (segment accuracy change).
- Standardised accuracy = accuracy computed at a fixed reference mix of segments.
- Guardrails: segment sizes, new-user share, a per-segment cost-weighted error.

**Risks:**
- Too many slices produce false alarms; control with minimum sample sizes, intervals and a limited, pre-chosen list of slices.
- Mix change hides or creates movement; a fixed-mix metric avoids it.
- Slicing on a variable that is itself a model input can look circular; still useful.
- Treating the flat aggregate as success and shipping.

**What the interviewer scores:**
- Strong: does the arithmetic in the interview and shows offsetting contributions. Weak: "Simpson's paradox" with no numbers.
- Strong: gives concrete cold-start hypotheses and tests. Weak: "it is drift".
- Strong: weights by cost and share. Weak: treats segments as equal.
- Strong: monitoring with sample-size rules. Weak: "add more dashboards".

**Example:** The prompt's own numbers work out exactly. Before: 0.8 x 90% + 0.2 x 88% = 89.6%. After: 0.8 x 92% + 0.2 x 80% = 89.6%. Errors in points of traffic: existing 8.0 to 6.4, new 2.4 to 4.0, total 10.4 both times. New-user error rate went from 12% to 20% (up 1.67 times). If the new-user share grows to 30% with no further change, the aggregate becomes 0.7 x 92% + 0.3 x 80% = 88.4%. With (illustrative) 400,000 scored cases a month, new users are 80,000 cases, the standard error of 80% is 0.14 points and an 8-point fall is a 57-sigma move, not noise.
- Weak: "Accuracy is flat, so nothing changed."
- Strong: "Flat because a 2-point gain on 80% of traffic cancels an 8-point loss on 20%. New-user errors went up by two thirds, and I would investigate the cold-start path today."

**Code:**
```python
# Q8 flat aggregate accuracy hides a new-user drop (numbers from the prompt)
w_old, w_new = 0.80, 0.20
before = (0.90, 0.88)       # existing, new
after = (0.92, 0.80)
agg_b = w_old * before[0] + w_new * before[1]
agg_a = w_old * after[0] + w_new * after[1]
print(f"aggregate before {agg_b:.3f}, after {agg_a:.3f}")
assert round(agg_b, 3) == 0.896 and round(agg_a, 3) == 0.896

# Errors as a share of all traffic (percentage points of traffic)
err_old_b, err_old_a = w_old * (1 - before[0]), w_old * (1 - after[0])
err_new_b, err_new_a = w_new * (1 - before[1]), w_new * (1 - after[1])
print(f"existing-user errors {err_old_b*100:.1f} -> {err_old_a*100:.1f} pts of traffic; new-user errors {err_new_b*100:.1f} -> {err_new_a*100:.1f} pts")
assert round(err_old_b * 100, 1) == 8.0 and round(err_old_a * 100, 1) == 6.4
assert round(err_new_b * 100, 1) == 2.4 and round(err_new_a * 100, 1) == 4.0
assert round((err_old_a + err_new_a) * 100, 1) == round((err_old_b + err_new_b) * 100, 1) == 10.4

# Error rate of new users rose by two thirds in relative terms even though the aggregate error is unchanged
print(f"new-user error rate: {1-before[1]:.0%} -> {1-after[1]:.0%} (x{(1-after[1])/(1-before[1]):.2f})")
assert abs((1 - after[1]) / (1 - before[1]) - 1.667) < 0.001

# If the new-user share grows, the aggregate falls even with no further change
for share in (0.20, 0.30, 0.40):
    agg = (1 - share) * after[0] + share * after[1]
    print(f"new-user share {share:.0%}: aggregate {agg:.3f}")
assert round(0.7 * 0.92 + 0.3 * 0.80, 3) == 0.884

# Is the 8-point drop noise? Say 400,000 scored cases a month -> 80,000 new-user cases
n_new = 80_000
se = (0.80 * 0.20 / n_new) ** 0.5
print(f"standard error of new-user accuracy: {se*100:.2f} pts, so 88% to 80% is a {(0.88-0.80)/se:.0f}-sigma move")
assert (0.88 - 0.80) / se > 50

# Monitoring rule: alert when a segment's lower confidence bound falls below its baseline floor
def seg_alert(acc, n, floor, z=1.96):
    se = (acc * (1 - acc) / n) ** 0.5
    return acc + z * se < floor          # even the upper bound is under the floor
print("new-user alert fires:", seg_alert(0.80, n_new, 0.86))
print("aggregate alert fires:", seg_alert(agg_a, 400_000, 0.88))
assert seg_alert(0.80, n_new, 0.86) and not seg_alert(agg_a, 400_000, 0.88)
```

**Output (my run):**
```text
aggregate before 0.896, after 0.896
existing-user errors 8.0 -> 6.4 pts of traffic; new-user errors 2.4 -> 4.0 pts
new-user error rate: 12% -> 20% (x1.67)
new-user share 20%: aggregate 0.896
new-user share 30%: aggregate 0.884
new-user share 40%: aggregate 0.872
standard error of new-user accuracy: 0.14 pts, so 88% to 80% is a 57-sigma move
new-user alert fires: True
aggregate alert fires: False
```

**Follow-ups:**
- Should the existing-user gain count? It is real, but the new-user loss may cost more per error and new users are the future base. Decide with cost and growth, not with the average.
- How many slices can you monitor? Limit to a few that matter by business or risk, require a minimum n, and use a rolling window. Book 4 Part 8 Q2 covers what to monitor in layers.

**Common mistakes:** Reporting only the aggregate. Slicing after the fact on dozens of columns. Ignoring segment share changes. Using no minimum sample size. Treating cold start as an edge case.

### Q9 ⭐⭐⭐ 🟡 A fraud team says precision at a fixed threshold fell from 67% to 50% and wants an emergency retrain. On a volume of 1,000,000 transactions the fraud rate fell from 1.6% to 0.8% over the same period, while recall (70%) and false-positive rate (about 0.56%) are unchanged. Explain what is actually happening, how you would check it, and whether a retrain or a threshold change is warranted.
**Asked at:** Calibration, prior-shift and threshold-review material (an arXiv paper on calibrating metrics under class-prior change, a futureagi model-versus-data-drift post, a fraud-score vendor page on reviewing thresholds); no interview page for the exact scenario, so editor-designed; search snippets only, not opened
**Say this first (1 line):** Precision depends on the fraud rate; recall and false-positive rate did not move, so the model is ranking exactly as before and precision fell only because there is half as much fraud to find; no emergency retrain.

**Clarifying questions:**
- Is the fall in fraud rate real or a labelling artefact (late chargebacks, a changed fraud definition)? If labels lag, the "fall" may be fake.
- Is recall measured on matured labels? Recall of 70% on immature labels can look fine for the wrong reason.
- Did a fraud-prevention action (a new rule, a merchant block, a seasonal lull) cause the drop? The cause decides if it lasts.
- What is the review capacity and the cost of a false positive versus a missed fraud? It decides if the threshold should move.
- Is the 67% to 50% measured at the same threshold, same population and same label window?

**Approach:**
1. Rebuild the confusion matrix from the stated rates: on 1,000,000 transactions, 1.6% fraud is 16,000 frauds. Recall 70% gives 11,200 caught. FPR 0.56% on 984,000 non-frauds gives 5,510 false positives. Precision = 11,200 / 16,710 = 67.0%.
2. Repeat at 0.8%: 8,000 frauds, 5,600 caught, 5,555 false positives, precision = 5,600 / 11,155 = 50.2%. The false positives hardly changed; the true positives halved.
3. Verify with the data: confirm the fraud rate drop with matured labels; confirm that recall and FPR are unchanged by segment and by week.
4. Decide on action: retrain is not warranted by a precision fall that the base rate fully explains. A threshold change is a business choice (cost and review capacity), not a model fix.
5. If the business wants 67% precision again, raise the threshold; compute what recall is lost (see the example) and compare expected cost.
6. Report precision alongside the fraud rate, and monitor recall, FPR and PR-AUC plus a prevalence-adjusted precision (precision at a fixed reference fraud rate).

**Metrics:**
- Precision = TP / (TP + FP) = recall x pi / (recall x pi + FPR x (1 - pi)), where pi is the fraud rate.
- Recall = TP / (TP + FN). FPR = FP / (FP + TN).
- Prevalence-adjusted precision: the same formula evaluated at a reference pi.
- Guardrails: alert volume per day, review workload, expected cost per 1,000,000 transactions.

**Risks:**
- Retraining on a quiet period can reduce recall on the next wave.
- Raising the threshold drops recall; if fraud rises again you are exposed.
- A recall figure measured on immature labels.
- Treating FPR as stable while review workload (FP count) is what the business feels.

**What the interviewer scores:**
- Strong: derives the 50% from the base rate with arithmetic. Weak: "model decay".
- Strong: separates ranking quality (recall, FPR) from precision. Weak: watches only precision.
- Strong: frames the threshold as a cost decision with numbers. Weak: retrains or ignores.
- Strong: asks if the fraud-rate fall is real. Weak: accepts it.

**Example:** (illustrative; numbers from the prompt) At a 1.6% fraud rate: 16,000 frauds, 11,200 caught, 5,510 false positives, precision 67.0% (the implied FPR is 0.5606%, matching "about 0.56%"). At 0.8%: 8,000 frauds, 5,600 caught, 5,555 false positives, precision 50.2%. To get 67% back at 0.8%, under an assumed equal-variance binormal score model calibrated to the 70% recall at 0.56% FPR, the FPR would have to fall to about 0.235% and recall would drop to about 59.3%: roughly 859 more frauds missed per million transactions. With an invented cost of Rs 4,000 per missed fraud and Rs 60 per review, expected cost rises from about Rs 9.93 million to Rs 13.17 million per million transactions, so keeping the threshold is cheaper under those costs.
- Weak: "Precision fell 17 points, retrain now."
- Strong: "Same recall, same false-positive rate, half the fraud, so precision falls to 50% by arithmetic. I would verify the fraud-rate drop, keep the threshold unless the review team cannot cope, and report precision at a fixed reference prevalence."

**Code:**
```python
# Q9 precision fell 67% -> 50% while recall and FPR are unchanged (numbers from the prompt)
from scipy.stats import norm
N = 1_000_000
recall, fpr = 0.70, 0.0056

def confusion(pi):
    pos = N * pi; neg = N - pos
    tp = recall * pos; fp = fpr * neg
    return pos, tp, fp, tp / (tp + fp)

for pi in (0.016, 0.008):
    pos, tp, fp, prec = confusion(pi)
    print(f"fraud rate {pi:.1%}: frauds {pos:,.0f}, TP {tp:,.0f}, FP {fp:,.0f}, flagged {tp+fp:,.0f}, precision {prec:.1%}")
p0 = confusion(0.016)[3]; p1 = confusion(0.008)[3]
assert round(p0 * 100) == 67 and round(p1 * 100) == 50

# Does 'about 0.56%' FPR match 67% precision exactly?
fpr_implied = recall * 0.016 * (1 - 0.67) / (0.67 * (1 - 0.016))
print(f"FPR implied by 67% precision: {fpr_implied:.4%}")
assert abs(fpr_implied - 0.0056) < 0.00005

# To get 67% precision back at the new fraud rate, the threshold must be stricter.
# Equal-variance binormal score model (assumption), calibrated so recall 70% at FPR 0.56%:
from scipy.optimize import brentq
thr0 = norm.ppf(1 - fpr)
mu = thr0 - norm.ppf(1 - recall)
print(f"binormal separation implied: {mu:.2f}")
def recall_at(f): return 1 - norm.cdf(norm.ppf(1 - f) - mu)
pi = 0.008
def prec_at(f): return recall_at(f) * pi / (recall_at(f) * pi + f * (1 - pi))
assert abs(recall_at(fpr) - 0.70) < 1e-9 and abs(prec_at(fpr) - p1) < 1e-9
fpr_need = brentq(lambda f: prec_at(f) - 0.67, 1e-5, 0.0056)
r_new = recall_at(fpr_need)
print(f"FPR needed for 67% precision at fraud rate 0.8%: {fpr_need:.3%}; recall then {r_new:.1%}")
assert 0.0023 < fpr_need < 0.0027 and 0.56 < r_new < 0.60
tp_lost = (0.70 - r_new) * N * pi
print(f"frauds missed extra per million transactions: {tp_lost:,.0f}")
assert 800 < tp_lost < 1000

# Cost view (invented): a missed fraud costs Rs 4,000, a review costs Rs 60
for name, f in (("current threshold", fpr), ("stricter threshold", fpr_need)):
    rec = recall_at(f)
    cost = (1 - rec) * N * pi * 4000 + f * N * (1 - pi) * 60
    print(f"{name}: expected cost Rs {cost:,.0f}")
```

**Output (my run):**
```text
fraud rate 1.6%: frauds 16,000, TP 11,200, FP 5,510, flagged 16,710, precision 67.0%
fraud rate 0.8%: frauds 8,000, TP 5,600, FP 5,555, flagged 11,155, precision 50.2%
FPR implied by 67% precision: 0.5606%
binormal separation implied: 3.06
FPR needed for 67% precision at fraud rate 0.8%: 0.235%; recall then 59.3%
frauds missed extra per million transactions: 859
current threshold: expected cost Rs 9,933,312
stricter threshold: expected cost Rs 13,174,157
```

**Follow-ups:**
- What if recall also fell? Then ranking quality or the population changed; look at features, segments and concept drift. Book 4 Part 8 Q1 (why ML models degrade) covers the types of drift.
- What is this kind of shift called? A prior (label) shift: P(fraud) changed while P(features given fraud) stayed. The ROC point is unchanged but precision is not.

**Common mistakes:** Quoting precision without the base rate. Retraining on a prevalence change. Comparing precision across weeks with different fraud rates. Moving the threshold without costing the lost recall.

### Q10 ⭐⭐⭐ 🟡 A loan-default model gets its true labels about 12 months after disbursal, and it has been live for six months. The business wants an early-warning system rather than waiting a year. Explain which signals you would build now, how you would use early repayment behaviour as a proxy, and how you would state your confidence honestly to risk leadership.
**Asked at:** Drift and monitoring-without-labels guides (techinterview.org MLOps guides, a DataDome write-up on monitoring models without labels, KodeKloud and NannyML-style material); commonly reported in public guides for MLOps and ML-system-design loops; search snippets only, not opened
**Say this first (1 line):** I would not wait for 12-month labels: I would compare each vintage with older vintages at the same loan age, use early delinquency as a proxy mapped to eventual default, and tell risk leadership a range with the assumptions that could break it.

**Clarifying questions:**
- How are loans repaid (monthly instalments, bullet) and when is "default" defined (for example 90 days past due)? It decides which early event is a usable proxy.
- Do we have older vintages with complete outcomes and their month-by-month repayment? They give the mapping from early behaviour to final default.
- What does the model feed (approve or decline, pricing, limits)? It sets the cost of being wrong.
- Has the applicant mix or policy changed since launch? Without it, I can only show the model's stability, not its accuracy.
- Who decides on action from the warning (credit policy, collections), and how fast must they react?

**Approach:**
1. Input and score monitoring now: score distribution and feature PSI by vintage, approval mix, applicant channels. Book 4 Part 8 Q8 (monitoring performance when labels arrive late or never) covers the layers.
2. Same-age comparison (vintage curves): compare the current vintage's cumulative default or 30-days-past-due rate at month 3, 6 with history at the same month, per score band.
3. Proxy labels: first-instalment default, 30 or 60 days past due, roll rates, partial payments, collection outcomes. Estimate from history how a proxy maps to the 12-month outcome.
4. Projection: use the share of eventual defaults that is visible by month 6 in history to project the 12-month rate, with an interval that includes both sampling noise and the uncertainty in that share.
5. Check rank ordering: do higher-risk score bands show higher early delinquency? Stable ordering means the model still ranks even if the level moves.
6. Communicate in levels: green (consistent with expectation), amber (outside the interval, investigate) and red (action). Revise as each month of data matures.
7. Plan the real validation: a full back-test at month 12 and a policy for model refresh.

**Metrics:**
- Cumulative default by month t = loans in default by month t / loans disbursed in the vintage.
- Visible share r = (defaults by month 6) / (defaults by month 12) in old vintages.
- Projected 12-month default = current default by month 6 / r.
- Predicted-to-projected ratio per score band; rank correlation of band versus early delinquency.
- Guardrails: size of each cell, vintage mix, approval-rate change.

**Risks:**
- The timing pattern may change (a recession makes defaults earlier), so r is not stable.
- Censoring: recent loans have had less time to default, so comparing them with old loans' final default is wrong.
- Selection: approved-only data (see Q13).
- Early delinquency can rise for operational reasons (collection capacity, payment-app outage).
- Overconfidence: an interval that includes only sampling noise.

**What the interviewer scores:**
- Strong: compares at the same loan age and handles censoring. Weak: compares month-6 default with month-12 history.
- Strong: builds proxies and maps them to the target using old data. Weak: "use the model scores as the truth".
- Strong: an honest interval with named assumptions. Weak: a single number or "can't know".
- Strong: communication in levels with actions. Weak: no decision path.

**Example:** (illustrative numbers) History: 40,000 loans, with 5.83% in default by month 12; 2.68% were already in default by month 6, so r = 0.46. The model predicted 6.0%. The current vintage of 25,000 loans shows 3.39% in default by month 6, which projects to 3.39% / 0.46, about 7.4%; the 95% bootstrap interval, carrying both the current sampling error and the history's uncertainty, is 6.8% to 8.0%, which excludes the model's 6.0%. Say it as: "About 7.4%, probably between 6.8% and 8.0%, if repayment timing matches history; if only 35% of defaults show by month 6 the projection becomes 9.7%, and if 55% it is 6.2%."
- Weak: "We have no labels yet, so we cannot say anything."
- Strong: "Same-age comparison and early delinquency say this vintage is running above the model's 6.0%, about 7.4% with a 6.8% to 8.0% range, assuming normal timing. I would put the timing assumption on the slide."

**Code:**
```python
# Q10 loan default: 12-month labels, live 6 months. Early-warning from repayment behaviour (illustrative numbers)
import numpy as np
rng = np.random.default_rng(10)

# Historical vintages (labels complete): default flag and month of default (1..12)
n_hist = 40_000
p12_hist = 0.060
default = rng.random(n_hist) < p12_hist
month_pmf = np.array([1, 3, 7, 11, 12, 12, 11, 10, 9, 8, 8, 8], float); month_pmf /= month_pmf.sum()
dmonth = np.where(default, rng.choice(np.arange(1, 13), n_hist, p=month_pmf), 99)

by6 = ((dmonth <= 6)).sum(); by12 = (dmonth <= 12).sum()
r = by6 / by12                                  # share of eventual 12-month defaults already visible by month 6
print(f"history: default by month 6 = {by6/n_hist:.2%}, by month 12 = {by12/n_hist:.2%}, visible share r = {r:.2f}")
assert 0.4 < r < 0.5

# Current vintage: only 6 months observed
n_now = 25_000
true_p12_now = 0.075                            # truth we cannot see (worse than the 6.0% history)
d6_now = rng.binomial(n_now, true_p12_now * r) / n_now
print(f"current vintage: default by month 6 = {d6_now:.2%} on {n_now:,} loans")

# Project to 12 months and carry BOTH uncertainties by bootstrap
B = 4000
proj = np.empty(B)
for b in range(B):
    d6 = rng.binomial(n_now, d6_now) / n_now                              # sampling noise now
    h = rng.integers(0, n_hist, n_hist)                                    # resample history
    rb = (dmonth[h] <= 6).sum() / max((dmonth[h] <= 12).sum(), 1)
    proj[b] = d6 / rb
lo, mid, hi = np.percentile(proj, [2.5, 50, 97.5])
print(f"projected 12-month default: {mid:.2%} (95% interval {lo:.2%} to {hi:.2%}); model's predicted: 6.00%")
assert lo < 0.075 < hi and lo > 0.06                 # the interval excludes the model's 6.0%

# What the interval does NOT cover: the assumption that the timing pattern r is unchanged
for r_alt in (0.35, 0.55):
    print(f"if the visible share were {r_alt:.2f} instead of {r:.2f}: projection {d6_now/r_alt:.2%}")
assert d6_now / 0.35 > d6_now / 0.55
```

**Output (my run):**
```text
history: default by month 6 = 2.68%, by month 12 = 5.83%, visible share r = 0.46
current vintage: default by month 6 = 3.39% on 25,000 loans
projected 12-month default: 7.38% (95% interval 6.80% to 8.00%); model's predicted: 6.00%
if the visible share were 0.35 instead of 0.46: projection 9.69%
if the visible share were 0.55 instead of 0.46: projection 6.17%
```

**Follow-ups:**
- Which signal first? Score and feature drift (day 1), first-instalment default (month 1), 30-days-past-due roll rates (month 2 to 4), then vintage curves.
- How do you state confidence? Give a range, name the assumption it rests on (timing and mix), and show a sensitivity (the 9.7% and 6.2% cases) so leadership sees the risk.

**Common mistakes:** Comparing immature vintages with mature ones. Using the model's own predictions as evidence of its accuracy. Reporting a point estimate with no interval. Forgetting that approved-only data is selected. Not agreeing in advance what level triggers action.

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

### Q21 ⭐⭐ 🟡 A recommender's click-through rate has slid 6% over eight weeks even though its offline NDCG improved 3% at launch. Catalogue diversity in recommendations has also shrunk. Explain how a feedback loop and exposure bias could cause this, how you would check for it, and what you would change.
**Asked at:** Recommender feedback-loop and popularity-bias literature (Mansoury et al. 'Feedback Loop and Bias Amplification in Recommender Systems', a popularity-bias survey on arXiv) plus a Prachub ranking-debugging page; no public interview page for this exact prompt, so editor-designed from the literature; search snippets only, not opened
**Say this first (1 line):** If the recommender learns only from clicks on items it already showed, popular items get more exposure and more clicks, the tail starves, diversity shrinks and CTR drifts down, while an offline NDCG measured on those same logs still looks better; I would prove it with exposure data and a small random slice, then add exploration.

**Clarifying questions:**
- Is "6%" relative (5.0% to 4.7%) or six points? It sets how big the problem is, and I will assume relative.
- Is CTR per impression or per user, and did the traffic mix (new versus returning users, platform) change over the eight weeks? A mix shift can fake a slide.
- How was the offline NDCG computed? If it used clicks logged under the old ranker, it can only credit items that ranker already showed, so it is exposure-biased.
- How is "diversity" measured: share of catalogue shown, entropy of impressions, top-10 item share? I need one number to track.
- Is any traffic randomised today? Random exposure is the only unbiased evidence of how tail items really perform.
- Do users see the same items repeatedly? That adds fatigue, a second cause of a slide.

**Approach:**
1. Confirm the slide is real: CTR per impression by week, split by position, platform and user cohort, with seasonality and UI changes ruled out.
2. Measure concentration over time: distinct items shown per day, share of impressions going to the top 1% of items, normalised entropy of impression shares. Compare week 0 with week 8.
3. Test the loop directly: for items with similar quality signals (price, rating, age), compare CTR per exposure for items that got high early exposure versus low. Use position-normalised CTR so slot effects do not distort it.
4. Run a small randomised slice (illustrative 1 to 2% of requests, one slot filled by random eligible items). Compare CTR of randomised-slot items by popularity bucket. If tail items do as well per exposure as head items, the ranker is under-exposing them.
5. Check fatigue: CTR by number of prior exposures of the same item to the same user.
6. Change the system: reserve exploration slots or use Thompson-style sampling for uncertain items; train with inverse-propensity weights from logged exposure probabilities; add a diversity or coverage constraint in re-ranking; give new items a freshness boost.
7. Evaluate offline with a counterfactual estimator on randomised data, not raw logged NDCG; then run a long A/B with a permanent small holdout.

**Metrics:**
- CTR = clicks / impressions, also reported per position so slot mix does not change it.
- Coverage = distinct items shown in a day / eligible items that day.
- Top-1% share = impressions on the 1% most-shown items / all impressions.
- Normalised entropy = -sum(s_i ln s_i) / ln(N), where s_i is item i's impression share and N the number of items.
- Randomised-slot CTR by popularity bucket (head, torso, tail).
- Guardrails: orders or revenue per session, session length, latency, and the CTR cost of the exploration slice.

**Risks:**
- Exposure-biased offline evaluation: NDCG up 3% on logged data does not show a better ranker for items it never showed.
- Seasonality or catalogue changes can explain CTR without any loop.
- Exploration lowers CTR in the short run, so it needs a budget and a time horizon.
- Diversity can be gamed with irrelevant items; pair it with a relevance floor.
- A multi-week slide has more than one cause (fatigue, novelty fade, competition); do not credit it all to the loop.

**What the interviewer scores:**
- Strong: explains the loop (exposure drives clicks, clicks drive ranking) and why offline logged NDCG cannot see it. Weak: says "retrain more often".
- Strong: asks for randomised exposure data or a holdout as unbiased evidence. Weak: argues from the dashboard only.
- Strong: gives concrete concentration metrics and the fix list (exploration, IPS, diversity). Weak: "add diversity" with no measurement.
- Strong: states the cost of exploration and how to cap it.

**Example:** (illustrative) CTR goes from 5.00% to 4.70%, which is -6.0% relative. Offline NDCG goes from 0.500 to 0.515, +3.0% relative. Both are in the code. Then a toy world of 300 items, 5 slots, with a legacy popularity head start unrelated to true appeal, and an assumption that an item's appeal saturates as it is shown to the same audience. Ranking by raw clicks shows only 5 distinct items and the slate CTR falls 14.1% over the run. A ranker that keeps one slot random shows all 300 items, top-5 impression share 0.60 instead of 1.00, and its slate CTR roughly doubles because it finds better items. These are toy numbers; the saturation assumption is mine and produces the slide. Weak: "NDCG improved, so the model is better; CTR will recover." Strong: "NDCG was measured on what the old model chose to show. Show me concentration over time and a randomised slice before I touch the model."

**Code:**
```python
import numpy as np

# Part A: the prompt's arithmetic (illustrative levels)
ctr0, ctr1 = 0.0500, 0.0470
assert abs((ctr1 - ctr0) / ctr0 - (-0.06)) < 1e-9          # 6% relative slide
ndcg0, ndcg1 = 0.500, 0.515
assert abs((ndcg1 - ndcg0) / ndcg0 - 0.03) < 1e-9          # +3% relative
print("CTR 5.00% -> 4.70% = -6.0% relative; NDCG 0.500 -> 0.515 = +3.0% relative")

# Part B: toy feedback loop. Assumption (labelled): an item's appeal saturates with repeated
# exposure, p_eff = p * exp(-impressions / TAU).
rng = np.random.default_rng(21)
N, K, ROUNDS, USERS, TAU = 300, 5, 300, 200, 200000.0
true_p = rng.beta(2, 38, N)                       # mean about 5%
exam = np.array([1.0, 0.6, 0.4, 0.3, 0.2])        # position bias
head_start = rng.permutation(1.0 / np.arange(1, N + 1)) * 40  # legacy popularity, unrelated to true_p

def run(policy):
    clicks = rng.poisson(head_start).astype(float)
    imps = np.zeros(N)
    shown = set(); ctrs = []; imp_total = np.zeros(N)
    for r in range(ROUNDS):
        if policy == "popularity":
            slate = np.argsort(-clicks)[:K]
        else:                                        # rate-based, 1 of 5 slots is random exploration
            score = (clicks + 1) / (imps + 20)
            slate = list(np.argsort(-score)[:K - 1])
            rest = [i for i in range(N) if i not in slate]
            slate.append(int(rng.choice(rest)))
            slate = np.array(slate)
        p_eff = true_p[slate] * np.exp(-imp_total[slate] / TAU)
        c = rng.binomial(USERS, exam * p_eff)
        clicks[slate] += c; imps[slate] += USERS; imp_total[slate] += USERS
        shown.update(slate.tolist())
        ctrs.append((exam * p_eff).sum() / exam.sum())
    ctrs = np.array(ctrs)
    top5_share = np.sort(imp_total)[::-1][:5].sum() / imp_total.sum()
    return ctrs[:20].mean(), ctrs[-20:].mean(), len(shown), top5_share

for pol in ("popularity", "explore"):
    a, b, d, s = run(pol)
    print(f"{pol:10s} slate CTR first20={a:.4f} last20={b:.4f} ({(b-a)/a:+.1%}) distinct items shown={d} top5 impression share={s:.2f}")
    if pol == "popularity":
        pa, pb, pd, ps = a, b, d, s
    else:
        ea, eb, ed, es = a, b, d, s
assert pb < pa                  # greedy slate CTR slides
assert pd < ed                  # greedy shows fewer distinct items
assert ps > es                  # greedy concentrates impressions
assert eb > pb                  # exploring policy ends higher
print("asserts passed")
```

**Output (my run):**
```text
CTR 5.00% -> 4.70% = -6.0% relative; NDCG 0.500 -> 0.515 = +3.0% relative
popularity slate CTR first20=0.0750 last20=0.0644 (-14.1%) distinct items shown=5 top5 impression share=1.00
explore    slate CTR first20=0.0718 last20=0.1392 (+94.0%) distinct items shown=300 top5 impression share=0.60
asserts passed
```

**Follow-ups:**
- How big should the random slice be? Size it for the smallest tail-versus-head CTR gap you care about, using the two-proportion sample-size formula on impressions; typically 1 to 2% of traffic is enough because impressions are plentiful.
- Can you fix it without exploration? Partly: IPS-weighted training and diversity constraints help, but they cannot learn about items with zero exposure, so some exploration is still needed.
- How does this relate to Book 6 Part 1, Q39 ("A recommendation model refresh raised click-through rate by 5%, but catalogue diversity fell ...")? That question is about weighing a short-term CTR lift against long-term harm and setting up a holdout for the decision; this one is about why a deployed ranker slides over weeks and how to prove the loop. The long-term holdout idea carries over.

**Common mistakes:**
- Taking logged-click NDCG as proof of a better ranker.
- Blaming seasonality without checking exposure concentration.
- Adding a diversity re-ranker without measuring whether it helps CTR or revenue.
- Running exploration without a budget, or forgetting to log exposure propensities so they cannot be used later.
- Treating the 6% as points when it is relative, or the reverse.

### Q22 ⭐⭐ 🟡 A RAG support chatbot's thumbs-up rate fell from 78% to 69% in a week with no release from your team, and the LLM provider had pushed a silent model update. Explain how you would confirm the cause, what regression evidence you need from a fixed test set, and how to guard against provider-side change in future.
**Asked at:** AI-era RAG and LLM quality-regression guides (Braintrust RAG-observability article, Dataiku RAG-observability post, an Apptension RAG quality guide, practitioner posts on silent AI degradation); reported as a current theme in practitioner guides, not tied to a named employer; search snippets only, not opened
**Say this first (1 line):** A thumbs-up drop with no release on my side points to something I do not control, so I replay a fixed, versioned question set through the old and new provider behaviour, show the paired drop, and then lock the provider version and add a daily canary.

**Clarifying questions:**
- Can I pin or even see the provider's model version, and do my logs record the version string returned? Without it I cannot date the change.
- Did anything else change that week: traffic mix, new documents indexed, a UI change to the thumbs button, a marketing push? These are rival causes.
- How many votes per week, and what share of answers get a vote? Few votes or a small share means selection bias.
- Do I have a frozen test set with expected answers or rubric scores from before the change? If not, building one is step zero.
- Is the retrieval layer unchanged (same index, same prompts, same temperature)? I need to isolate the generator.

**Approach:**
1. Rule out measurement: thumbs-up rate per day around the change date, vote volume, UI changes, user mix. A step change that lines up with the provider date is the first clue.
2. Check for retrieval or data changes: same retrieved passages for the same queries, same index version, same prompt hash.
3. Replay a fixed regression set (illustrative 300 questions) through the current provider and through any pinned older snapshot or archived outputs from before the change, with the same prompts and retrieved context.
4. Compare pass/fail per question with a paired test (exact McNemar): count questions that passed before and fail now versus the reverse.
5. Read the failures: format changes, refusals, shorter answers, citation style, tone. Provider updates usually change style and refusal behaviour, not only knowledge.
6. Mitigate: pin a dated model version if the provider offers one, adjust the prompt for the new behaviour, or switch provider/version; re-run the regression set before any change goes live.
7. Guard for the future: a daily canary of fixed questions with an alert on the pass rate, a provider-change log, and an eval gate for every model or prompt update.

**Metrics:**
- Thumbs-up rate = thumbs-up votes / (thumbs-up + thumbs-down votes), plus vote rate = votes / answers shown.
- Regression pass rate = questions meeting the rubric / questions in the fixed set.
- Paired discordance: b = passed before and failed now, c = failed before and passed now; the test statistic uses b versus c only.
- Guardrails: refusal rate, average answer length, latency, cost per answer, citation validity.

**Risks:**
- Thumbs are self-selected and noisy; a changed UI or user mix can move them without any model change.
- The fixed set can be stale; it may not represent today's questions.
- You cannot rerun the "before" model if the provider has retired it. Archive outputs on a schedule so a baseline exists.
- LLM-judge scores on the regression set can drift too (see Book 6 Part 2, Q45).
- A canary with too few questions misses small drops.

**What the interviewer scores:**
- Strong: separates "users are unhappier" from "answers got worse", using a controlled replay. Weak: guesses it is the provider.
- Strong: uses a paired comparison on the same questions. Weak: compares two different samples of live traffic.
- Strong: proposes pinning, a canary and an eval gate. Weak: only suggests re-prompting.
- Strong: notes the missing model-version logging as a root gap.

**Example:** (illustrative) 3,000 votes in each week: 78% is 2,340 up, 69% is 2,070 up; the two-proportion z is 7.9, so it is not noise, but it says nothing about cause. The fixed set has 300 questions: 255 passed before (85%), 231 pass now (77%). Of the discordant pairs, 38 went pass to fail and 14 went fail to pass: 255 - 38 + 14 = 231. The exact McNemar p-value is 0.0012 and the 95% interval for the paired difference is -12.6 to -3.4 points. A daily unpaired canary of 300 questions could only see a drop of about 8 points with 80% power, so a canary needs more questions or a paired design. Weak: "The provider changed it, nothing we can do." Strong: "Here is the paired replay showing an 8-point fall on the same 300 questions; I will read the 38 regressions, then pin a version and add a canary."

**Code:**
```python
import numpy as np
from scipy import stats

# Thumbs-up: illustrative 3,000 votes per week
n = 3000
up0, up1 = round(0.78 * n), round(0.69 * n)
assert (up0, up1) == (2340, 2070)
p0, p1 = up0 / n, up1 / n
pool = (up0 + up1) / (2 * n)
z = (p0 - p1) / np.sqrt(pool * (1 - pool) * 2 / n)
print(f"thumbs-up {p0:.0%} -> {p1:.0%}, z={z:.1f}")
assert z > 6          # not noise, but says nothing about cause

# Fixed regression set: 300 questions, same questions, same prompts, pinned old vs new provider run
total = 300
pass_before = 255       # 85%
pass_after = 231        # 77%
b_lost, c_gained = 38, 14       # discordant pairs: pass->fail, fail->pass
assert pass_before - b_lost + c_gained == pass_after
assert pass_before / total == 0.85 and pass_after / total == 0.77
res = stats.binomtest(b_lost, b_lost + c_gained, 0.5)       # exact McNemar
print(f"fixed set {pass_before/total:.0%} -> {pass_after/total:.0%}; lost {b_lost}, gained {c_gained}; exact McNemar p={res.pvalue:.4f}")
assert res.pvalue < 0.01
# 95% interval for the paired difference in pass rate (normal approx on paired differences)
d = (c_gained - b_lost) / total
se = np.sqrt((b_lost + c_gained) - (b_lost - c_gained) ** 2 / total) / total
print(f"difference {d*100:+.1f} points, 95% CI [{(d-1.96*se)*100:+.1f}, {(d+1.96*se)*100:+.1f}]")
assert d + 1.96 * se < 0

# Smallest drop a daily 300-question canary can see (pass rate .85, unpaired, 80% power, alpha .05)
sd = np.sqrt(2 * 0.85 * 0.15 / 300)
mde = (1.96 + 0.84) * sd
print(f"unpaired canary of 300: minimum detectable drop about {mde*100:.1f} points")
assert 0.07 < mde < 0.09
```

**Output (my run):**
```text
thumbs-up 78% -> 69%, z=7.9
fixed set 85% -> 77%; lost 38, gained 14; exact McNemar p=0.0012
difference -8.0 points, 95% CI [-12.6, -3.4]
unpaired canary of 300: minimum detectable drop about 8.2 points
```

**Follow-ups:**
- The provider will not let you pin a version. What do you do? Keep your own regression set and canary, own a fallback provider or model path, and treat each provider change as a release that must pass your eval gate.
- Why paired and not two proportions on the replay? The same questions are used twice, so only the questions that changed state carry information; pairing gives a tighter test.
- How would you size the canary? Pick the smallest drop that matters (say 4 points), use the paired or unpaired sample-size formula, and run it daily or at provider-change signals.

**Common mistakes:**
- Declaring the provider guilty from the thumbs drop alone.
- Comparing this week's live traffic with last week's instead of replaying the same questions.
- Not logging the model version and prompt hash with every answer.
- Building a canary too small to see a 4 to 8 point change.
- Fixing the prompt before reading the failure cases.

### Q23 ⭐⭐ 🟡 Answer quality in a RAG system dropped after the team re-embedded only the newly added documents with a newer embedding model, leaving the old vectors in the same index. Retrieval hit rate on a fixed query set went from 82% to 71%. Explain why mixing embedding versions hurts, how you would verify it, and how to fix and prevent it.
**Asked at:** AI-era RAG and LLM quality-regression guides (Braintrust RAG-observability article, Dataiku RAG-observability post, an Apptension RAG quality guide, practitioner posts on silent AI degradation); reported as a current theme in practitioner guides, not tied to a named employer; search snippets only, not opened
**Say this first (1 line):** Vectors from two different embedding models live in two different geometries, so their similarity scores cannot be compared in one index; I would prove it by splitting the hit rate by old and new documents, then re-embed everything with one model (blue-green) and version the index.

**Clarifying questions:**
- Which model embeds the query today, the old one, the new one, or both? This decides which documents become unreachable.
- Do the two models have different dimensions or normalisation? A dimension mismatch would fail loudly; same dimension fails silently.
- How big is the corpus and what does a full re-embed cost and take? It decides between a full re-embed and a gradual migration.
- Is there a fixed query set with labelled relevant documents (the 82% to 71% measurement)? I need to slice it by which model embedded the answer document.
- Can the system keep two indexes side by side? That allows a safe cutover.

**Approach:**
1. Slice the hit-rate query set by the embedding version of the target document (old-embedded versus new-embedded). A mixed index shows old and new targets behaving differently.
2. Check query-side behaviour: which model embeds the query, and what are the top-1 cosine scores for old-document and new-document hits? Different score scales mean the merged ranking is biased.
3. Verify the mechanism offline: re-embed a sample of old documents with the new model and compare hit rate, or embed the same documents with both models and measure cross-model cosine (it will be near chance).
4. Fix: re-embed the whole corpus with the new model into a fresh index, build it in the background, compare hit rate on the fixed query set, then switch traffic; keep the old index for rollback.
5. Prevent: store the embedding model name and version on every vector and on the index; refuse inserts whose version differs from the index; make "model change" mean "new index"; add a retrieval hit-rate check to the deploy gate.

**Metrics:**
- Hit rate at k = queries whose labelled relevant document appears in the top k / all queries. Report by target embedding version.
- Mean reciprocal rank as a second view; mean top-1 cosine by index segment.
- Guardrails: query latency, index build cost, answer-quality score on the fixed set.

**Risks:**
- Normalising or rescaling scores per model can hide the problem without fixing it.
- Dual-querying both models and merging by raw cosine looks reasonable but ranks by score scale, not relevance.
- Partial re-embedding leaves a long tail of old vectors that are quietly unreachable.
- Re-embedding costs money and time; the fixed query set must be representative of real traffic.

**What the interviewer scores:**
- Strong: explains that embedding spaces are model-specific, so cross-model cosine is meaningless. Weak: "the new model is probably worse".
- Strong: verifies with a slice and a controlled re-embed. Weak: just reverts.
- Strong: version metadata plus blue-green index as the prevention. Weak: "tell the team to be careful".

**Example:** (illustrative toy, 2,000 documents, 400 queries, 15% of documents embedded by a new model, whose cosines sit higher because it has a large shared direction). The baseline with everything in the old model finds the target in the top 5 for 100% of queries (the toy is easy on purpose). In the mixed index: querying with the old model gives 0.91 overall but 0.00 for new-embedded targets; querying with the new model gives 0.10 overall and 0.00 for old-embedded targets; querying both and merging by raw cosine gives 0.33, because new-model cosines are larger (mean top-1 cosine 0.93 versus 0.78) and crowd out the old documents. Re-embedding everything with the new model returns 1.00. The prompt's 82% to 71% is a milder version of the same effect, probably because other signals (keyword search, a reranker) rescue part of the loss; I would not claim which. Weak: "retrieval got worse, add more documents." Strong: "Slice by embedding version, show old and new targets behave differently, rebuild one index."

**Code:**
```python
import numpy as np
rng = np.random.default_rng(23)
D, N, Q, NEW_FRAC, K = 32, 2000, 400, 0.15, 5

def unit(m): return m / np.linalg.norm(m, axis=1, keepdims=True)
latent = unit(rng.normal(size=(N, D)))
def rot():
    q, _ = np.linalg.qr(rng.normal(size=(D, D))); return q
RA, RB = rot(), rot()
common = unit(rng.normal(size=(1, D)))[0]             # model B shares a big common direction (higher cosines)
def embA(x): return unit(x @ RA + 0.05 * rng.normal(size=x.shape))
def embB(x): return unit(unit(x @ RB + 0.05 * rng.normal(size=x.shape)) + 1.5 * common)

is_new = rng.random(N) < NEW_FRAC
docA = embA(latent); docB = embB(latent)
target = rng.integers(0, N, Q)
qlat = unit(latent[target] + 0.12 * rng.normal(size=(Q, D)))
qA, qB = embA(qlat), embB(qlat)
docs_mixed = np.where(is_new[:, None], docB, docA)      # index: old docs in A, new docs in B
docs_allA = docA

def hit(scores):
    top = np.argsort(-scores, axis=1)[:, :K]
    return (top == target[:, None]).any(axis=1)

h_clean = hit(qA @ docs_allA.T)                                    # all docs and queries in model A
h_Aq = hit(qA @ docs_mixed.T)                                      # mixed index, query embedded by A
h_Bq = hit(qB @ docs_mixed.T)                                      # mixed index, query embedded by B
# dual query: score old docs with qA, new docs with qB, merge on raw cosine
s_dual = np.where(is_new[None, :], qB @ docB.T, qA @ docA.T)
h_dual = hit(s_dual)
# fix: re-embed everything with B and query with B
h_fix = hit(qB @ docB.T)
print(f"new-model share of index: {is_new.mean():.0%}")
for name, h in [("all old, A query (baseline)", h_clean), ("mixed, A query", h_Aq), ("mixed, B query", h_Bq),
                ("mixed, dual query merged by raw score", h_dual), ("all re-embedded with B", h_fix)]:
    print(f"{name:40s} hit@{K} = {h.mean():.2f}  | target old docs {h[~is_new[target]].mean():.2f}  target new docs {h[is_new[target]].mean():.2f}")
assert h_clean.mean() > 0.7
assert h_Aq.mean() < h_clean.mean() - 0.05
assert h_Bq.mean() < h_clean.mean() - 0.3
assert h_dual.mean() < h_clean.mean() - 0.03
assert abs(h_fix.mean() - h_clean.mean()) < 0.08
# the cosine between a doc and its own query is on a different scale in each space
print("mean top-1 cosine A:", round(float((qA @ docA.T).max(1).mean()), 2), " B:", round(float((qB @ docB.T).max(1).mean()), 2))
print("asserts passed")
```

**Output (my run):**
```text
new-model share of index: 14%
all old, A query (baseline)              hit@5 = 1.00  | target old docs 1.00  target new docs 1.00
mixed, A query                           hit@5 = 0.91  | target old docs 1.00  target new docs 0.00
mixed, B query                           hit@5 = 0.10  | target old docs 0.00  target new docs 1.00
mixed, dual query merged by raw score    hit@5 = 0.33  | target old docs 0.26  target new docs 1.00
all re-embedded with B                   hit@5 = 1.00  | target old docs 1.00  target new docs 1.00
mean top-1 cosine A: 0.78  B: 0.93
asserts passed
```

**Follow-ups:**
- Could you align the two spaces with a learned linear map? Sometimes approximately, but it needs paired data and loses quality; a full re-embed is the safe answer when the corpus is not huge.
- What if the corpus is huge? Migrate by shard into a new index while serving from the old, and switch only when the whole index is on one version; never mix inside one search.
- What belongs on the deploy gate? Fixed-query hit rate by segment, the embedding version tag check, and a latency check.

**Common mistakes:**
- Embedding only new documents with the new model "to save cost".
- Merging results from two indexes by raw similarity score.
- No model-version metadata, so nobody can tell which vectors are which.
- Judging only the overall hit rate and missing the old-versus-new split.
- Rebuilding the index in place with no rollback copy.

### Q24 ⭐⭐ 🟡 A demand model that had a bias of about zero now over-forecasts by 15% after a competitor cut prices and the company changed its own pricing. MAPE has risen from 11% to 18%. Explain how you would diagnose a structural break, what you would do before you can retrain on enough new data, and how you would keep the business safe in the meantime.
**Asked at:** No interview page located; forecast-monitoring practitioner pages (demandplanning.net MAPE and bias, John Galt Solutions, 42signals forecast-drift post) describe bias, structural breaks and MAPE blind spots, so editor-designed; search snippets only, not opened
**Say this first (1 line):** A bias that jumps from zero to +15% right after a price cut is a structural break, not noise, so I confirm it with bias and change-point checks, patch the forecast with a short-lag bias correction and manual overrides, and retrain once I have enough post-break weeks.

**Clarifying questions:**
- Exactly when did the competitor cut and when did we change our own price? The break date tells me how many post-break weeks exist.
- Is price an input to the model today? If not, it is blind to this cause; if yes, the new price range may be outside what it saw.
- Is the over-forecast uniform across products and regions, or concentrated where the competitor competes? It decides between one global correction and segment corrections.
- What do the forecasts drive (stock, purchase orders, markdown)? Over-forecast of 15% means excess stock, and I need its cost.
- Are there other changes in that window (promotions, stock-outs that censor demand, tracking changes)? These look like a break too.

**Approach:**
1. Separate bias from error size: report bias = sum(forecast - actual) / sum(actual) next to MAPE. Bias near 0 before, +15% after, is a level shift; MAPE alone hides its direction.
2. Locate the break: plot weekly bias, run a CUSUM or change-point check, and line the date up with the competitor and own price events.
3. Rule out data errors and stock-outs (censored demand would push actuals down and create a false over-forecast).
4. Segment: which categories and regions carry the bias? Price-sensitive segments first.
5. Interim fix before retraining: multiply the forecast by a rolling forecast-to-actual ratio from the last few matured weeks (lagged so only known actuals are used), let planners override, and widen safety-stock logic so that it is not driven by the bad point forecast.
6. Model fix: add price and competitor-price ratio as features; with only a few weeks post-break use a hierarchical or elasticity-prior approach, or train on all history with a regime indicator and interaction terms.
7. Monitor: weekly bias alert (not only MAPE), a break detector, and a rule that any pricing change notifies the forecasting team.

**Metrics:**
- Bias = (sum of forecasts - sum of actuals) / sum of actuals over a window.
- MAPE = mean over weeks of |forecast - actual| / actual (state the treatment of zero actuals).
- Tracking signal or CUSUM of percentage error for break detection.
- Business guardrails: excess stock weeks of cover, stock-out rate, markdown cost.

**Risks:**
- Retraining immediately on a few weeks can overfit noise; retraining late keeps the bias.
- A rolling correction lags a second break and can over-correct once the model is fixed.
- Stock-outs censor demand; the data can mislead.
- Price effects differ by category; one global multiplier fixes the total but not the mix.

**What the interviewer scores:**
- Strong: names bias separately from MAPE and ties the break to the price events. Weak: "retrain".
- Strong: gives an interim control that works with little data. Weak: waits for data.
- Strong: asks what the forecast decides, and sizes the business risk. Weak: only talks about the model.
- Strong: monitors bias and breaks. Weak: monitors accuracy only.

**Example:** (illustrative) Percentage errors are roughly Normal. If the spread gives a MAPE of 11% at zero bias, adding a +15% bias gives a MAPE of about 16.9%, so the prompt's move from 11% to 18% is plausible and is mostly the bias. In a 120-week simulation with the break at week 60 (demand ends up 1/1.15 of what the old pattern implies): before the break the bias is -0.9% and the MAPE 12.3%; after it the bias is +14.6% and the MAPE 17.1%. A CUSUM alarm fires at week 66, six weeks after the break. A rolling forecast-to-actual ratio lagged by two weeks brings the post-break bias to +2.9% and the MAPE to 12.5% without any retraining. Weak: "MAPE went up, retrain the model on the last month." Strong: "Bias is +15% since the price cut; I patch with a lagged ratio and overrides now and add price features once there are enough weeks."

**Code:**
```python
import numpy as np
from scipy.stats import norm

# Check the prompt: can bias 0 -> +15% and MAPE 11% -> 18% both be true?
# Percentage error e = (forecast - actual)/actual ~ Normal(mu, s). E|e| for a folded normal:
def mape_fold(mu, s): return s * np.sqrt(2 / np.pi) * np.exp(-mu**2 / (2 * s**2)) + mu * (1 - 2 * norm.cdf(-mu / s))
s = 0.11 / np.sqrt(2 / np.pi)                  # s that gives MAPE 11% at zero bias
print(f"spread giving MAPE 11% at zero bias: {s:.3f}; MAPE with +15% bias: {mape_fold(0.15, s):.3f}")
assert abs(mape_fold(0, s) - 0.11) < 1e-9 and 0.16 < mape_fold(0.15, s) < 0.19   # consistent with the prompt's 18%

# Simulation: 120 weekly points, break at week 60 (price cut; model does not see price)
rng = np.random.default_rng(24)
W, BREAK = 120, 60
actual = 1000 * (1 + 0.1 * np.sin(np.arange(W) * 2 * np.pi / 52)) * 1.0
actual[BREAK:] *= 1 / 1.15                      # demand ends up 1/1.15 of what the old pattern implies
fc = 1000 * (1 + 0.1 * np.sin(np.arange(W) * 2 * np.pi / 52)) * np.exp(rng.normal(0, s, W))
act = actual * np.exp(rng.normal(0, 0.02, W))
err = (fc - act) / act
pre, post = err[:BREAK], err[BREAK:]
print(f"before: bias {pre.mean():+.3f} MAPE {np.abs(pre).mean():.3f} | after: bias {post.mean():+.3f} MAPE {np.abs(post).mean():.3f}")

# CUSUM on the percentage error: flag when cumulative positive drift passes a limit
k, h = 0.08, 0.50
c, flag = 0.0, None
for t in range(W):
    c = max(0.0, c + err[t] - k)
    if c > h and flag is None: flag = t
print("break at week", BREAK, "| CUSUM alarm at week", flag)
assert flag is not None and BREAK <= flag <= BREAK + 6

# Interim patch: multiply forecast by a bias correction learned from the last 4 matured weeks (lag 2)
adj = fc.copy()
for t in range(BREAK, W):
    lo, hi = max(0, t - 6), t - 2
    ratio = (fc[lo:hi] / act[lo:hi]).mean()      # recent forecast-to-actual ratio
    adj[t] = fc[t] / ratio
err_adj = (adj - act) / act
print(f"after, with rolling ratio patch: bias {err_adj[BREAK:].mean():+.3f} MAPE {np.abs(err_adj[BREAK:]).mean():.3f}")
assert np.abs(err_adj[BREAK + 8:]).mean() < np.abs(post[8:]).mean()
print("asserts passed")
```

**Output (my run):**
```text
spread giving MAPE 11% at zero bias: 0.138; MAPE with +15% bias: 0.169
before: bias -0.009 MAPE 0.123 | after: bias +0.146 MAPE 0.171
break at week 60 | CUSUM alarm at week 66
after, with rolling ratio patch: bias +0.029 MAPE 0.125
asserts passed
```

**Follow-ups:**
- Why not just wait six weeks and retrain? Six weeks at +15% bias is real excess stock; the interim patch costs little and is reversible.
- How would you pick the correction window? Short enough to track the new level (4 to 6 weeks), long enough that noise does not move it; test it on past breaks and check how it behaves after the model is retrained.
- How do you know the break is price and not a stock-out? Check on-hand stock and sales per day; stock-outs show censored sales, price shows lower demand with stock available.

**Common mistakes:**
- Looking at MAPE only and missing that the error is one-sided.
- Retraining at once on too few weeks and swapping one bias for another.
- Leaving the rolling correction on after the model is fixed (double correction).
- Ignoring stock-out censoring.
- Not telling planners which forecasts are being overridden and why.

### Q25 ⭐⭐ 🟡 A payments fraud model's catch rate on confirmed fraud fell from 85% to 70% over three months while its false-positive rate stayed flat, and analysts say fraudsters changed tactics. Explain how you would confirm adversarial adaptation, why naive retraining on recent flagged cases is risky, and which layered responses you would use.
**Asked at:** No interview question page located for this exact scenario; practitioner fraud and retraining guides (a Firstsource fraud-model post, a datainterview.com 'when to retrain' course page) describe the retrain-versus-rollback and adaptive-fraud themes, so editor-designed; search snippets only, not opened
**Say this first (1 line):** A falling catch rate with a flat false-positive rate means fraud changed, not the model, so I show it with confirmed-fraud cohorts split by tactic, refuse to retrain only on flagged cases because they hide the new tactic, and respond in layers with random audits, rules, features and a retrain on proper labels.

**Clarifying questions:**
- How is "confirmed fraud" labelled, and how late? Chargebacks lag, so recent months are under-counted and the 70% may still move.
- Did the transaction mix or approval policy change, or was a rule that used to catch fraud removed? Those drop catch rate without any adversary.
- Is the catch rate measured at a fixed score threshold, and is the threshold unchanged?
- Which analyst signals say tactics changed: new merchant types, device patterns, small-amount probing, mule accounts?
- Is there a random audit sample today? It is the clean way to measure fraud the model never flags.

**Approach:**
1. Confirm the drop is real and not label lag: compare catch rate for equal-maturity cohorts (same days since transaction) and report a confidence interval.
2. Split confirmed fraud by "tactic" using features and analyst tags: old patterns versus new. Compute the catch rate in each.
3. Look at the score distribution of confirmed fraud: new fraud clusters just below the threshold or at low scores, and its features (new devices, merchants, amount patterns) are unlike the training data.
4. Check what stayed the same: false-positive rate flat and good-traffic distribution stable point to the fraud side moving, not the model decaying everywhere.
5. Avoid the naive retrain: a training set of recent flagged cases contains mostly the old tactic, because the new one was not flagged; unflagged new fraud is labelled legitimate unless the chargeback arrives. That reinforces the blind spot.
6. Layered response: a random audit slice for unbiased labels; fast rules and velocity or device-linking features for the new tactic; a retrain on confirmed outcomes with recency weights and the new features; consider a second model or anomaly score for novelty; keep an analyst feedback loop.
7. Monitor catch rate per tactic and per segment, not only overall, and track adversary signals (probing, reaction after each rule change).

**Metrics:**
- Catch rate (recall) = confirmed fraud cases flagged / confirmed fraud cases, by matured cohort.
- False-positive rate = legitimate transactions flagged / legitimate transactions.
- Catch rate by tactic = flagged cases of that tactic / all confirmed cases of that tactic.
- Guardrails: approval rate, customer friction (declines of good users), analyst queue size and review time.

**Risks:**
- Label delay makes the latest cohorts look better or worse than they are.
- Selection bias: labels exist mainly where the system or analysts looked.
- Adversaries adapt to each fix; rules decay.
- A new rule raises false positives and customer friction.
- A random audit costs reviewer time and lets some fraud through, by design.

**What the interviewer scores:**
- Strong: separates "fraud changed" from "model broke" with a tactic split. Weak: assumes drift and retrains.
- Strong: explains why flagged-only training data is biased. Weak: "retrain on the last three months".
- Strong: layered response with time scales (rules now, model later) and the audit slice. Weak: one fix.
- Strong: mentions label maturity. Weak: treats the 70% as final.

**Example:** (illustrative) Take 1,000 confirmed fraud cases. If the old tactic is caught 85% of the time and the new one 10%, a 70% overall catch rate needs the new tactic to be 20% of fraud: 800 old cases (680 caught) and 200 new (20 caught), 700 of 1,000. A z-test with 1,000 cases in each period gives z = 8.0 for 85% versus 70%, so the drop is not noise. Among flagged fraud, the new tactic is only 20 of 700 = 2.9%, against 20% of real fraud, and 180 new-tactic fraud cases look like normal traffic. A flagged-only retrain would learn almost nothing about the new tactic. A random audit of 2,000 transactions at a 0.5% fraud base rate finds about 10 fraud cases (12 in my seeded run), enough to start measuring the blind spot. Weak: "Retrain on the recent fraud we caught." Strong: "Split by tactic first; recent flagged cases are the cases the model already knew."

**Code:**
```python
import numpy as np
from scipy.stats import norm

# Prompt check: catch rate 85% -> 70% with flat FPR. Illustrative month: 1,000 confirmed fraud cases.
# Two tactics: old (still caught at 85%) and new (caught at 10%).
n_fraud, catch_old, catch_new = 1000, 0.85, 0.10
share_new = (0.85 - 0.70) / (catch_old - catch_new)      # mix that gives 70% overall
print(f"new-tactic share needed for 70% overall: {share_new:.2f}")
assert abs(share_new - 0.20) < 1e-12
old_n, new_n = round(n_fraud * (1 - share_new)), round(n_fraud * share_new)
caught_old, caught_new = old_n * catch_old, new_n * catch_new
caught_old, caught_new = round(caught_old), round(caught_new)
assert (old_n, new_n, caught_old, caught_new) == (800, 200, 680, 20)
overall = (caught_old + caught_new) / n_fraud
assert abs(overall - 0.70) < 1e-12
print(f"old {old_n} cases, caught {caught_old:.0f}; new {new_n} cases, caught {caught_new:.0f}; overall {overall:.0%}")

# Is the drop real? Two catch rates, 1,000 cases each (previous quarter vs this quarter)
p1, p2, n = 0.85, 0.70, 1000
pool = (p1 + p2) / 2
z = (p1 - p2) / np.sqrt(pool * (1 - pool) * 2 / n)
print(f"z for 85% -> 70% with n=1000 each: {z:.1f}")
assert z > 7

# Naive retrain on 'recent flagged cases': fraud labels only exist where we flagged (or chargebacks come later)
flagged_fraud = caught_old + caught_new
share_new_in_flagged = caught_new / flagged_fraud
print(f"new tactic is {share_new:.0%} of real fraud but {share_new_in_flagged:.1%} of flagged fraud")
assert round(share_new_in_flagged, 3) == 0.029
# the model learns the old pattern even more strongly; the 180 missed new-tactic cases look like normal traffic
missed_new = new_n - caught_new
print("new-tactic fraud labelled as legitimate in a flagged-only training set:", int(missed_new))
assert missed_new == 180

# Fix: add a random audit sample. Auditing 2,000 of 200,000 transactions (1%) at a 0.5% fraud base rate
rng = np.random.default_rng(25)
audit = rng.binomial(1, 0.005, 2000)
print("random audit finds", audit.sum(), "fraud cases in 2,000 reviewed (expected about 10)")
assert 3 <= audit.sum() <= 20
```

**Output (my run):**
```text
new-tactic share needed for 70% overall: 0.20
old 800 cases, caught 680; new 200 cases, caught 20; overall 70%
z for 85% -> 70% with n=1000 each: 8.0
new tactic is 20% of real fraud but 2.9% of flagged fraud
new-tactic fraud labelled as legitimate in a flagged-only training set: 180
random audit finds 12 fraud cases in 2,000 reviewed (expected about 10)
```

**Follow-ups:**
- Why is the FPR staying flat informative? It suggests the good-traffic score distribution did not move, so the model is not broadly miscalibrated; the missed cases are a new fraud subpopulation.
- How would you know an adversary is probing? Many small-amount attempts or new accounts testing the threshold, followed by a change in pattern after each rule or model update.
- What if fraud is also reaching you through a channel with no labels? The random audit slice and downstream signals (disputes, customer reports) are the only way to size it.

**Common mistakes:**
- Retraining on flagged-only data.
- Judging the newest cohorts before chargebacks have arrived.
- Fixing with a single rule that fraudsters route around in a week.
- Reporting only overall catch rate and missing the tactic split.
- Having no random audit, so the blind spot cannot be measured.

### Q26 ⭐⭐ 🟡 A search ranker's overall NDCG is stable, but long-tail queries (the 20% that are rare) have worsened by 8% while head queries improved. Explain how segment-level degradation can be hidden by head-query volume, how you would build a sliced evaluation and monitoring view, and what remedies exist.
**Asked at:** Recommender feedback-loop and popularity-bias literature (Mansoury et al. 'Feedback Loop and Bias Amplification in Recommender Systems', a popularity-bias survey on arXiv) plus a Prachub ranking-debugging page; no public interview page for this exact prompt, so editor-designed from the literature; search snippets only, not opened
**Say this first (1 line):** Head queries are most of the volume, so a small head gain can cancel a large tail loss in the overall number; I would report NDCG by query frequency bucket with confidence intervals, alert on the tail slice itself, and fix the tail with better candidate generation, query understanding and tail-focused training data.

**Clarifying questions:**
- Is "20%" the share of queries or of traffic? Long-tail queries are rare, so the two shares differ and the weights in the overall number depend on it.
- How is "long tail" defined (frequency in the last 30 days, a head/torso/tail cut, or a rare-term flag)? The cut decides which queries land in the slice.
- Is NDCG computed from human judgements or from clicks? Clicks on rare queries are sparse and noisy.
- What changed in the ranker: new training data, a popularity feature, a new embedding model? Tail queries often depend on semantic matching.
- What does a failed tail query cost: zero-result pages, abandonment, support contacts?

**Approach:**
1. Slice the evaluation: bucket queries by frequency (head, torso, tail), by intent, by length, by language or script, and by whether the query has results at all. Report NDCG and volume per bucket.
2. Do the weighting arithmetic: overall change = sum of (share x change). A tail drop of 8% with 20% share is a 1.6% drag on the overall, and can be hidden by a head gain.
3. Add uncertainty: with fewer tail queries per week, bootstrap confidence intervals per slice; alert on a slice only when the interval excludes zero change.
4. Diagnose: compare candidate recall (is the right item even retrieved?) versus ranking order (is it retrieved but ranked low?). Tail failures are often retrieval or vocabulary mismatch.
5. Remedies: hybrid lexical plus semantic retrieval, query rewriting and spell correction, data augmentation or synthetic queries for tail, a tail-weighted loss, a separate tail model or fallback, and click-data smoothing so popularity features do not bury rare items.
6. Operationalise: a sliced-metrics dashboard with a minimum-sample rule, a release gate that blocks a launch if a protected slice regresses beyond a set margin, and a golden set of tail queries kept fresh.

**Metrics:**
- NDCG@10 by bucket = mean over queries in the bucket of DCG@10 / ideal DCG@10.
- Volume share by bucket = queries in bucket / all queries (state if by queries or traffic).
- Zero-result rate = queries returning no result / queries; abandonment rate on tail queries.
- Guardrails: head NDCG must not fall, latency, index recall at k.

**Risks:**
- Per-query NDCG is noisy and tail slices are small; a small slice can look worse by chance.
- Changing the bucket definition after seeing the result is slice shopping.
- Click-based labels favour head queries, so the tail looks worse than it is, or better.
- A tail-specific fix can slow queries or hurt the head.

**What the interviewer scores:**
- Strong: shows the weighted-average arithmetic and why the overall metric stays flat. Weak: "the model got worse for some queries".
- Strong: uses intervals and a minimum sample per slice. Weak: reads point estimates.
- Strong: separates retrieval from ranking failure. Weak: "add more data".
- Strong: proposes a release gate on slices. Weak: only a dashboard.

**Example:** (illustrative) Head NDCG is 0.70 on 80% of queries and tail NDCG is 0.50 on 20%. A tail fall of 8% takes it to 0.46, which moves the overall by 0.2 x (-0.04) = -0.008. The head needs to rise from 0.70 to 0.71 to hide it, a gain of only 1.4%. In a seeded simulation with 10,000 queries a week and per-query NDCG sd of 0.3: overall changes -0.0050 with a 95% bootstrap interval of [-0.0121, +0.0024] (flat); head +0.0041 [-0.0038, +0.0121]; tail -0.0412 [-0.0583, -0.0248] (clearly down). Only the tail slice shows the problem. Weak: "Overall NDCG is stable, so no action." Strong: "Show me NDCG by frequency bucket with intervals; the tail can fall while the head hides it."

**Code:**
```python
import numpy as np

# Prompt arithmetic: head 80% / tail 20% of queries; tail NDCG 0.50 -> 0.46 (-8%); overall stable.
head_share, tail_share = 0.8, 0.2
tail0, tail1 = 0.50, 0.46
assert abs((tail1 - tail0) / tail0 + 0.08) < 1e-12
tail_loss = tail_share * (tail1 - tail0)               # -0.008 on overall NDCG
head_gain_needed = -tail_loss / head_share             # head must gain this much for overall to be flat
head0 = 0.70
head1 = head0 + head_gain_needed
print(f"tail drags overall by {tail_loss:+.3f}; head must rise {head0:.2f} -> {head1:.2f} ({head_gain_needed/head0:+.1%}) to hide it")
assert abs(tail_loss + 0.008) < 1e-12 and abs(head1 - 0.71) < 1e-12

# Simulation: per-query NDCG is noisy (sd 0.3). 10,000 queries per week: 8,000 head, 2,000 tail.
rng = np.random.default_rng(26)
def week(head_mean, tail_mean):
    h = np.clip(rng.normal(head_mean, 0.3, 8000), 0, 1); t = np.clip(rng.normal(tail_mean, 0.3, 2000), 0, 1)
    return h, t
h0, t0 = week(0.70, 0.50); h1, t1 = week(0.71, 0.46)
all0, all1 = np.r_[h0, t0], np.r_[h1, t1]
def diff_ci(a, b, B=2000):
    d = [rng.choice(b, len(b)).mean() - rng.choice(a, len(a)).mean() for _ in range(B)]
    return np.mean(b) - np.mean(a), np.percentile(d, [2.5, 97.5])
for name, a, b in [("overall", all0, all1), ("head", h0, h1), ("tail", t0, t1)]:
    d, ci = diff_ci(a, b)
    print(f"{name:8s} change {d:+.4f}  95% bootstrap CI [{ci[0]:+.4f}, {ci[1]:+.4f}]")
d_all, ci_all = diff_ci(all0, all1)
d_tail, ci_tail = diff_ci(t0, t1)
assert ci_all[0] < 0 < ci_all[1]                       # overall: not distinguishable from flat
assert ci_tail[1] < 0                                  # tail alone: clearly down
print("asserts passed")
```

**Output (my run):**
```text
tail drags overall by -0.008; head must rise 0.70 -> 0.71 (+1.4%) to hide it
overall  change -0.0050  95% bootstrap CI [-0.0121, +0.0024]
head     change +0.0041  95% bootstrap CI [-0.0038, +0.0121]
tail     change -0.0412  95% bootstrap CI [-0.0583, -0.0248]
asserts passed
```

**Follow-ups:**
- How many tail queries do you need? For a slice mean with per-query sd of 0.3, the standard error is 0.3 / sqrt(n); with 2,000 queries it is about 0.0067, so a 0.04 change is visible, but a 0.01 change is not. Pool several weeks for smaller changes.
- Should you optimise the tail at the expense of the head? Not blindly: set a protected-slice rule, such as no head regression beyond a small margin, and weigh by business value.
- Is the tail always low value? No; in some products rare queries carry high intent, so check conversion by bucket.

**Common mistakes:**
- Trusting a single overall metric.
- Reading small-slice point estimates without intervals.
- Defining the slices after looking at the results.
- Fixing ranking when the item was never retrieved.
- Letting popularity features bury new or rare items.

### Q27 ⭐⭐ 🟡 Mean score from a credit model fell from 0.30 to 0.22 this month, but outcomes will not mature for months. Explain the competing hypotheses (a change in applicants, a pipeline bug, a model change, real risk improvement), the checks that separate them using only unlabelled data, and what you would tell the business before labels arrive.
**Asked at:** Drift and monitoring-without-labels guides (techinterview.org MLOps guides, a DataDome write-up on monitoring models without labels, KodeKloud and NannyML-style material); commonly reported in public guides for MLOps and ML-system-design loops; search snippets only, not opened
**Say this first (1 line):** With no outcomes yet, I split the fall in mean score into a change in who is applying and a change in score within each type of applicant, then check pipeline, model and feature health to see which part is real; I tell the business what we know, what we do not, and when labels will tell us.

**Clarifying questions:**
- Was there any change to the model, its features, the scoring service or the data feeds this month? A deployment calendar answers part of this at once.
- Did the applicant source mix change (new partner, marketing channel, product, city)? Mix is the first non-model cause.
- Did the policy upstream of the model change (pre-filters, eligibility rules, cut-offs)? It changes who reaches the model.
- Is the score a probability of default, and is it calibrated? A mean-score fall only means lower risk if calibrated.
- Do we have partial early signals (first-payment default, early delinquency)? They give a weak read before full labels.

**Approach:**
1. Rule out a plain bug: null rates, ranges, units and schema checks on every input feature; compare feature distributions to last month with PSI; check the scoring service version and that the model hash is unchanged.
2. Replay test: re-score last month's applications through the current pipeline. If scores differ, the pipeline or model changed; if not, the inputs changed.
3. Decompose the fall: segment applicants (for example prime, near-prime, subprime, or by channel) and split the change into a mix effect (shares changed) and a within-segment effect (scores moved inside a segment).
4. If it is mostly mix, check whether the new mix is plausible (marketing, partner, policy change). If within-segment, find which features moved and why (new data source, changed bureau fields, income capture).
5. Look at early indicators: first-payment default, early delinquency and application-level proxies, with caution about their power.
6. Communicate: "Mean score fell 0.08; about half is a change in applicant mix; the rest is inside segments and I am checking features. No evidence of a bug if the replay matches. Risk is unconfirmed until outcomes mature; here are the early indicators and the date to re-check." Avoid declaring that risk improved.
7. Put in place: a feature and score-drift dashboard with alerts and a rule that applicant-mix changes are announced to the model team.

**Metrics:**
- Mean score = sum of scores / number of applicants, by month and by segment.
- Mix effect = sum over segments of (share_this - share_last) x mean_last; within-segment effect = sum of share_this x (mean_this - mean_last). They add exactly to the total change.
- PSI by feature and for the score; null rate; replay score difference.
- Guardrails: approval rate, early delinquency, rejection reasons.

**Risks:**
- A lower mean score is not lower risk unless the model is calibrated and the mix is understood.
- Reweighting by observed segments assumes the segments are stable definitions.
- Early indicators are weak and biased by who was approved.
- Acting on the score (for example loosening cut-offs) before outcomes mature locks in losses.

**What the interviewer scores:**
- Strong: lists competing hypotheses and a check for each that needs no labels. Weak: "the model must be fine/broken".
- Strong: mix versus rate decomposition and a replay test. Weak: only PSI.
- Strong: honest communication that risk is unconfirmed. Weak: tells the business risk improved.
- Strong: asks about deployments and policy changes. Weak: jumps to modelling.

**Example:** (illustrative) Segments last month: prime 40% (mean score 0.12), near-prime 30% (0.30), subprime 30% (0.54), mean 0.30. This month: prime 50% (0.092), near-prime 30% (0.26), subprime 20% (0.48), mean 0.22. The change is -0.08. The mix effect is (0.10)(0.12) + 0 + (-0.10)(0.54) = -0.042, which is 52% of it; the within-segment effect is 0.5(-0.028) + 0.3(-0.04) + 0.2(-0.06) = -0.038, or 48%. All three segments' scores fell, which a mix change alone cannot explain, so something also moved inside segments: pipeline, model, feature data, or real improvement. Weak: "The score fell, so risk improved." Strong: "Half is mix; the other half is inside every segment, so I replay and check features before saying anything about risk."

**Code:**
```python
# Mix versus rate decomposition of a fall in mean score (illustrative segments)
seg = ["prime", "near_prime", "subprime"]
share0, mean0 = [0.40, 0.30, 0.30], [0.12, 0.30, 0.54]
share1, mean1 = [0.50, 0.30, 0.20], [0.092, 0.26, 0.48]
m0 = sum(s * m for s, m in zip(share0, mean0)); m1 = sum(s * m for s, m in zip(share1, mean1))
print(f"mean score last month {m0:.3f}, this month {m1:.3f}, change {m1-m0:+.3f}")
assert abs(m0 - 0.30) < 1e-9 and abs(m1 - 0.22) < 1e-9
mix = sum((s1 - s0) * m for s0, s1, m in zip(share0, share1, mean0))        # shares change, old means
rate = sum(s1 * (b - a) for s1, a, b in zip(share1, mean0, mean1))          # means change, new shares
print(f"mix effect {mix:+.3f} ({mix/(m1-m0):.0%}), within-segment effect {rate:+.3f} ({rate/(m1-m0):.0%})")
assert abs(mix + rate - (m1 - m0)) < 1e-12
assert abs(mix - (-0.042)) < 1e-12 and abs(rate - (-0.038)) < 1e-12
for sname, a, b in zip(seg, mean0, mean1):
    print(f"  {sname:10s} mean {a:.3f} -> {b:.3f}  ({b-a:+.3f})")
# Which segments carry the within-segment fall?
contrib = [s1 * (b - a) for s1, a, b in zip(share1, mean0, mean1)]
print("within-segment contributions:", [round(c, 3) for c in contrib])
assert all(c < 0 for c in contrib)     # fall is in every segment: points at pipeline/model/real improvement, not mix alone
print("asserts passed")
```

**Output (my run):**
```text
mean score last month 0.300, this month 0.220, change -0.080
mix effect -0.042 (52%), within-segment effect -0.038 (48%)
  prime      mean 0.120 -> 0.092  (-0.028)
  near_prime mean 0.300 -> 0.260  (-0.040)
  subprime   mean 0.540 -> 0.480  (-0.060)
within-segment contributions: [-0.014, -0.012, -0.012]
asserts passed
```

**Follow-ups:**
- What would a replay mismatch tell you? That the pipeline, feature data or model changed even for the same applicants, so it is not applicant mix.
- What would you say if everything checks out? That the evidence points to a mix shift and unchanged pipeline, with risk still unconfirmed until outcomes mature, and that I will track early delinquency.
- Can you decompose with continuous features instead of segments? Yes, by reweighting this month's applicants to last month's feature distribution and rescoring, which gives the within-segment part without choosing segments.

**Common mistakes:**
- Equating a lower score with lower risk.
- Skipping the replay test.
- Looking only at the overall distribution and missing the segment shift.
- Reassuring the business without saying what is unknown.
- Forgetting upstream policy or source changes.

### Q28 ⭐⭐ 🟡 A conversion model looks badly calibrated on the most recent seven days: predicted 5% against observed 1.5% for yesterday's cohort. The attribution window is seven days, so recent cohorts have not finished converting. Explain how label maturation creates this artefact, how you would restrict or adjust the evaluation, and why this matters for any alert threshold.
**Asked at:** Drift and monitoring-without-labels guides (techinterview.org MLOps guides, a DataDome write-up on monitoring models without labels, KodeKloud and NannyML-style material); commonly reported in public guides for MLOps and ML-system-design loops; search snippets only, not opened
**Say this first (1 line):** Yesterday's cohort has had only a fraction of its seven days to convert, so the observed rate is low by construction; I compare the model against a maturity-adjusted expectation, or only evaluate cohorts that have finished their window, and I set alerts on matured cohorts.

**Clarifying questions:**
- What is the conversion-delay curve (share of eventual conversions by day since click)? It converts "age 1 day" into an expected share of matured conversions.
- Is the attribution window fixed at seven days for every conversion, and does the model predict conversion within seven days? The label definition must match the window.
- Is the observed 1.5% the same cohort the model scored at 5%? Cohort and prediction date must match.
- Do delays vary by channel or product? A single curve may not fit all.
- How quickly do we need an alert? The answer sets whether we adjust or wait.

**Approach:**
1. Define the label as "converted within seven days of exposure" and write down that it is only complete once seven days have passed.
2. Compute calibration by cohort age (days since exposure). Recent cohorts will look over-predicted; older ones converge to the true level.
3. Estimate the delay curve from fully matured cohorts: share of conversions by day 1, 2, ... 7.
4. Evaluate recent cohorts against a maturity-adjusted prediction: expected observed rate = predicted rate x share matured at that age. Or exclude cohorts younger than seven days.
5. Alert rules: use only matured cohorts for the main calibration alert; use a separate "early read" with the maturity adjustment and a wider band; log cohort age with every metric.
6. Check the adjusted ratio is about 1.0; if not, then look for real miscalibration (traffic mix, tracking, model).

**Metrics:**
- Calibration ratio = sum of predicted conversions / sum of observed conversions, by cohort age.
- Maturity-adjusted ratio = observed rate / (predicted rate x matured share at age).
- Matured share at age d = share of eventual conversions that happen by day d.
- Guardrails: sampling noise (standard error of a rate) so alert bands reflect cohort size.

**Risks:**
- An alert on immature cohorts fires every day and trains people to ignore it.
- The delay curve shifts over time (channel change, a product change), which makes the adjustment wrong.
- Right-censored data also biases training sets: new rows have fewer positive labels.
- Adjusting too aggressively hides a real problem in recent data.

**What the interviewer scores:**
- Strong: names right-censoring / label maturation and shows the ratio converges with age. Weak: "the model is badly calibrated, recalibrate".
- Strong: gives a maturity-adjusted metric or an age cut-off. Weak: waits without a plan.
- Strong: links it to alert design and to training data. Weak: stops at diagnosis.

**Example:** (illustrative) The model predicts 5% and the true seven-day rate is 5%. If 30% of eventual conversions happen by day 1, yesterday's cohort shows 0.05 x 0.30 = 1.5%, and the naive ratio of predicted to observed is 3.33 (5 divided by 1.5). In a seeded simulation with 200,000 users per cohort the observed rate by cohort age (days 1 to 7) is 1.55%, 2.57%, 3.22%, 3.88%, 4.43%, 4.73% and 4.93%, so the predicted-to-observed ratio goes 3.23, 1.95, 1.55, 1.29, 1.13, 1.06, 1.01. Maturity-adjusted, yesterday's ratio is 1.03. The standard error of a 5% rate on a 20,000-user cohort is 0.0015, so an alert band is about plus or minus 0.003. Weak: "Predicted 5% versus 1.5% means we are 3.3 times off." Strong: "Cohort age is one day; expected observed is 1.5%, so the model is fine."

**Code:**
```python
import numpy as np
rng = np.random.default_rng(28)
TRUE_P = 0.05                                    # true 7-day conversion probability (model predicts 5%)
# Share of eventual conversions that have happened by day d after the click (illustrative delay curve)
cdf = np.array([0.30, 0.50, 0.65, 0.78, 0.88, 0.95, 1.00])    # day 1 ... day 7
N = 200_000
print("cohort age (days) | matured share | expected observed | observed (sim) | pred/obs")
rows = []
for age in range(1, 8):
    # each user converts w.p. TRUE_P within 7 days; conversion day drawn from the delay curve
    conv = rng.random(N) < TRUE_P
    u = rng.random(N)
    day = np.searchsorted(cdf, u) + 1             # day of conversion, 1..7
    seen = conv & (day <= age)
    obs = seen.mean()
    rows.append((age, cdf[age - 1], TRUE_P * cdf[age - 1], obs))
    print(f"{age:17d} | {cdf[age-1]:13.2f} | {TRUE_P*cdf[age-1]:17.4f} | {obs:14.4f} | {TRUE_P/obs:.2f}")
assert abs(rows[0][3] - 0.015) < 0.0015            # yesterday's cohort: about 1.5%
assert abs(rows[-1][3] - 0.05) < 0.0015           # fully matured: about 5%
# Prompt arithmetic: predicted 5% vs observed 1.5% would be a miscalibration of 3.33x if read naively
assert abs(0.05 / 0.015 - 3.333) < 0.001
# Maturity-adjusted calibration of age-1 cohort: observed / (pred * share matured)
adj = rows[0][3] / (0.05 * cdf[0])
print(f"maturity-adjusted ratio for yesterday's cohort: {adj:.2f} (1.00 means well calibrated)")
assert 0.9 < adj < 1.1
# Alert rule: only evaluate cohorts at least 7 days old; threshold uses sampling noise at that size
se = np.sqrt(TRUE_P * (1 - TRUE_P) / 20000)
print(f"for a 20,000-user cohort the standard error of a 5% rate is {se:.4f}; alert band about +/-{1.96*se:.4f}")
assert abs(se - 0.00154) < 0.00005
print("asserts passed")
```

**Output (my run):**
```text
cohort age (days) | matured share | expected observed | observed (sim) | pred/obs
                1 |          0.30 |            0.0150 |         0.0155 | 3.23
                2 |          0.50 |            0.0250 |         0.0257 | 1.95
                3 |          0.65 |            0.0325 |         0.0322 | 1.55
                4 |          0.78 |            0.0390 |         0.0388 | 1.29
                5 |          0.88 |            0.0440 |         0.0443 | 1.13
                6 |          0.95 |            0.0475 |         0.0473 | 1.06
                7 |          1.00 |            0.0500 |         0.0493 | 1.01
maturity-adjusted ratio for yesterday's cohort: 1.03 (1.00 means well calibrated)
for a 20,000-user cohort the standard error of a 5% rate is 0.0015; alert band about +/-0.0030
asserts passed
```

**Follow-ups:**
- How does this affect training? Recent rows have incomplete labels and look negative; train only on matured rows or use a survival or delayed-feedback model.
- What if the delay curve changes? Re-estimate it on a rolling window of matured cohorts and alert when it moves.
- Could you alert faster? Yes, with the maturity-adjusted ratio and a wider band, but label it an early read and confirm with the matured cohort.

**Common mistakes:**
- Evaluating calibration on cohorts younger than the window.
- Forgetting to log cohort age with the metric.
- Using one alert threshold for cohorts of different maturity.
- Training on immature rows labelled as negatives.
- Declaring recalibration needed before the cohort has matured.

### Q29 ⭐⭐ 🟡 Revenue loss from a degraded risk model is about Rs 2 lakh per day, a proper retrain and validation takes two weeks, and a business-rule patch could be live tomorrow but is crude. Explain how you would weigh the patch against waiting for the retrain, what you would test about the patch, and how you would retire it later.
**Asked at:** No interview question page located for this exact scenario; practitioner fraud and retraining guides (a Firstsource fraud-model post, a datainterview.com 'when to retrain' course page) describe the retrain-versus-rollback and adaptive-fraud themes, so editor-designed; search snippets only, not opened
**Say this first (1 line):** I put numbers on both paths: waiting costs the daily loss times the retrain days, and a patch is worth it when what it recovers, net of its own side-costs and build cost, beats that; I ship the patch only with a backtest, a shadow run, a kill switch and a sunset date.

**Clarifying questions:**
- How certain is the Rs 2 lakh a day figure, and how does it vary by day? The whole case depends on it.
- What does the patch do (extra rule, higher cut-off, manual review) and what is the side-effect, for example good customers wrongly declined?
- Can the patch be backtested on recent data before launch? A crude rule with no backtest can cost more than it saves.
- Is the retrain date firm at two weeks, or could it be faster with a reduced scope?
- Who owns the patch and who can switch it off?

**Approach:**
1. Cost of waiting = daily loss x retrain days. Here 2 lakh x 14 = Rs 28 lakh.
2. Model the patch: days it is live x (share of loss it recovers x daily loss - its daily side-cost) - build cost. Include the day or two before it is live.
3. Find the break-even recovery fraction and the sensitivity: how much must the patch recover to pay for itself, and what happens in a bad case?
4. Test the patch: backtest on the last few weeks of matured data; run it in shadow for a day or two if time allows; check segment effects and customer impact; define a rollback rule and who can use it.
5. Roll out in steps (a share of traffic first) with monitoring of loss, declines and complaints.
6. Retire it: define the exit before launch. Switch it off when the retrained model beats model plus patch on matured data, delete the code by a fixed date, and record it in the change log.
7. Do the retrain in parallel and ask whether the scope can be cut to deliver sooner.

**Metrics:**
- Net benefit of patch = (retrain days - days before live) x (loss per day x recovery fraction - side-cost per day) - build cost.
- Break-even recovery fraction = (build cost / days protected + side-cost per day) / loss per day.
- Guardrails: wrongful decline rate, approval rate, complaints, loss per day by segment.

**Risks:**
- The recovery fraction is an estimate; an untested rule may recover little and hurt customers.
- Patches become permanent and interact with the new model.
- The loss estimate may itself be wrong.
- Fast, ad hoc changes to a risk decision may bypass model-risk governance.

**What the interviewer scores:**
- Strong: quantifies both options, finds a break-even and a worst case. Weak: "patches are hacky" or "ship it".
- Strong: designs the test and the exit. Weak: no plan to remove the patch.
- Strong: respects governance (approval, audit). Weak: ignores it.

**Example:** (illustrative, Rs lakh) Waiting 14 days costs 2 x 14 = 28. A patch live from day 1 protects 13 days. If it recovers 50% of the daily loss (1.0) with a side-cost of 0.2 a day and a build cost of 1.5, the net is 13 x (1.0 - 0.2) - 1.5 = 8.9. Break-even recovery is 15.8%. At 10% recovery the patch loses 1.5; at 20% it gains 1.1; at 30%, 3.7; at 70%, 14.1. In a bad case (20% recovery, side-cost 0.4 a day) it loses 1.5. So I would ship the patch if the backtest supports recovery well above about 16% and the side-cost is controlled. Weak: "Wait for the proper retrain." Strong: "The patch pays for itself above about 16% recovery; I will backtest it, stage it, and set its sunset date."

**Code:**
```python
# Retrain-vs-patch economics (all illustrative, in Rs lakh)
loss_per_day = 2.0
retrain_days = 14
patch_live_day = 1                       # patch live after 1 day, so day 1 is unprotected
build_cost = 1.5                         # patch build and test cost
recover_frac = 0.50                      # share of the daily loss the patch removes (assumption)
side_cost = 0.2                          # extra cost per day from crude rules (e.g. wrongly declined good customers)

wait_loss = loss_per_day * retrain_days
assert wait_loss == 28.0
days_protected = retrain_days - patch_live_day
net_daily = loss_per_day * recover_frac - side_cost
benefit = days_protected * net_daily - build_cost
print(f"wait for retrain: lose {wait_loss:.1f} lakh over {retrain_days} days")
print(f"patch: protected {days_protected} days, net {net_daily:.2f} lakh/day, benefit after build cost = {benefit:.2f} lakh")
assert abs(benefit - 8.9) < 1e-9

# Break-even recovery fraction: days_protected * (loss*r - side) = build_cost
r_star = (build_cost / days_protected + side_cost) / loss_per_day
print(f"break-even recovery fraction: {r_star:.3f}")
assert abs(r_star - 0.1577) < 0.001

print("recovery  net benefit (lakh)")
for r in (0.10, 0.20, 0.30, 0.50, 0.70):
    b = days_protected * (loss_per_day * r - side_cost) - build_cost
    print(f"{r:8.0%}  {b:8.2f}")
# Worst case: patch recovers only 20% and side cost is twice as large
worst = days_protected * (loss_per_day * 0.2 - 0.4) - build_cost
print(f"worst case (20% recovery, side cost 0.4/day): {worst:.2f} lakh")
assert worst < 0
# Retirement rule: switch the patch off when the retrained model beats model+patch on matured shadow data
# (the patch is also deleted from code on a fixed date, e.g. retrain day + 7)
```

**Output (my run):**
```text
wait for retrain: lose 28.0 lakh over 14 days
patch: protected 13 days, net 0.80 lakh/day, benefit after build cost = 8.90 lakh
break-even recovery fraction: 0.158
recovery  net benefit (lakh)
     10%     -1.50
     20%      1.10
     30%      3.70
     50%      8.90
     70%     14.10
worst case (20% recovery, side cost 0.4/day): -1.50 lakh
```

**Follow-ups:**
- What if the patch has uncertain recovery? Use a range and decide on the worst case you can accept; stage the rollout to learn the real recovery in days.
- How would you shorten the retrain? Reduce scope (refit recent data on the same features), reuse the validation pipeline, and parallelise tasks.
- Who approves? The model owner and risk or compliance for decisions affecting customers, with a written change record.

**Common mistakes:**
- Shipping a patch with no backtest.
- No kill switch, owner or end date.
- Counting the patch benefit without its customer-side costs.
- Letting the patch live beside the new model unreviewed.
- Ignoring the days before the patch is live.

### Q30 ⭐⭐ 🟡 A churn model trained before a major price change now shows weaker lift, since the relationship between usage and churn seems to have changed even though input distributions look similar. Explain why this is concept drift rather than data drift, how you would confirm it with labelled data, and what training-window and feature changes you would try.
**Asked at:** Production-degradation question banks (Dataford pages such as 'if a model's performance drops in production, what is your step-by-step diagnostic process', a Prepfully 'diagnose and fix a model deployed to production that underperformed' answer page, a TryExponent production-ML course page); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** It is concept drift when the inputs look the same but the link between inputs and churn has changed; I confirm it by comparing the fitted relationship before and after on labelled data, and I fix it with newer data, regime-aware features and a shorter or weighted training window.

**Clarifying questions:**
- When exactly was the price change, and was it for all customers or a subset? That defines the regimes and a clean before/after split.
- How long until churn labels mature after the change? It tells me how much post-change labelled data exists.
- Did the price change come with other changes (plans, bundles, competitors)? Concept drift has many possible causes.
- How is lift measured (top-decile lift, precision at a retention budget)? I need a metric for the before/after comparison.
- Is price or plan information available as a feature? A model that can see price can learn the new relationship.

**Approach:**
1. Rule out data drift: compare input distributions (means, sds, PSI) before and after; also train a classifier to tell before from after inputs; if it cannot (AUC near 0.5), inputs have not moved.
2. Confirm concept drift on labelled data: evaluate the old model on post-change data and compare with its pre-change performance; then fit a fresh model on post-change data and compare coefficients (or partial dependence) with the old one.
3. Test the change formally: the usage coefficient differs by more than its sampling error, or an interaction between usage and a post-change flag is significant.
4. Check where the relationship changed: by plan, tenure, price band. The price change may bite only some customers.
5. Try fixes in order: add price or plan features and a post-change indicator with interactions; retrain on post-change data when there is enough (otherwise combine old and new with a regime flag or recency weights); shorten the training window; consider separate models per regime.
6. Validate on a post-change time split, not a random split.
7. Monitor: labelled lift weekly once labels mature, a drift check on the model's partial dependence, and a rule that major price or product changes trigger a model review.

**Metrics:**
- Top-decile lift = churn rate in the top 10% by score / overall churn rate.
- AUC on a post-change holdout.
- Usage coefficient and its standard error before and after; PSI per input.
- Guardrails: retention-campaign cost per saved customer, calibration of predicted churn.

**Risks:**
- Few post-change labels, so new models are noisy.
- The new regime may still be settling (customers react over weeks).
- Fixing with a random-split validation hides the problem.
- Retention offers based on the old relationship waste budget.

**What the interviewer scores:**
- Strong: separates covariate (data) drift from concept drift with a test for each. Weak: "distribution changed".
- Strong: confirms with labelled data and shows the changed relationship. Weak: assumes it.
- Strong: proposes regime features and window choices with trade-offs. Weak: "retrain".
- Strong: uses a time-based validation. Weak: random split.

**Example:** (illustrative simulation) Churn depends on usage with a slope of -1.0 before the price change and about -0.2 after, with a higher base level. The estimated usage coefficients are -1.00 (plus or minus 0.03) and -0.21 (plus or minus 0.02): far outside noise. The input means and sds of both features are unchanged (0.01 and -0.01 means, sd 1.0). The old model's AUC falls from 0.753 to 0.574 and its top-decile lift from 2.55 to 1.37 on post-change data; a model refit on the new regime gets AUC 0.604 and lift 1.49 on the same test, which is about the best this noisy relationship allows. With only 3,000 post-change rows, a model fit on just those reaches 0.603, so a small amount of fresh data already recovers most of the loss in this toy. Weak: "The inputs did not change, so the model should be fine." Strong: "Inputs same, relationship different: that is concept drift, and the old model's ranking is what broke."

**Code:**
```python
import numpy as np
from scipy.stats import rankdata
rng = np.random.default_rng(30)

def sigmoid(z): return 1 / (1 + np.exp(-z))
def fit(X, y, it=25):
    Xb = np.c_[np.ones(len(X)), X]; w = np.zeros(Xb.shape[1])
    for _ in range(it):
        p = sigmoid(Xb @ w); W = p * (1 - p)
        w += np.linalg.solve(Xb.T @ (Xb * W[:, None]) + 1e-6 * np.eye(len(w)), Xb.T @ (y - p))
    cov = np.linalg.inv(Xb.T @ (Xb * (sigmoid(Xb @ w) * (1 - sigmoid(Xb @ w)))[:, None]))
    return w, np.sqrt(np.diag(cov))
def pred(w, X): return sigmoid(np.c_[np.ones(len(X)), X] @ w)
def auc(y, s):
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
def decile_lift(y, s):
    top = s >= np.quantile(s, 0.9)
    return y[top].mean() / y.mean()

def make(n, usage_slope, intercept):
    usage = rng.normal(0, 1, n); tenure = rng.normal(0, 1, n)
    p = sigmoid(intercept + usage_slope * usage - 0.3 * tenure)
    return np.c_[usage, tenure], (rng.random(n) < p).astype(float)

# Before price change: churn falls with usage (slope -1.0). After: the same usage no longer protects (slope -0.2), base level higher.
Xa, ya = make(40000, -1.0, -1.5)
Xb, yb = make(40000, -0.2, -1.0)           # input distribution identical, relationship changed
Xt, yt = make(40000, -0.2, -1.0)           # fresh post-change test data

wA, seA = fit(Xa, ya); wB, seB = fit(Xb, yb)
print("coefficient on usage: before", round(wA[1], 2), "+/-", round(1.96 * seA[1], 2), "| after", round(wB[1], 2), "+/-", round(1.96 * seB[1], 2))
assert abs(wA[1] - wB[1]) > 4 * np.hypot(seA[1], seB[1])           # difference far outside noise

# Data-drift check: the input means and sds barely move
print("input mean/sd before:", Xa.mean(0).round(2), Xa.std(0).round(2), "after:", Xb.mean(0).round(2), Xb.std(0).round(2))
assert np.abs(Xa.mean(0) - Xb.mean(0)).max() < 0.03 and np.abs(Xa.std(0) - Xb.std(0)).max() < 0.03

print(f"old model on old-regime test data: AUC {auc(ya, pred(wA, Xa)):.3f}, top-decile lift {decile_lift(ya, pred(wA, Xa)):.2f}")
print(f"old model on new-regime test data: AUC {auc(yt, pred(wA, Xt)):.3f}, top-decile lift {decile_lift(yt, pred(wA, Xt)):.2f}")
print(f"refit on new regime, same test:    AUC {auc(yt, pred(wB, Xt)):.3f}, top-decile lift {decile_lift(yt, pred(wB, Xt)):.2f}")
assert auc(yt, pred(wA, Xt)) < auc(yt, pred(wB, Xt)) - 0.02
assert decile_lift(yt, pred(wA, Xt)) < decile_lift(yt, pred(wB, Xt))

# Training-window trade-off: only 3,000 post-change rows exist; combine with old data plus a regime flag
Xn, yn = Xb[:3000], yb[:3000]
w_small, _ = fit(Xn, yn)
Xmix = np.r_[Xa[:20000], Xn]; flag = np.r_[np.zeros(20000), np.ones(3000)]
Xi = np.c_[Xmix, flag, Xmix[:, 0] * flag]
w_int, _ = fit(Xi, np.r_[ya[:20000], yn])
Xti = np.c_[Xt, np.ones(len(Xt)), Xt[:, 0]]
print(f"3,000 new rows only:               AUC {auc(yt, pred(w_small, Xt)):.3f}")
print(f"old 20,000 + new 3,000 + regime x usage: AUC {auc(yt, pred(w_int, Xti)):.3f}")
assert auc(yt, pred(w_small, Xt)) > auc(yt, pred(wA, Xt))
print("asserts passed")
```

**Output (my run):**
```text
coefficient on usage: before -1.0 +/- 0.03 | after -0.21 +/- 0.02
input mean/sd before: [ 0.01 -0.01] [1. 1.] after: [ 0.01 -0.01] [1. 1.]
old model on old-regime test data: AUC 0.753, top-decile lift 2.55
old model on new-regime test data: AUC 0.574, top-decile lift 1.37
refit on new regime, same test:    AUC 0.604, top-decile lift 1.49
3,000 new rows only:               AUC 0.603
old 20,000 + new 3,000 + regime x usage: AUC 0.603
asserts passed
```

**Follow-ups:**
- Why would the inputs look the same but churn behave differently? Because the price change altered how customers respond to usage, not how much they use.
- How much post-change data is enough? Enough to estimate the changed relationship with a small standard error; in the toy, 3,000 rows were enough, but in real data with many features it takes more. Check by learning curves.
- When would you prefer separate models by regime? When the relationship differs a lot and each regime has enough data; otherwise a shared model with regime interactions borrows strength.

**Common mistakes:**
- Calling it data drift because the PSI is small, or ignoring it because the PSI is small.
- Validating on a random split that mixes regimes.
- Retraining on a window that mostly predates the change.
- Not adding the price or plan feature.
- Waiting for a large sample when a small fresh sample already shows the change.

### Q31 ⭐⭐ 🟡 An ads click model's predicted-to-observed click ratio drifted from 1.00 to 1.12 over a quarter, meaning it over-predicts, while AUC barely moved. Explain why this matters for bidding, what might cause it (traffic mix, auction changes, feedback effects), and how you would recalibrate without retraining everything.
**Asked at:** Calibration, prior-shift and threshold-review material (an arXiv paper on calibrating metrics under class-prior change, a futureagi model-versus-data-drift post, a fraud-score vendor page on reviewing thresholds); no interview page for the exact scenario, so editor-designed; search snippets only, not opened
**Say this first (1 line):** A 12% over-prediction means every bid built on the click probability is about 12% too high, and AUC cannot see it because AUC only checks order; I would find which segments drifted, then fix it with a small calibration layer on top of the model, not a full retrain.

**Clarifying questions:**
- Is the 1.12 an average over all traffic, or is it the same in every slice (placement, device, advertiser, country)? Why: one slice at 1.45 and the rest at 1.00 needs a different fix from a uniform 1.12.
- Is the ratio measured on the same impressions the model scored, with clicks counted the same way (click-fraud filtering, attribution window)? Why: a changed click definition looks exactly like drift.
- How does the bid use the probability: bid = value per click x pCTR, in a first-price or second-price auction, with pacing or a budget? Why: it decides how much money the 12% costs.
- Did anything change in the auction (reserve prices, new formats, new inventory, a competitor)? Why: it points to traffic mix or auction effects instead of model decay.
- When was the model last retrained, and is a calibration layer already in the serving path? Why: it tells me whether a patch is quick or needs new plumbing.

**Approach:**
1. Confirm it is real: recompute predicted/observed on matured clicks, check the click definition and logging, and look at it by day to see slow slide versus step.
2. Say why it matters: bid = value x pCTR, so a 12% too-high pCTR is a 12% too-high bid. In a first-price auction you pay it. In a second-price auction you mostly pay the rival's price, but you win extra impressions that are worth less than the price. Pacing and ROI reporting also go wrong.
3. Slice by placement, device, advertiser, country, format and score bucket. A reliability table (predicted bucket versus observed rate) shows whether the error is uniform or sits in the tail.
4. Find causes. Traffic mix: more of a segment where the model was always high. Auction change: new placements or position effects the training data never saw. Feedback effects: the model's own wins shape which impressions it sees (it only learns from impressions it bought). Click-definition or logging change.
5. Fix without full retrain. Fit a calibration layer on the log-odds of the old score using a recent matured window: an intercept first, then a slope, then per-segment or isotonic only if slices disagree and there is enough data. Ranking stays untouched (monotone), so AUC and the downstream ordering do not move.
6. Validate on a later holdout (ratio, reliability table, spend, ROI), ship behind a canary, and alert on the ratio per slice.
7. Plan the real fix: retrain on recent data with the missing features, keep the calibration layer as the quick lever for the next drift.

**Metrics:**
- Calibration ratio = sum of predicted click probabilities / number of observed clicks, over a matured window (numerator and denominator on the same impressions).
- Reliability table: for each predicted-probability bucket, mean predicted versus observed click rate. Also log loss and Brier score.
- Business guardrails: spend, cost per click, ROI (value / spend) per campaign, win rate, pacing error.
- AUC stays as the ranking check; it is not the calibration check.

**Risks:**
- Fitting the fix on too little data: with a 2% click rate, 2,000 clicks give a ratio standard error of about 2%.
- One global factor can make a mixed problem worse (see the Code block: 1.00 and 1.45 segments end up at 0.89 and 1.29).
- Feedback loop: a recalibrated model changes which impressions are won, so the calibration data shifts again.
- Fixing the symptom and never asking why a segment drifted.
- Label delay: very recent clicks are incomplete, so the ratio looks too high just from immature data.

**What the interviewer scores:**
- Strong: states that AUC measures ranking and calibration measures level, and ties 1.12 to money (bid, win rate, ROI).
- Strong: slices before fixing, and says a single factor is only right if the error is uniform.
- Strong: proposes a cheap post-hoc recalibration on a matured window plus a validation and canary, and a retrain as the later step.
- Weak: "retrain the model" as the first and only answer, or "AUC is fine so there is no problem".
- Cross-reference: Book 1 Part 3 has "What is model calibration and why can a model with great AUC still be badly calibrated?" and Book 1 Part 7 has "Does a ranker's predicted probability need to be calibrated? When does it matter (ads, blending scores, thresholds) and how do you fix it?".

**Example:** (illustrative numbers) 1,000 impressions with predicted CTR 2.0% each give 20 expected clicks; you observe 17.9, so the ratio is 20 / 17.9 = 1.12. You value a click at Rs 10 and bid pCTR x Rs 10, so you bid Rs 0.20 where the true value is about Rs 0.18. Weak answer: "AUC is the same, so the model is fine." Strong answer: "AUC checks order, not level. The bid is 12% high, so I would slice the ratio, fit an intercept on matured clicks, canary it, and keep the retrain for later."

**Code:**
```python
# Q31: ads click model over-predicts (ratio 1.12) while AUC is unchanged (illustrative simulation)
import numpy as np
from scipy.stats import rankdata

rng = np.random.default_rng(31)
def auc(y, s):
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
logit = lambda p: np.log(p / (1 - p))
sig = lambda z: 1 / (1 + np.exp(-z))

N = 1_200_000
p_true = np.clip(rng.lognormal(np.log(0.02), 0.8, N), 1e-4, 0.5)   # true CTR per impression
y = (rng.random(N) < p_true).astype(int)

# Drift = a constant shift in the log-odds. Find the shift that gives predicted/observed = 1.12.
lo, hi = 0.0, 0.5
for _ in range(60):
    mid = (lo + hi) / 2
    if sig(logit(p_true) + mid).mean() / y.mean() < 1.12: lo = mid
    else: hi = mid
shift = (lo + hi) / 2
p_pred = sig(logit(p_true) + shift)
ratio = p_pred.mean() / y.mean()
print(f"shift in log-odds: {shift:.3f}   predicted/observed: {ratio:.3f}")
assert abs(ratio - 1.12) < 0.01          # observed clicks are random, so allow 0.01

# AUC does not see a monotone shift at all
a0, a1 = auc(y, p_true), auc(y, p_pred)
print(f"AUC before drift {a0:.4f}   after drift {a1:.4f}")
assert abs(a0 - a1) < 1e-12

# Why bidding cares: bid = value_per_click * pCTR. Real value of an impression = value * true CTR.
v = 10.0                                   # Rs per click (illustrative)
rival = rng.lognormal(np.log(v * 0.02), 0.8, N)   # rival bids
rival_fp = rival * 0.6                              # rivals shade too
def second_price(p_used):                  # winner pays the rival bid
    win = v * p_used > rival
    return (v * p_true[win] - rival[win]).sum(), win.sum()
def first_price(p_used):                   # winner pays its own bid
    bid = 0.6 * v * p_used; win = bid > rival_fp   # shade the bid to 60% of value
    return (v * p_true[win] - bid[win]).sum(), win.sum(), bid[win].sum()
sp_ok, w_ok = second_price(p_true); sp_bad, w_bad = second_price(p_pred)
fp_ok, _, spend_ok = first_price(p_true); fp_bad, _, spend_bad = first_price(p_pred)
print(f"second price: won {w_ok} -> {w_bad}; profit Rs {sp_ok:,.0f} -> {sp_bad:,.0f}")
print(f"first price : profit Rs {fp_ok:,.0f} -> {fp_bad:,.0f}; spend Rs {spend_ok:,.0f} -> {spend_bad:,.0f}")
assert w_bad > w_ok and sp_bad < sp_ok     # extra wins are the unprofitable ones
assert fp_bad < 0.9 * fp_ok and 0.8 < sp_bad / sp_ok < 1 and spend_bad > 1.12 * spend_ok   # you pay your own inflated bid

# Recalibrate WITHOUT retraining: fit one intercept on the log-odds of the old score
# using a recent window (first 800k impressions), then test on the rest.
fit, test = slice(0, 800_000), slice(800_000, N)
z = logit(p_pred[fit]); b = 0.0
for _ in range(25):                         # Newton steps on the intercept only
    q = sig(z + b)
    b -= (q - y[fit]).sum() / (q * (1 - q)).sum()
p_fix = sig(logit(p_pred) + b)
r_fix = p_fix[test].mean() / y[test].mean()
print(f"fitted offset {b:.3f}   ratio on holdout after fix {r_fix:.3f}")
assert abs(b + shift) < 0.06 and abs(r_fix - 1) < 0.03
assert abs(auc(y, p_fix) - a1) < 1e-12      # ranking is untouched
fp_fix, _, _ = first_price(p_fix)
print(f"first-price profit after fix (Rs): {fp_fix:,.0f}")
assert fp_fix > fp_bad

# Segment trap: overall 1.12 can hide one bad segment, and one global factor then mis-fixes both.
share = np.array([0.65, 0.35]); seg_ratio = np.array([1.00, 1.45])
pred = np.array([0.020, 0.020]); obs = pred / seg_ratio
overall = (share * pred).sum() / (share * obs).sum()
print(f"overall ratio {overall:.3f}; segment ratios {seg_ratio}")
assert abs(overall - 1.12) < 0.005
after_global = seg_ratio / overall          # divide every prediction by the overall ratio
print("after one global factor, segment ratios:", np.round(after_global, 3))
assert after_global[0] < 0.9 and after_global[1] > 1.25
```

**Output (my run):**
```text
shift in log-odds: 0.128   predicted/observed: 1.120
AUC before drift 0.7197   after drift 0.7197
second price: won 599633 -> 652488; profit Rs 141,722 -> 140,959
first price : profit Rs 94,429 -> 80,257; spend Rs 141,644 -> 167,743
fitted offset -0.118   ratio on holdout after fix 1.007
first-price profit after fix (Rs): 93,405
overall ratio 1.122; segment ratios [1.   1.45]
after one global factor, segment ratios: [0.891 1.293]
```
The text above matches this run: the 12% drift moves AUC by nothing (0.7197 both), the second-price loss is small (about 0.5%, the extra wins are near break-even), the first-price loss is large (profit down about 15%, spend up about 18%), and one fitted intercept brings the holdout ratio to 1.007.

**Follow-ups:**
- Why not just retrain? It can take days, needs fresh labels, and the same drift can come back; a calibration layer is a fast, reversible patch, and you still retrain to fix the root cause.
- Intercept, Platt (intercept plus slope) or isotonic? Intercept if the error is a uniform level shift; Platt if the error grows with the score; isotonic if the shape is irregular and you have a lot of data.
- What if the ratio is 1.00 overall but wrong by segment? Then bids are mis-priced across segments even though the total looks right; calibrate per segment or add the segment feature.

**Common mistakes:** Saying AUC fine means model fine. Dividing every prediction by 1.12 without slicing. Fitting on immature clicks. Ignoring the auction type. Forgetting the feedback loop.

### Q32 ⭐⭐ 🟡 A support-ticket triage LLM is checked weekly by humans on 400 random tickets, and accuracy went from 91% (364 of 400) to 86% (344 of 400) after a product launch. Explain whether that sample size supports calling it a real decline, what you would segment by, and how you would decide what to do next.
**Asked at:** AI-era RAG and LLM quality-regression guides (Braintrust RAG-observability article, Dataiku RAG-observability post, an Apptension RAG quality guide, practitioner posts on silent AI degradation); reported as a current theme in practitioner guides, not tied to a named employer; search snippets only, not opened
**Say this first (1 line):** Five points on 400 tickets is borderline evidence (p about 0.03, and the 95% interval runs from under 1 point to about 9 points), so I would not call it a decline yet; I would split it by ticket type and by what the launch changed, and decide from that.

**Clarifying questions:**
- Are the 400 tickets a fresh random sample each week, labelled blind by the same reviewers with the same rubric? Why: a changed reviewer or rubric moves accuracy with no change in the model.
- What did the launch change: new ticket types, new languages, a new form, a new model or prompt? Why: it separates a coverage gap from real decay.
- What does "accuracy" mean here (exact category match, priority, routing)? Why: different errors cost different amounts.
- What are the costs: a mis-routed urgent ticket versus a mis-tagged low-priority one? Why: they decide how much evidence I need before acting.
- How many weekly checks have we looked at so far? Why: the more weeks you watch, the more false alarms you will see.

**Approach:**
1. Do the arithmetic. 364/400 = 91.0% and 344/400 = 86.0%. Pooled rate 0.885, standard error 0.0226, z = 2.22, two-sided p = 0.027. The interval for the drop is about 0.6 to 9.4 points. So: probably lower, but the size is very uncertain.
2. Say what the sample can and cannot do. To catch a 5-point drop with 80% power you need about 635 tickets a week, so 400 is slightly underpowered. And with weekly checks, about 1 week in 19 shows a "significant" drop by luck alone.
3. Do not stop at the p-value. The launch is not randomised, so ask what else changed: ticket mix, language, channel, reviewers.
4. Segment: by ticket type (especially new types), language, channel, customer tier, ticket length, model or prompt version, and reviewer. Compare accuracy inside each segment before and after. Report the mix effect and the within-segment effect separately.
5. Get more labels where they matter: stratify the next sample by the suspicious segments (oversample the new types), and add a second reviewer on a subset to measure labelling agreement.
6. Decide by cost, not by p-value: if the drop sits in one new ticket type, add examples and routing rules for it; if it is broad, check the model, prompt and retrieval versions; if urgent tickets are hit, fall back to a human queue for them now.

**Metrics:**
- Accuracy = correct triage decisions / tickets reviewed, per week and per segment, with a Wilson or normal interval.
- Difference = this week minus baseline, with a 95% interval; the baseline should be several weeks, not one.
- Mix decomposition: change = sum over segments of (share x change in accuracy) + sum of (change in share x accuracy). Both parts are reported.
- Guardrails: mis-routed urgent tickets per 1,000, time to first response, reviewer agreement rate.

**Risks:**
- Calling noise a decline, or calling a real decline noise because p is above 0.05.
- Simpson-type mix: the model is the same on old tickets but the launch added a hard new type (see Code).
- Reviewer drift or a rubric change.
- A sample that is not random: easy tickets are labelled faster.
- Looking at many segments and finding one that is "significant" by chance.

**What the interviewer scores:**
- Strong: does the arithmetic out loud (z, p, interval, power) and says what it means in words.
- Strong: separates statistics from causality: the launch is not an experiment, so segment and find the mechanism.
- Strong: links the decision to costs and offers a cheap next step (more labels in the suspect segment).
- Weak: "400 is too small" with no calculation, or "p < 0.05 so it dropped" with no cause.
- Cross-reference: Book 6 Part 1 has "A daily metric is down 2% and an alert fired. The metric usually moves 1.5% day to day, with a weekend dip..." as the same noise-versus-signal question for a product metric (Q37 in Part 1).

**Example:** (illustrative numbers) Before the launch: 400 old-type tickets, 364 right (91%). After: 300 old-type tickets, 276 right (92%), and 100 tickets of a new type the launch created, 68 right (68%). Total 344 of 400 = 86%. The old types did not get worse (they went up one point). The new type is 25% of the sample at 68%, which costs 0.25 x (0.68 - 0.91) = 5.75 points, and the old types add back 0.75 x 0.01 = 0.75 points; net -5 points. Weak answer: "The model degraded 5 points, retrain it." Strong answer: "The drop is borderline by itself, but split by type it is all one new ticket category. I would add labelled examples and a rule for that category and keep watching the old types."

**Code:**
```python
# Q32: is 91% -> 86% on 400 tickets a real decline? (numbers from the prompt, rest illustrative)
import math
import numpy as np

def phi_upper(z): return 0.5 * math.erfc(z / math.sqrt(2))     # P(Z > z)

a_ok, b_ok, n = 364, 344, 400
pa, pb = a_ok / n, b_ok / n
assert (pa, pb) == (0.91, 0.86)
pool = (a_ok + b_ok) / (2 * n)
se_pool = math.sqrt(pool * (1 - pool) * (2 / n))
z = (pa - pb) / se_pool
p_two = 2 * phi_upper(z)
se_diff = math.sqrt(pa * (1 - pa) / n + pb * (1 - pb) / n)
lo, hi = (pa - pb) - 1.96 * se_diff, (pa - pb) + 1.96 * se_diff
print(f"drop {pa - pb:.3f}  z {z:.2f}  two-sided p {p_two:.4f}  95% CI for the drop [{lo:.3f}, {hi:.3f}]")
assert round(z, 2) == 2.22 and 0.02 < p_two < 0.035 and 0.004 < lo < 0.008 and 0.09 < hi < 0.10

# Power: tickets per week needed to detect a 5-point drop from 91% (80% power, 5% two-sided)
za, zb = 1.96, 0.8416
need = (za + zb) ** 2 * (pa * (1 - pa) + pb * (1 - pb)) / (pa - pb) ** 2
print(f"tickets per week for 80% power at a 5-point drop: {need:.0f}")
assert 600 < need < 700

# Weekly checking: if the true accuracy never changes (89%), how often does a week
# look 'significantly lower' than the previous week at the 5% one-sided level?
rng = np.random.default_rng(32)
weeks = 20_000
x = rng.binomial(n, 0.89, size=weeks + 1)
p = x / n
z_w = (p[:-1] - p[1:]) / np.sqrt(2 * 0.89 * 0.11 / n)
false_alarm = (z_w > 1.645).mean()
print(f"false 'decline' weeks when nothing changed: {false_alarm:.3f}  (about 1 in {1 / false_alarm:.0f} weeks)")
assert 0.03 < false_alarm < 0.07

# Mix effect: launch added a new ticket type the model never saw. Same model, same skill on old types.
before = {"old types": (400, 364)}                    # (tickets, correct)
after = {"old types": (300, 276), "new type": (100, 68)}
acc = lambda d: sum(c for _, c in d.values()) / sum(t for t, _ in d.values())
print(f"before {acc(before):.2%}  after {acc(after):.2%}")
print(f"old types: {364 / 400:.1%} -> {276 / 300:.1%}   new type: {68 / 100:.0%}   new-type share {100 / 400:.0%}")
assert acc(before) == 0.91 and acc(after) == 0.86
assert 276 / 300 == 0.92 and 68 / 100 == 0.68
# exact decomposition of the 5-point drop (reference = old accuracy 91%)
new_part = 0.25 * (0.68 - 0.91)      # new ticket type
old_part = 0.75 * (0.92 - 0.91)      # old ticket types
print(f"new type {new_part:+.4f}  old types {old_part:+.4f}  total {new_part + old_part:+.4f}")
assert abs(new_part + old_part - (0.86 - 0.91)) < 1e-12
assert abs(new_part) > 5 * abs(old_part)
```

**Output (my run):**
```text
drop 0.050  z 2.22  two-sided p 0.0267  95% CI for the drop [0.006, 0.094]
tickets per week for 80% power at a 5-point drop: 635
false 'decline' weeks when nothing changed: 0.052  (about 1 in 19 weeks)
before 91.00%  after 86.00%
old types: 91.0% -> 92.0%   new type: 68%   new-type share 25%
new type -0.0575  old types +0.0075  total -0.0500
```

**Follow-ups:**
- Would you act at p = 0.027? Not on the p-value. If the new segment is a real coverage gap, act now with a cheap, reversible step; if no cause is found, collect another week of stratified labels before a costly change.
- How do you cut the false alarms from weekly checks? Use a baseline of several weeks, a control chart or a sequential test, and require the drop to hold for two weeks or to show in a named segment.
- What if reviewers disagree 8% of the time? Then accuracy against one reviewer is noisy by itself; measure agreement, use two reviewers on a subset, and treat accuracy changes smaller than the disagreement with care.

**Common mistakes:** Calling it a decline or noise from the headline numbers alone. Ignoring that the launch changed the ticket mix. Forgetting that repeated weekly checks produce false alarms. Using one baseline week. Skipping the cost of each error type.

### Q33 ⭐⭐ 🟡 A vision model that reads documents from phone photos has lost accuracy since a popular new phone with a different camera pipeline became common among your users. Explain how you would find this from the data, estimate its size, decide between augmentation, targeted data collection and a threshold change, and monitor for the next device shift.
**Asked at:** No public page found, editor-designed from standard production-ML judgement themes that the degradation guides describe in general terms; search snippets only, not opened
**Say this first (1 line):** I would tag every upload with its device model, show that accuracy fell only where the new phone is common, size the gap on a small human-labelled audit, and then pick the cheapest fix that holds: a threshold change now, targeted data and augmentation next.

**Clarifying questions:**
- Do we log the device model (EXIF or user agent) and image properties (resolution, blur, HDR or night mode, compression) with each upload? Why: without it the cause is a guess.
- Do we have labels for current uploads (human review, downstream corrections, user edits)? Why: accuracy by device needs ground truth, even a small audit.
- What is the cost of an error versus a manual review? Why: it decides between a higher threshold and more training data.
- How fast can we collect and label new-phone images and ship a retrain? Why: if it takes weeks, a threshold change is the stopgap.
- Is the model's confidence calibrated and logged? Why: a threshold change only works if the score separates good from bad reads.

**Approach:**
1. Find it from data. Slice accuracy (or a proxy such as confidence, field-level agreement, user corrections) by device model and week. A rising device share with a falling overall number, while old devices stay flat, is the signature (see Code).
2. Look for the mechanism: compare image statistics between phones (resolution, sharpness, noise, colour, aggressive smoothing, HDR, a new default format such as HEIC). Look at failure examples by hand.
3. Size it: audit a few hundred labelled uploads per group, take the accuracy gap with a bootstrap interval, then overall loss = share of new phone x gap. This also says what happens as the share grows.
4. Choose the fix:
   - Threshold change (stopgap, hours): raise the confidence threshold for this device so fewer bad reads auto-process; cost is more manual review (the Code run shows the trade).
   - Augmentation (days): simulate the new pipeline's look (sharpening, denoise, colour curve, compression) on existing images; cheap but only as good as the simulation.
   - Targeted data collection (weeks): get real images from the new phone, label them, and fine-tune; best accuracy, slowest. Use it when the gap is large and the device share is growing.
5. Check the fix on a held-out set from the new phone and on the old phones (no regression), then canary.
6. Monitor for the next shift: device-model share (alert when a new model passes a small share such as 5%), per-device confidence distribution, image-quality statistics, and a rolling labelled audit sample per device group.

**Metrics:**
- Accuracy by device group = correct reads / audited uploads in the group, with an interval.
- Overall loss = (share of the group) x (accuracy of old minus accuracy of group).
- Automation rate = uploads auto-processed / all uploads; accuracy of the auto-processed set; manual-review rate.
- Drift signals: device share, PSI or distance on confidence and image statistics per device.
- Guardrails: old-device accuracy (no regression), review queue time, cost per document.

**Risks:**
- Confounding: users with the new phone may differ (documents, lighting, app version), not only the camera.
- An audit with too few labels (300 per group gives a gap interval about plus or minus 5 points wide on each side, see Code).
- Augmentation that does not look like the real pipeline can raise training metrics and change nothing in production.
- Raising the threshold quietly overloads the manual queue.
- Over-fitting to one phone and missing the next.

**What the interviewer scores:**
- Strong: starts from the data (device tag, slice, share versus accuracy) and proves it is the device.
- Strong: gives the size as share x gap and says it will grow with adoption.
- Strong: ranks the fixes by speed and durability and states the cost of each.
- Weak: "retrain with more data" with no diagnosis, or no plan for the next device.
- Cross-reference: Book 4 Part 8 has "Monitoring models on unstructured data (images, text, embeddings) at the Part 8 level" for the monitoring side.

**Example:** (illustrative numbers) 5,000 uploads a week. Old phones read correctly 95% of the time; the new phone 80%. At a 30% share, overall accuracy = 0.70 x 0.95 + 0.30 x 0.80 = 90.5%, versus about 95% with no new phone, a 4.5-point loss. At a 2% share the loss is only 0.3 points, which is why nobody noticed. Weak answer: "Accuracy is down, retrain on recent data." Strong answer: "Overall dropped because the new phone share grew; old phones are flat. It is a 15-point gap on 30% of traffic. Today I raise the threshold for that device, this week I add augmentation, and I collect labelled images from the phone for the real fix."

**Code:**
```python
# Q33: document-reading model loses accuracy after a new phone becomes popular (illustrative simulation)
import numpy as np

rng = np.random.default_rng(33)
weeks = 12
share_new = np.linspace(0.02, 0.30, weeks)      # share of uploads from the new phone
per_week = 5000                                    # uploads per week
acc_old, acc_new = 0.95, 0.80                   # true accuracy by device group

# 1. Overall accuracy slides while old-phone accuracy is flat
n_new = rng.binomial(per_week, share_new)
ok_new = rng.binomial(n_new, acc_new)
ok_old = rng.binomial(per_week - n_new, acc_old)
overall = (ok_new + ok_old) / per_week
old_only = ok_old / (per_week - n_new)
print("week  new-phone share  overall  old phones")
for w in (0, 5, 11):
    print(f"{w:>4}  {share_new[w]:>14.0%}  {overall[w]:>7.1%}  {old_only[w]:>10.1%}")
assert overall[0] - overall[-1] > 0.03 and abs(old_only[0] - old_only[-1]) < 0.01

# 2. Size of the problem: audit 300 labelled uploads from each group (human-checked)
a_new = rng.binomial(1, acc_new, 300); a_old = rng.binomial(1, acc_old, 300)
boot = []
for _ in range(2000):
    boot.append(rng.choice(a_old, 300).mean() - rng.choice(a_new, 300).mean())
lo, hi = np.percentile(boot, [2.5, 97.5])
print(f"audit gap old-new {a_old.mean() - a_new.mean():.3f}, bootstrap 95% [{lo:.3f}, {hi:.3f}]")
assert 0.08 < lo and hi < 0.22
# expected loss at 30% share if nothing is done: 0.30 x gap
loss = 0.30 * (acc_old - acc_new)
print(f"overall accuracy loss at 30% share: {loss:.3f}")
assert abs(loss - 0.045) < 1e-9

# 3. Threshold change versus other fixes: confidence scores differ by device
conf_old_ok = rng.beta(8, 1.2, 20000); conf_old_bad = rng.beta(3, 3, 1000)
conf_new_ok = rng.beta(5, 1.5, 16000); conf_new_bad = rng.beta(3, 3, 4000)
def at(th, ok, bad):
    kept_ok = (ok >= th).sum(); kept_bad = (bad >= th).sum()
    auto = kept_ok + kept_bad
    return auto / (len(ok) + len(bad)), kept_ok / auto
print("new-phone uploads: threshold -> share auto-processed, accuracy of auto-processed")
for th in (0.50, 0.70, 0.85):
    share, acc = at(th, conf_new_ok, conf_new_bad)
    print(f"  {th:.2f}  {share:.1%}  {acc:.1%}")
s50, a50 = at(0.50, conf_new_ok, conf_new_bad); s85, a85 = at(0.85, conf_new_ok, conf_new_bad)
assert a85 > a50 and s85 < s50             # a higher threshold buys accuracy with more manual review
print(f"going 0.50 -> 0.85 sends {s50 - s85:.1%} more of new-phone uploads to manual review")

# 4. Monitoring: alert when a new device model passes 5% of traffic or its audited accuracy is low
first_alert = int(np.argmax(share_new > 0.05))
print(f"week the new phone crosses 5% share: {first_alert}  (share {share_new[first_alert]:.1%})")
assert share_new[first_alert] > 0.05 and share_new[first_alert - 1] <= 0.05
```

**Output (my run):**
```text
week  new-phone share  overall  old phones
   0              2%    94.7%       95.2%
   5             15%    92.3%       94.5%
  11             30%    90.2%       95.2%
audit gap old-new 0.137, bootstrap 95% [0.090, 0.190]
overall accuracy loss at 30% share: 0.045
new-phone uploads: threshold -> share auto-processed, accuracy of auto-processed
  0.50  85.1%  88.1%
  0.70  60.2%  94.3%
  0.85  29.7%  98.1%
going 0.50 -> 0.85 sends 55.5% more of new-phone uploads to manual review
week the new phone crosses 5% share: 2  (share 7.1%)
```
The run shows overall accuracy sliding from about 94.7% to 90.2% while old phones stay near 95%, an audit gap near 13.7 points (interval 9 to 19), and a threshold move from 0.50 to 0.85 sending about 55% more new-phone uploads to manual review in this simulation.

**Follow-ups:**
- The device tag is not logged. What now? Use proxies (image resolution, EXIF if kept, user-agent, app version), cluster images on simple statistics, and add the tag to the logs from today.
- Why not only augment? It only works if the simulation matches the real pipeline; always verify on real labelled images from the phone.
- How do you stop this recurring? A device-share alert, a per-device audit sample, and a standing process to collect labelled images when a new model passes a small share.

**Common mistakes:** Treating the overall average as the problem. Retraining on a random recent sample that has few new-phone images. Raising the threshold without costing the manual queue. Checking only the new device and missing regressions on old ones. No device-level monitoring afterwards.

### Q34 ⭐⭐ 🟡 A summarisation feature's human rating slipped from 4.3 to 3.9 out of 5 after a developer edited the shared prompt template to fix one customer complaint, and neither the prompt nor the model version was recorded with each output. Explain how you would find out what changed, what a frozen regression set and prompt versioning would have shown, and how to ship prompt edits safely.
**Asked at:** AI-era RAG and LLM quality-regression guides (Braintrust RAG-observability article, Dataiku RAG-observability post, an Apptension RAG quality guide, practitioner posts on silent AI degradation); reported as a current theme in practitioner guides, not tied to a named employer; search snippets only, not opened
**Say this first (1 line):** I would date the drop from rating timestamps, match it against the deploy and git history of the template, rebuild the old prompt and compare old versus new on a fixed set of inputs, and from now on version every prompt and gate every edit on a frozen regression set.

**Clarifying questions:**
- How are ratings collected (human raters, users, an LLM judge), and did the rubric or raters change? Why: a rating change is not always a quality change.
- Is the template in version control, and do we have deploy timestamps and old copies (git history, config store, cached copies)? Why: it decides whether I can rebuild the old prompt exactly.
- Is the template shared by several features or customers? Why: one customer's fix can hurt the others, which is probably what happened.
- Did the base model, retrieval or input mix change in the same weeks? Why: the prompt edit is the prime suspect, not the only one.
- Do we keep inputs and outputs (with consent) so I can replay them? Why: replay is the cleanest test.

**Approach:**
1. Check the number: 4.3 to 3.9 is a 0.4-point drop (9.3% of 4.3). With a 0.9 standard deviation per rating you need about 80 ratings per group to see it, so it is detectable on normal volumes. Confirm raters and rubric are unchanged.
2. Date it. With no version logged, find the change day from the daily mean ratings with a simple two-level fit (the Code run recovers the true day). Then match the date with deploy logs, git history of the template and the model provider's release notes.
3. Rebuild both prompts (old from history, new from the repo) and replay the same fixed inputs through both with the same model and settings. Judge both with the same raters or judge. Compare paired: same input, two prompts.
4. Break the change down: by input category, length and customer. A fix for one complaint usually helps one category and hurts the others.
5. Decide: keep the edit only for the segment that needs it (a separate template or a conditional section), or revert and fix the complaint another way.
6. What a frozen regression set and versioning would have shown: the paired drop (about -0.4 with an interval below zero), plus the category that improved (the complaint) and the four that got worse, before the edit ever shipped.
7. Ship prompt edits safely: prompts in version control; a version id and model id logged with every output; a frozen regression set (150 to 300 fixed inputs across categories, including every past complaint); a gate (mean must not drop and no category may fall more than a set amount); then a canary or A/B on a share of traffic, with a one-click rollback.

**Metrics:**
- Mean rating = sum of ratings / number of rated outputs, per day, per category, per prompt version.
- Paired change = mean over regression items of (new score minus old score), with a bootstrap interval.
- Category worst-case change = the lowest category mean change (gate on it, not just the average).
- Guardrails: length, refusal rate, format-valid rate, latency and cost per output.

**Risks:**
- Judge or rater drift looks like a prompt effect; use the same judge on both prompts and a fixed rubric.
- The regression set must be frozen and must cover the long tail; if it never includes the complaint type it cannot catch it.
- Overfitting the prompt to the regression set.
- A model-provider update at the same time hides which change caused the drop.
- Replay with different temperature or model settings.

**What the interviewer scores:**
- Strong: treats the prompt like code (version, test, gate, canary, rollback) and logs prompt and model version per output.
- Strong: uses paired comparison on fixed inputs and breaks the result down by category.
- Strong: dates the change from the data when versions are missing, and treats the date as a lead.
- Weak: "ask the developer to revert" with no measurement, or "we need more data".
- Cross-reference: Book 4 Part 8 has "LLM and GenAI monitoring, only at the boundary with Book 2" for the monitoring side.

**Example:** (illustrative numbers) Frozen set: 150 inputs, 30 each in five categories. The edit lifts the complaint-type category by 0.4 and lowers the others by 0.46, 0.91, 0.51 and 0.60 points in this simulation. Average change: -0.41, interval about -0.51 to -0.32. The gate (no category below -0.3) fails, so the edit would not ship as written. Weak answer: "Ratings dropped, revert the prompt." Strong answer: "Date the drop, replay old versus new on a fixed set, show it helps one category and hurts four, then ship a category-specific fix through the gate."

**Code:**
```python
# Q34: summary rating slipped 4.3 -> 3.9 after an unversioned prompt edit (illustrative simulation)
import numpy as np

rng = np.random.default_rng(34)
assert round(4.3 - 3.9, 1) == 0.4 and round((4.3 - 3.9) / 4.3, 3) == 0.093

# 1. No version was logged: find WHEN it changed from daily mean ratings (60 days, 40 rated per day)
days, per_day, change_day = 60, 40, 33
daily_mean = []
for d in range(days):
    mu = 4.3 if d < change_day else 3.9
    r = np.clip(np.round(rng.normal(mu, 0.9, per_day)), 1, 5)
    daily_mean.append(r.mean())
daily_mean = np.array(daily_mean)
def sse(k):  # two-level fit with a break before day k
    return ((daily_mean[:k] - daily_mean[:k].mean()) ** 2).sum() + ((daily_mean[k:] - daily_mean[k:].mean()) ** 2).sum()
best = min(range(5, days - 5), key=sse)
print(f"estimated change day {best} (true {change_day});  mean before {daily_mean[:best].mean():.2f}  after {daily_mean[best:].mean():.2f}")
assert abs(best - change_day) <= 2
# the date is only a lead: match it against deploy logs / git history of the template

# 2. Frozen regression set: 150 fixed inputs in 5 categories, same judge, old vs new prompt (paired)
cats = ["complaint-type", "short", "long", "technical", "legal"]
cat_of = np.repeat(np.arange(5), 30)
base = rng.normal(4.3, 0.5, 150)                    # item difficulty carried across prompts
effect = np.array([+0.6, -0.5, -0.9, -0.7, -0.6])   # the edit helps one case, hurts four
old = np.clip(base + rng.normal(0, 0.3, 150), 1, 5)
new = np.clip(base + effect[cat_of] + rng.normal(0, 0.3, 150), 1, 5)
diff = new - old
boot = [rng.choice(diff, 150).mean() for _ in range(4000)]
lo, hi = np.percentile(boot, [2.5, 97.5])
print(f"paired mean change {diff.mean():+.2f}  95% bootstrap [{lo:+.2f}, {hi:+.2f}]")
for c in range(5):
    print(f"  {cats[c]:15} {diff[cat_of == c].mean():+.2f}")
assert hi < 0 and diff[cat_of == 0].mean() > 0 and diff[cat_of == 2].mean() < -0.5
# average of the effects: (0.6 - 0.5 - 0.9 - 0.7 - 0.6) / 5
assert abs(effect.mean() - (-0.42)) < 1e-9

# 3. Why a frozen set beats waiting for live ratings: sample sizes for a 0.4 shift
sd = 0.9
n_live = 2 * (1.96 + 0.8416) ** 2 * sd ** 2 / 0.4 ** 2    # independent groups
sd_diff = diff.std(ddof=1)                                 # paired: only the prompt effect + noise
n_paired = (1.96 + 0.8416) ** 2 * sd_diff ** 2 / 0.4 ** 2
print(f"ratings needed for 80% power at a 0.4 shift: unpaired {n_live:.0f} per group, paired {n_paired:.0f} items")
assert n_live > 4 * n_paired

# 4. Ship gate: block a prompt version if any category drops more than 0.3 or the mean drops at all
def gate(d, cat, tol=0.3):
    worst = min(d[cat == c].mean() for c in range(5))
    return bool(d.mean() >= 0 and worst >= -tol)
print("gate passes for the edited prompt:", gate(diff, cat_of))
assert gate(diff, cat_of) is False and gate(np.zeros(150), cat_of) is True
```

**Output (my run):**
```text
estimated change day 33 (true 33);  mean before 4.20  after 3.83
paired mean change -0.41  95% bootstrap [-0.51, -0.32]
  complaint-type  +0.40
  short           -0.46
  long            -0.91
  technical       -0.51
  legal           -0.60
ratings needed for 80% power at a 0.4 shift: unpaired 79 per group, paired 17 items
gate passes for the edited prompt: False
```
In this run the break day is recovered exactly (33), the paired change is about -0.41 with an interval below zero, one category rose and four fell, and the paired design needs about 17 items to see a 0.4 shift where unpaired live ratings need about 79 per group.

**Follow-ups:**
- Nothing in history, the old prompt is lost. Reconstruct it from cached requests, logs or the last good outputs; if truly gone, write a candidate and judge it against old outputs for the same inputs.
- Is an LLM judge enough? As a gate yes if you calibrate it against human ratings on a sample and watch for judge drift; keep a small human check.
- How do you stop edits for one customer hurting others? Per-customer or per-category template sections, plus the gate across all categories.

**Common mistakes:** No version logged with the output. Comparing different inputs instead of paired replay. Looking at the average only and missing the category that rose. Treating a prompt as a config tweak. Gating on a set that does not contain the complaint types.

### Q35 ⭐⭐ 🔴 A model scored an AUC of 0.95 offline, but live AUC is 0.71. A review finds one feature was only populated after the outcome happened, so it leaked at training time but is empty at serving time. Explain how you would confirm leakage, quantify the damage, rebuild the evaluation to be point-in-time correct, and handle the live system while you fix it.
**Asked at:** Training-serving skew and offline-versus-online question pages (DesignGurus 'Grokking the AI System Design Interview', techinterview.org MLOps drift and feature-store guide, a Prachub ML-serving concept page); commonly reported in public guides; search snippets only, not opened
**Say this first (1 line):** An offline AUC of 0.95 that becomes 0.71 live, with one feature that only exists after the outcome, is classic target leakage; I would prove it with timestamps and an ablation, report the honest number (about the clean-model AUC), rebuild the evaluation with point-in-time joins, and switch the live system to a clean model or a rule fallback now.

**Clarifying questions:**
- Which feature is it, and which system writes it and when? Why: the write time is the proof, and it tells me what the legitimate version of the feature would be.
- What is the prediction moment (application time, transaction time, request time)? Why: every feature must be known at that moment, and nothing else counts.
- What decisions use the score today, and at what threshold? Why: an empty feature shifts every score, so the thresholds are now wrong.
- Is there a previous model or a rule set we can fall back to, and how long does a clean retrain take? Why: it decides the interim plan.
- Which other models or features share the same source table or join? Why: leakage tends to repeat through the same pipeline.

**Approach:**
1. Confirm leakage with three checks: (a) timestamps: for each row compare the feature's write time with the prediction time (in the Code run 98% of rows are written after); (b) single-feature strength: a feature that alone has AUC 0.95 for a hard problem is suspect; (c) ablation: drop it and retrain; offline AUC falls to the live level.
2. Quantify the damage. The honest performance is the clean-model AUC (0.705 in the run), not 0.95. Also compute what the live system did wrong: with the feature empty, the old model's scores collapse (mean predicted risk 0.027 versus a true rate 0.286 here), so at the old threshold almost nothing is flagged.
3. Rebuild evaluation, point-in-time correct: join features by "latest value at or before the prediction time" (an as-of join), not "latest value ever"; split by time, not at random; run a leakage test in the pipeline (feature timestamp must not be after the prediction time).
4. Handle the live system. Immediately: roll back to the last model that did not use the feature or to a rule-based fallback; or retrain without the feature and ship it behind a shadow run; recalibrate thresholds on live outcomes because the score distribution changed. Tell the business the true number and the period of exposure.
5. Fix the cause: block the post-outcome source from the feature store for training, add the leakage check to CI, and review sibling models for the same pattern.
6. Look for a legitimate substitute: a version of the signal that exists at prediction time (for example a previous-case value, or an earlier-stage field).

**Metrics:**
- Leak rate = rows where feature write time is after prediction time / all rows.
- Single-feature AUC and the offline AUC drop when the feature is removed.
- Honest AUC = AUC of a point-in-time model on a time-based holdout, and AUC on live matured labels.
- Operational: flag rate, precision and recall at the live threshold, mean score versus observed rate.

**Risks:**
- Believing the clean offline number is already good: re-check on a time split with as-of joins; other leakage may remain.
- Imputing the missing feature (zero, median) and shipping silently, which is what made the live scores collapse.
- Fixing only this feature while the join logic that caused it stays.
- Changing the threshold on the leaky model instead of replacing it.
- Late labels: live AUC is measured on matured labels only.

**What the interviewer scores:**
- Strong: proves leakage with timestamps and ablation, not only a hunch from the AUC gap.
- Strong: separates "what we reported" from "what is true" and states the exposure window.
- Strong: gives an interim plan for the live system (rollback or fallback, thresholds) before the long fix.
- Weak: "retrain the model" without recognising the feature cannot exist at serving time.
- Cross-reference: Book 4 Part 9 has "Point-in-time correct joins" for the feature-store mechanics, and Book 4 Part 1 has "Write tests that catch data leakage" for the test.

**Example:** (illustrative numbers) Offline: AUC 0.96 with the leaky feature. Without it: 0.705, the same as live (0.705 in the run). A tiny as-of join case: user 1 has feature values 100 (day 10), 200 (day 20) and 300 (day 30); the prediction is at day 22. "Latest value ever" gives 300 (a future value); as-of gives 200. Weak answer: "Retrain and hope live improves." Strong answer: "The feature is written after the outcome, so the true AUC is about 0.70. I roll back to the previous model, rebuild training with an as-of join and a time split, add a timestamp check to CI, and recalibrate thresholds."

**Code:**
```python
# Q35: a feature that exists only after the outcome leaks offline and is empty live (illustrative simulation)
import numpy as np
import pandas as pd
from scipy.stats import rankdata

rng = np.random.default_rng(35)
def auc(y, s):
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
def fit_logit(X, y, l2=1e-3, steps=40):
    Xb = np.c_[np.ones(len(X)), X]; w = np.zeros(Xb.shape[1])
    for _ in range(steps):
        p = 1 / (1 + np.exp(-Xb @ w)); g = Xb.T @ (p - y) + l2 * w
        H = (Xb * (p * (1 - p))[:, None]).T @ Xb + l2 * np.eye(len(w))
        w -= np.linalg.solve(H, g)
    return w
def score(w, X): return np.c_[np.ones(len(X)), X] @ w

N = 60_000
legit = rng.normal(size=(N, 3))
y = (legit @ np.array([0.9, 0.6, 0.4]) + rng.normal(0, 2.4, N) > 1.5).astype(int)
# leaky feature: written by the process that happens AFTER the outcome (e.g. a 'case closed' amount)
leak = y * rng.normal(1.0, 0.42, N) + (1 - y) * rng.normal(0.0, 0.42, N)
train, test = slice(0, 40_000), slice(40_000, N)

# 1. Offline with the leaky feature
X_all = np.c_[legit, leak]
w_all = fit_logit(X_all[train], y[train])
offline = auc(y[test], score(w_all, X_all[test]))
# 2. Live: the feature is empty (filled with 0 by the pipeline)
X_live = np.c_[legit, np.zeros(N)]
live = auc(y[test], score(w_all, X_live[test]))
# 3. Clean model, no leaky feature
w_cl = fit_logit(legit[train], y[train])
clean = auc(y[test], score(w_cl, legit[test]))
print(f"offline AUC (with leak) {offline:.3f}   live-like AUC (feature empty) {live:.3f}   clean model {clean:.3f}")
assert offline > 0.93 and 0.68 < live < 0.80 and clean > live - 0.02

# Confirm leakage: single-feature AUC, and ablation
print(f"single-feature AUC: leak {auc(y, leak):.3f}   best legit {max(auc(y, legit[:, j]) for j in range(3)):.3f}")
print(f"ablation: dropping the leaky feature changes offline AUC by {clean - offline:+.3f}")
assert auc(y, leak) > 0.85 and clean < offline - 0.15

# Time check: share of rows whose feature timestamp is after the prediction time
t_pred = rng.uniform(0, 100, N)
t_feat = np.where(rng.random(N) < 0.98, t_pred + rng.uniform(0.1, 5, N), t_pred - 1)   # 98% written later
after = (t_feat > t_pred).mean()
print(f"rows where the feature is written after the prediction time: {after:.1%}")
assert after > 0.97

# Point-in-time (as-of) join versus the leaky 'latest value' join
events = pd.DataFrame({"user": [1, 1, 1, 2, 2], "ts": [10, 20, 30, 15, 25], "val": [100, 200, 300, 50, 60]})
labels = pd.DataFrame({"user": [1, 2], "ts": [22, 20]})                       # prediction times
latest = events.sort_values("ts").groupby("user")["val"].last()               # leaky
asof = pd.merge_asof(labels.sort_values("ts"), events.sort_values("ts"), on="ts", by="user")
print("latest-value join:", latest.to_dict(), "  as-of join:", dict(zip(asof.user, asof.val)))
assert latest.to_dict() == {1: 300, 2: 60} and dict(zip(asof.user, asof.val)) == {1: 200, 2: 50}

# Live handling: the old leaky model's scores shift when the feature is empty
s_off = 1 / (1 + np.exp(-score(w_all, X_all[test]))); s_live = 1 / (1 + np.exp(-score(w_all, X_live[test])))
print(f"mean predicted risk offline {s_off.mean():.3f} vs live-like {s_live.mean():.3f}; true rate {y[test].mean():.3f}")
assert s_live.mean() < 0.5 * s_off.mean()
# decisions at the old threshold of 0.5: how many cases get flagged, and how many true cases are found
for name, s_ in (("offline", s_off), ("live-like", s_live)):
    f = s_ > 0.5
    print(f"{name:10} flagged {f.mean():.1%}  recall {(f & (y[test] == 1)).sum() / y[test].sum():.1%}")
assert (s_live > 0.5).mean() < 0.3 * (s_off > 0.5).mean()
```

**Output (my run):**
```text
offline AUC (with leak) 0.961   live-like AUC (feature empty) 0.705   clean model 0.705
single-feature AUC: leak 0.954   best legit 0.656
ablation: dropping the leaky feature changes offline AUC by -0.256
rows where the feature is written after the prediction time: 98.0%
latest-value join: {1: 300, 2: 60}   as-of join: {2: 50, 1: 200}
mean predicted risk offline 0.287 vs live-like 0.027; true rate 0.286
offline    flagged 27.2%  recall 81.3%
live-like  flagged 0.0%  recall 0.0%
```
The run shows the pattern in the prompt in a simulation: offline 0.961 and live-like 0.705, equal to the clean model; one feature with an AUC of 0.954 alone; 98% of rows where the feature is written after the prediction time; and the old model flagging 27.2% of cases offline but about none live-like.

**Follow-ups:**
- Could the live AUC still be hurt beyond the missing feature? Yes: the model gave the leaky feature most of its weight, so the other weights are not tuned for live; a clean retrain is usually better than the old model with the feature blanked.
- How do you prevent it? Event-time on every feature, as-of joins only, time-based splits, a CI check that fails if a feature timestamp is later than the label's prediction time, and a review of any feature with a suspiciously high single-feature AUC.
- Is it still useful as a signal? Only if a version exists at prediction time; otherwise drop it.

**Common mistakes:** Random train-test split on time-ordered data. "Latest value" joins. Filling the missing feature with zero and moving on. Reporting 0.95 for a month after the review. Fixing the threshold instead of the model.

### Q36 ⭐⭐ 🔴 A model trained on metro-city customers is launched in smaller cities and its precision falls from 62% to 48% in the new region, while the original cities hold steady. Explain how you would test whether covariate shift or a different relationship to the outcome is responsible, and whether you would reweight, add regional features, fine-tune or build a separate model.
**Asked at:** No public page found, editor-designed from standard production-ML judgement themes that the degradation guides describe in general terms; search snippets only, not opened
**Say this first (1 line):** First I would check how much of 62% to 48% a lower base rate alone explains, then use a small labelled sample from the new region to test whether reweighting the metro data to look like the new region reproduces the new precision (covariate shift) or leaves a gap (a different relationship); the answer picks the fix.

**Clarifying questions:**
- Is "precision" at a fixed threshold, and are labels in the new region defined and delayed the same way as in the metro cities? Why: a different label process looks like a different relationship.
- Do we have any labelled rows from the new region, and how many? Why: without them I can only test covariate shift, not the relationship.
- What differs in the new region: customer mix, product, channels, income, language, data sources, device? Why: it suggests features that carry the shift.
- Is the base rate of the outcome different in the new region? Why: precision falls when prevalence falls even if the model is unchanged.
- How many smaller regions are planned, and are they alike? Why: it decides one regional model versus per-region handling.

**Approach:**
1. Arithmetic first. Precision odds equal (TPR / FPR) times prevalence odds. If TPR and FPR did not change, 62% to 48% means prevalence odds fell by a factor 0.566, for example a base rate of 20% falling to 12.4%. So check the base rate before blaming the model.
2. Test covariate shift. Train a domain classifier (metro versus new region) on the features. If it separates them well, the feature distributions differ. Reweight metro rows with weights p/(1-p) from that classifier and compute the reweighted metro precision.
3. Read the result. If the reweighted metro precision is close to the actual new-region precision, the cause is covariate shift (the model is fine, the mix changed). If a gap remains, the relationship between features and outcome is different (concept shift), or the labels differ. In the simulation: scenario A (covariate shift only) leaves a 1.7-point gap, scenario B (different relationship) leaves 13.4 points.
4. Choose the fix:
   - Covariate shift only: reweight training, add or recalibrate features that carry the shift, and re-pick the threshold for the new mix; no new model needed.
   - Different relationship with a few labels: add a region flag or regional offset to the shared model, or recalibrate (cheap, uses all the data).
   - Different relationship with plenty of labels: fine-tune on the new region or build a separate model; with too few rows a separate model is worse than the metro model (the run shows 200 rows lose).
5. Check on a held-out new-region sample and confirm the metro cities do not regress; then canary.
6. Monitor per region from now on: precision on a rolling label sample, base rate, score distribution.

**Metrics:**
- Precision = true positives / flagged, per region at the same threshold; also recall and flag rate.
- Base rate = positives / cases, per region.
- Domain-classifier AUC (how separable the regions are); reweighted metro precision minus actual new-region precision (the unexplained gap).
- Log loss or calibration on the new region; guardrail: metro precision.

**Risks:**
- Importance weights can explode when regions barely overlap; clip them and check the effective sample size.
- Small labelled samples in the new region: a precision of 48% from 100 flagged cases has an interval of roughly plus or minus 10 points.
- Reweighting only fixes shift in the features you observe; unobserved differences look like concept shift.
- Different labelling (a slower or stricter review) can mimic a changed relationship.
- Both effects can be present at once.

**What the interviewer scores:**
- Strong: separates prior (base rate), covariate and concept shift, and tests them in a fixed order with cheap checks.
- Strong: names a concrete test (domain classifier plus reweighted evaluation) and what each outcome means.
- Strong: picks the fix by data availability (few labels: offset or recalibration; many: fine-tune or separate model).
- Weak: "just retrain on the new region's data" with no diagnosis and no thought about how many labels exist.
- Cross-reference: Book 4 Part 8 has "Label (prior) shift versus covariate shift in practice" and "Detecting concept drift" for the monitoring side.

**Example:** (illustrative numbers) Metro base rate 20%, new region 12.4%, same TPR and FPR: precision falls from 62% to 48% with no change in model quality. Now suppose the base rates match. You label 300 flagged cases in the new region and find 49% precision; the metro cases reweighted to look like the new region's features score 62%. The 13-point gap is a different relationship, so a regional offset or fine-tune is needed. Weak answer: "Precision fell, retrain on the new region." Strong answer: "First check the base rate, then reweight and compare; if reweighted metro still beats actual by more than the noise, the relationship differs and I add a region offset or fine-tune depending on label counts."

**Code:**
```python
# Q36: precision 62% -> 48% in smaller cities: covariate shift or a different relationship? (illustrative simulation)
import numpy as np

rng = np.random.default_rng(36)

# 0. Arithmetic first: how much of 62% -> 48% could a lower base rate explain alone?
odds = lambda p: p / (1 - p)
ratio = odds(0.48) / odds(0.62)
print(f"precision odds ratio 0.48 vs 0.62: {ratio:.3f}")
# precision odds = (TPR / FPR) x (prevalence odds); if TPR and FPR are fixed, prevalence odds must fall by that ratio
prev_new = lambda prev_old: (odds(prev_old) * ratio) / (1 + odds(prev_old) * ratio)
print(f"a base rate of 20% falling to {prev_new(0.20):.1%} gives the same precision drop")
assert abs(prev_new(0.20) - 0.1239) < 0.001

def sig(z): return 1 / (1 + np.exp(-z))
def fit(X, y, steps=30, l2=1e-3):
    Xb = np.c_[np.ones(len(X)), X]; w = np.zeros(Xb.shape[1])
    for _ in range(steps):
        p = sig(Xb @ w); g = Xb.T @ (p - y) + l2 * w
        H = (Xb * (p * (1 - p))[:, None]).T @ Xb + l2 * np.eye(len(w)); w -= np.linalg.solve(H, g)
    return w
pred = lambda w, X: sig(np.c_[np.ones(len(X)), X] @ w)

def world(shift_x, shift_rel, n=60_000):
    """metro: x ~ N(0,1) two features, y depends on x. new: x shifted (covariate) and/or coefficients changed (concept)."""
    beta = np.array([1.2, 0.8]); b0 = -2.2
    Xm = rng.normal(0, 1, (n, 2)); ym = rng.random(n) < sig(b0 + Xm @ beta)
    Xn = rng.normal(shift_x, 1, (n, 2))
    beta_n = beta * shift_rel[0]; b0n = b0 + shift_rel[1]
    yn = rng.random(n) < sig(b0n + Xn @ beta_n)
    return Xm, ym.astype(float), Xn, yn.astype(float)

def diagnose(name, shift_x, shift_rel, keep=False):
    Xm, ym, Xn, yn = world(shift_x, shift_rel)
    global LAST; LAST = (Xm, ym, Xn, yn)
    w = fit(Xm[:40_000], ym[:40_000]); th = 0.5
    flag_m = pred(w, Xm[40_000:]) > th; flag_n = pred(w, Xn) > th
    prec_m = ym[40_000:][flag_m].mean(); prec_n = yn[flag_n].mean()
    # domain classifier: can x tell the two regions apart?
    Xd = np.r_[Xm[:20_000], Xn[:20_000]]; yd = np.r_[np.zeros(20_000), np.ones(20_000)]
    wd = fit(Xd, yd); dp = pred(wd, Xd)
    # importance weights for metro rows, then reweighted metro precision on the flagged rows
    pm = pred(wd, Xm[40_000:]); wgt = pm / (1 - pm); wgt = np.clip(wgt, 0, 20)
    prec_rw = (wgt[flag_m] * ym[40_000:][flag_m]).sum() / wgt[flag_m].sum()
    print(f"{name:34} metro {prec_m:.1%}  new {prec_n:.1%}  metro reweighted to new covariates {prec_rw:.1%}")
    return prec_m, prec_n, prec_rw

a = diagnose("A covariate shift only", -1.0, (1.0, 0.0))
b = diagnose("B different relationship", 0.0, (0.85, -0.25))
# A: reweighting explains most of the new precision; B: reweighting does not
gap_a = abs(a[2] - a[1]); gap_b = abs(b[2] - b[1])
print(f"unexplained gap after reweighting: A {gap_a:.3f}, B {gap_b:.3f}")
assert gap_a < 0.03 and gap_b > 0.10

# Fix options for world B, using a small labelled sample from the new region (2,000 rows)
Xm, ym, Xn, yn = LAST
def logloss(y, p): p = np.clip(p, 1e-6, 1 - 1e-6); return -(y * np.log(p) + (1 - y) * np.log(1 - p)).mean()
Xn_tr, yn_tr, Xn_te, yn_te = Xn[:2000], yn[:2000], Xn[2000:], yn[2000:]
w_metro = fit(Xm, ym)
w_region = fit(np.c_[np.r_[Xm, Xn_tr], np.r_[np.zeros(len(Xm)), np.ones(2000)]], np.r_[ym, yn_tr])   # region flag
w_newonly = fit(Xn_tr, yn_tr)
w_new200 = fit(Xn_tr[:200], yn_tr[:200])
res = {
    "metro model as is": logloss(yn_te, pred(w_metro, Xn_te)),
    "metro + region flag (2,000 new rows)": logloss(yn_te, pred(w_region, np.c_[Xn_te, np.ones(len(Xn_te))])),
    "new-region only, 2,000 rows": logloss(yn_te, pred(w_newonly, Xn_te)),
    "new-region only, 200 rows": logloss(yn_te, pred(w_new200, Xn_te)),
}
for k, v in res.items(): print(f"  log loss on new region, {k:38} {v:.4f}")
assert res["metro + region flag (2,000 new rows)"] < res["metro model as is"]
assert res["new-region only, 2,000 rows"] < res["metro model as is"]
assert res["new-region only, 200 rows"] > res["metro model as is"]   # too few rows: worse than the metro model
```

**Output (my run):**
```text
precision odds ratio 0.48 vs 0.62: 0.566
a base rate of 20% falling to 12.4% gives the same precision drop
A covariate shift only             metro 64.5%  new 59.0%  metro reweighted to new covariates 60.7%
B different relationship           metro 62.6%  new 49.2%  metro reweighted to new covariates 62.6%
unexplained gap after reweighting: A 0.017, B 0.134
  log loss on new region, metro model as is                      0.3230
  log loss on new region, metro + region flag (2,000 new rows)   0.3167
  log loss on new region, new-region only, 2,000 rows            0.3156
  log loss on new region, new-region only, 200 rows              0.3370
```
In this simulation covariate shift alone moves precision by about 5 points and leaves a 1.7-point gap after reweighting, while a changed relationship moves it by about 13 points and leaves a 13.4-point gap. The metro-plus-region-flag and new-region-only models (2,000 rows) beat the metro model on new-region log loss; 200 rows are not enough.

**Follow-ups:**
- What if there are no labels from the new region? You can test covariate shift and prior shift only; collect a small labelled sample first (a few hundred reviewed cases is the start) and use a conservative threshold meanwhile.
- When a separate model? When the relationship differs a lot, there are enough labels (thousands), and you will maintain it; otherwise a shared model with regional features is simpler.
- How do you tell prior shift from the others? Compare base rates and calibration by region; prior shift changes precision but leaves TPR and FPR alone.

**Common mistakes:** Not checking the base rate first. Reweighting without clipping. Fine-tuning on 200 rows. Reading one precision number from a small sample as proof. Forgetting to check the original cities after the fix.

### Q37 ⭐⭐ 🔴 A team retrained a model on the last four weeks of data and it performed worse than the old one. Those four weeks included a payment outage and a heavy promotion. Explain how training-window choice, unusual events and label quality could explain this, and how you would design the retraining dataset and validation to avoid repeating it.
**Asked at:** No interview question page located for this exact scenario; practitioner fraud and retraining guides (a Firstsource fraud-model post, a datainterview.com 'when to retrain' course page) describe the retrain-versus-rollback and adaptive-fraud themes, so editor-designed; search snippets only, not opened
**Say this first (1 line):** The last four weeks were not normal weeks, so the retrain learned the outage and the promotion as if they were the new normal; I would retrain on a longer window with the outage rows removed or relabelled and the promotion marked, and validate on a time-ordered clean holdout against the old model before shipping.

**Clarifying questions:**
- How are labels defined, and what did the outage do to them (failed payments looking like defaults or abandonment)? Why: this is the likeliest way the window got corrupted.
- Which metric got worse (ranking, calibration, a business metric at a threshold), and on which holdout? Why: AUC can stay flat while the score level moves.
- How was the retrain validated: random split inside the four weeks, or a later period? Why: a random split inside the same four weeks hides the problem.
- Will promotions and outages recur (a calendar, a known event list)? Why: if the promotion recurs, the model should know about it, not forget it.
- How much older data is usable (schema, definitions stable)? Why: it sets how long the window can be.

**Approach:**
1. Diagnose before changing anything. Compare the retrain with the old model on a later clean period, by slice and by day. Check mean predicted versus observed rate, positive rate by day in the training window, feature distributions on promo and outage days.
2. Window choice. Four weeks is short and every unusual day is a large share of it. Use a longer window (for example 6 to 12 months, or all stable history), with recency weights if the relationship drifts, so one odd month cannot dominate.
3. Unusual events. Outage days: drop the rows, or relabel them if the cause is known (a failed payment is not a default). Promotion days: keep them but add a promo indicator (or an event feature), so the model can separate "promo behaviour" from "normal behaviour" and the indicator is off on normal days.
4. Label quality. Look at positive rate by day (the outage days show a spike), at label delay (recent weeks have immature labels), and at how labels are created. Only train on matured labels.
5. Validation. Time-ordered split with a clean future holdout, a second holdout that includes a past promotion, slice checks, and a champion-challenger run on live traffic. The new model must beat or match the old one on log loss, calibration and the business metric at the threshold.
6. Guardrails for the pipeline: an event calendar (outages, promos, launches), an automated check that flags days whose label rate or feature distribution is far from normal, and a rule that a retrain cannot ship if it loses to the champion.

**Metrics:**
- Log loss and Brier score (calibration-sensitive), AUC (ranking), and precision and recall at the live threshold.
- Mean predicted / mean observed rate on the holdout.
- Positive rate by day in the training window (spot corrupted days).
- Business guardrail: cost or approval rate at the live threshold.

**Risks:**
- Too long a window hides a real, recent change (concept drift): use recency weights and a drift check.
- Dropping outage days removes information about outage behaviour; mark them or relabel instead if the system must handle outages.
- A promo indicator that is set differently at serving than in training.
- The holdout shares the same unusual days (leakage in time).
- Immature labels in the most recent days.

**What the interviewer scores:**
- Strong: connects each of the three clues (window, events, labels) to a specific mechanism and shows it in data.
- Strong: a validation design that mirrors production (time split, clean future holdout, champion versus challenger).
- Strong: builds a repeatable process (event calendar, label-rate alerts), not a one-off patch.
- Weak: "use more data" with no check of label quality, or "retrain again next week".
- Cross-reference: Book 4 Part 7 has "Continuous training triggers and their guardrails" and Book 4 Part 8 has "Retraining pitfalls and feedback loops".

**Example:** (illustrative numbers) 30 weeks of data (210 days), 400 rows a day, a training window of the last 4 weeks (28 days, 11,200 rows). Five outage days in the window have a positive rate of 79%, against 31% on normal days. Those 5 days are 5/28 = 17.9% of the window (the run prints the same). The naive retrain predicts 14% too many positives on the clean test weeks (ratio 1.143) while the old model is at 0.974. Weak answer: "The new model is worse, so keep the old one forever." Strong answer: "The four-week window is dominated by an outage and a promo. I would train on 28 weeks, drop or relabel the outage days, add a promo flag, and promote only if it beats the champion on a clean later holdout."

**Code:**
```python
# Q37: retrain on the last 4 weeks, which had a payment outage and a heavy promotion (illustrative simulation)
import numpy as np
from scipy.stats import rankdata

rng = np.random.default_rng(37)
sig = lambda z: 1 / (1 + np.exp(-z))
def auc(y, s):
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
def fit(X, y, steps=30, l2=1e-3):
    Xb = np.c_[np.ones(len(X)), X]; w = np.zeros(Xb.shape[1])
    for _ in range(steps):
        p = sig(Xb @ w); g = Xb.T @ (p - y) + l2 * w
        H = (Xb * (p * (1 - p))[:, None]).T @ Xb + l2 * np.eye(len(w)); w -= np.linalg.solve(H, g)
    return w
pred = lambda w, X: sig(np.c_[np.ones(len(X)), X] @ w)
def logloss(y, p): p = np.clip(p, 1e-6, 1 - 1e-6); return -(y * np.log(p) + (1 - y) * np.log(1 - p)).mean()

# 30 weeks of daily data, 700 rows a day. Weeks 25-28 = the last four weeks used for the retrain.
days, per = 210, 400
beta = np.array([1.0, -0.8, 0.5]); b0 = -1.0
rows = []
for d in range(days):
    wk = d // 7
    promo = 24 <= wk <= 27 and (d % 7) in (2, 3, 4)           # promo days in the 4-week window
    outage = wk == 26 and (d % 7) in (0, 1, 2, 3, 4)                  # payment outage days
    X = rng.normal(0, 1, (per, 3))
    if promo: X[:, 0] += 1.5                                  # promo-driven shift in feature 0
    y = (rng.random(per) < sig(b0 + X @ beta)).astype(float)
    if outage:                                                # failed payments mislabelled as the positive class
        flip = rng.random(per) < 0.6
        y = np.where(flip, 1.0, y)
    rows.append((np.full(per, d), X, y, np.full(per, promo), np.full(per, outage)))
D = np.concatenate([r[0] for r in rows]); X = np.concatenate([r[1] for r in rows])
Y = np.concatenate([r[2] for r in rows]); P = np.concatenate([r[3] for r in rows]); O = np.concatenate([r[4] for r in rows])
print(f"outage days: {len(np.unique(D[O]))}, promo days: {len(np.unique(D[P]))}, share of training-window rows on outage days: {O[(D >= 168) & (D < 196)].mean():.1%}")

assert abs(O[(D >= 168) & (D < 196)].mean() - 5 / 28) < 1e-9
# Clean test: the next 2 weeks (days 196-209 are normal; train data end before day 196)
test = D >= 196; Xt, Yt = X[test], Y[test]
window = (D >= 168) & (D < 196)
old_w = fit(X[D < 168], Y[D < 168])                       # old model: weeks 1-24
models = {
    "old model (weeks 1-24)": old_w,
    "retrain: last 4 weeks, as is": fit(X[window], Y[window]),
    "retrain: last 4 weeks, outage days dropped": fit(X[window & ~O], Y[window & ~O]),
    "retrain: 28 weeks, outage dropped, promo flag": None,
}
# 28 weeks with outage days dropped, promo flag as a feature (set to 0 at serving on normal days)
tr = (D < 196) & ~O
Xf = np.c_[X, P.astype(float)]
w_flag = fit(Xf[tr], Y[tr])
res = {}; ratio_ = {}
for k, w in models.items():
    if w is None: p = pred(w_flag, np.c_[Xt, np.zeros(len(Xt))])
    else: p = pred(w, Xt)
    res[k] = (auc(Yt, p), logloss(Yt, p))
    print(f"{k:48} AUC {res[k][0]:.4f}  log loss {res[k][1]:.4f}  mean pred/observed {p.mean() / Yt.mean():.3f}")
    ratio_[k] = p.mean() / Yt.mean()
a_old = res["old model (weeks 1-24)"]; a_bad = res["retrain: last 4 weeks, as is"]
a_fix = res["retrain: 28 weeks, outage dropped, promo flag"]
assert a_bad[1] > a_old[1]                      # the naive retrain is worse than the old model on log loss
assert a_fix[1] <= a_old[1] + 0.003             # a careful retrain is at least as good
assert res["retrain: last 4 weeks, outage days dropped"][1] < a_bad[1]
print(f"naive retrain minus old model: log loss {a_bad[1] - a_old[1]:+.4f}")
assert ratio_["retrain: last 4 weeks, as is"] > ratio_["old model (weeks 1-24)"] + 0.02   # inflated base rate
# in the 4-week window the outage and promo days differ from normal days:
print(f"positive rate: normal window days {Y[window & ~O & ~P].mean():.3f}, outage days {Y[window & O].mean():.3f}, test {Yt.mean():.3f}")
assert Y[window & O].mean() > Y[window & ~O & ~P].mean() + 0.1
```

**Output (my run):**
```text
outage days: 5, promo days: 12, share of training-window rows on outage days: 17.9%
old model (weeks 1-24)                           AUC 0.7968  log loss 0.5015  mean pred/observed 0.974
retrain: last 4 weeks, as is                     AUC 0.7969  log loss 0.5082  mean pred/observed 1.143
retrain: last 4 weeks, outage days dropped       AUC 0.7969  log loss 0.5026  mean pred/observed 0.945
retrain: 28 weeks, outage dropped, promo flag    AUC 0.7968  log loss 0.5015  mean pred/observed 0.971
naive retrain minus old model: log loss +0.0068
positive rate: normal window days 0.309, outage days 0.793, test 0.330
```
In this run the ranking (AUC) is the same for every model (about 0.797); the damage is in calibration: the naive four-week retrain over-predicts by 14.3% and has the worst log loss (0.5082 versus 0.5015), and the careful retrain matches the old model.

**Follow-ups:**
- Why did AUC not move? The outage corrupted the level of the labels (the base rate), not the order of the features' effects; that is why a calibration check belongs next to AUC.
- Should the old model stay forever? No; keep it as the champion until a challenger wins a clean comparison, then retrain on a schedule with the event checks.
- What if the promotion repeats monthly? Then keep promo rows and keep the promo flag, and test the model on past promotions.

**Common mistakes:** Validating on a random split of the same four weeks. Training on rows from an outage unchanged. Dropping promo days when promos are part of normal business. Judging the retrain on AUC alone. No event calendar.

### Q38 ⭐⭐ 🔴 A moderation model only gets true labels for items a human reviewer sees, which are mostly those the model already scored as risky. Reported recall has stayed at 90% while user reports of missed harmful content are rising. Explain the selection bias in the monitoring metric and how you would obtain an unbiased estimate, for example with random sampling.
**Asked at:** No public page found, editor-designed from standard production-ML judgement themes that the degradation guides describe in general terms; search snippets only, not opened
**Say this first (1 line):** Recall computed only on items humans reviewed is biased, because reviewers mostly see what the model already flagged, so the metric cannot see what the model misses; I would label a random (or stratified, probability-weighted) sample of all items and estimate recall from that.

**Clarifying questions:**
- How do items reach reviewers (model flag, user report, random, policy list)? Why: each path has a different selection probability, and I need them to weight correctly.
- How is "recall" computed today: harmful items the model flagged / harmful items reviewed? Why: if the denominator is reviewed items only, it is biased by construction.
- How much review capacity do we have, and what does one review cost? Why: it bounds the size of the sample.
- Is harm prevalence low (for example 1 to 3%)? Why: rare harm makes a simple random sample expensive.
- Are the new user reports about a new kind of harm? Why: it suggests the model's blind spot is a specific type or region.

**Approach:**
1. Name the bias. Reviewers see flagged items plus a few borderline ones. Among reviewed harmful items almost all were flagged, so "flagged and harmful / reviewed and harmful" is close to 1 whatever the model misses. Harmful items with low scores are rarely reviewed, so they are missing from the denominator. That is selection bias. In the simulation: reported recall 89.4%, true recall 56.5%.
2. Corroborate with independent signals: user reports of missed content, appeals, reports by trust-and-safety staff, external audits. These are also biased, but they point in a direction (rising reports plus flat recall is the contradiction).
3. Get an unbiased estimate with a random sample: draw items uniformly from everything that was posted (including unflagged), have them reviewed blind, and compute recall as flagged-and-harmful / harmful in the sample, with a confidence interval.
4. Make it cheaper with stratified sampling and inverse-probability weights: sample the strata (flagged, borderline, low score) at different rates and weight each sampled item by 1 / its sampling probability. With the same 20,000 reviews, stratified sampling gave a standard deviation of 1.8 points versus 2.5 for simple random sampling in the run.
5. Keep it running: a small standing random sample (for example a fixed daily quota) so recall is tracked over time, by content type, region and language, and so the next retrain gets unbiased labels.
6. Use the result: find which harm types sit in the missed set, add them to training, and set thresholds using the corrected recall and precision.

**Metrics:**
- True recall = harmful items the model flagged / all harmful items, estimated from a probability sample: sum of weights of flagged harmful sampled items / sum of weights of harmful sampled items.
- Precision stays measurable on flagged items (all are reviewed).
- Reviewed-only recall (the biased one) is reported alongside, labelled as a diagnostic.
- Sample size for a 95% interval of plus or minus 3 points: about 1,049 harmful items in the sample, which is about 52,000 items at a 2% prevalence for simple random sampling (the run computes this).

**Risks:**
- Reviewers who know the model's score label differently: review blind.
- Rare harm: a small random sample may contain few harmful items and give a wide interval.
- Wrong weights: if the reviewed set mixes several routes, compute each item's selection probability correctly.
- Review cost and reviewer exposure to harmful content: cap and support reviewers.
- Time delay: harm reported later changes the label of earlier items.

**What the interviewer scores:**
- Strong: explains why the denominator is biased and that the contradiction (flat recall, rising reports) is a symptom of that.
- Strong: gives an unbiased estimate and its cost (sample size computed), and improves it with stratification and weights.
- Strong: adds a standing process and uses the sample to improve the model.
- Weak: "label more data" with no sampling design, or trusting the 90% figure.
- Cross-reference: Book 4 Part 8 has "Canary labels and label budgets" and "Retraining pitfalls and feedback loops"; Book 1 Part 7 has "Selection bias and counterfactual evaluation" (inverse propensity scoring).

**Example:** (illustrative numbers) 1,000,000 items, 2% harmful = 20,000 harmful. The model catches 56.5% of them (11,300), and misses 8,700. Reviewers see all 11,300 flagged harmful items plus a slice of borderline items that contain only about 1,350 harmful ones, so reported recall is about 11,300 / (11,300 + 1,350) = 89%. A random sample of 20,000 items finds about 400 harmful, of which 56% were flagged: recall about 56% with a standard deviation of 2.5 points. Weak answer: "Recall is 90%, so users are wrong." Strong answer: "The 90% is computed on items the model already likes. I would take a random blind sample, weight it properly, and find the real recall is about 56%."

**Code:**
```python
# Q38: moderation recall measured only on reviewed items is biased (illustrative simulation)
import numpy as np

rng = np.random.default_rng(38)
N = 1_000_000
harm = rng.random(N) < 0.02                       # 2% harmful
new_type = harm & (rng.random(N) < 0.45)          # a new kind of harm the model has not seen (45% of harm)
# model score: old-type harm scores high, new-type harm scores like ordinary content, ordinary items score low
score = np.where(harm & ~new_type, rng.beta(8, 1.5, N), np.where(new_type, rng.beta(2, 4, N), rng.beta(1.2, 6, N)))
flagged = score >= 0.6
true_recall = (flagged & harm).sum() / harm.sum()

# Review policy: all flagged items go to reviewers, plus 30% of items with score 0.3-0.6 (borderline)
mid = (score >= 0.3) & (score < 0.6)
reviewed = flagged | (mid & (rng.random(N) < 0.30))
rep_recall = (reviewed & flagged & harm).sum() / (reviewed & harm).sum()
print(f"true recall {true_recall:.3f}   reported recall (reviewed items only) {rep_recall:.3f}   reviewed {reviewed.sum():,} of {N:,}")
assert rep_recall > true_recall + 0.25 and 0.88 < rep_recall < 0.91

caught = (flagged & harm).sum(); extra = (reviewed & ~flagged & harm).sum()
print(f"harmful total {harm.sum():,}  flagged harmful {caught:,}  harmful seen by reviewers but not flagged {extra:,}")
assert abs(caught - 11_300) < 300 and abs(extra - 1_350) < 150
# Unbiased estimate 1: simple random sample of 20,000 items, reviewed by humans
def srs_estimate(n, seed):
    r = np.random.default_rng(seed); idx = r.choice(N, n, replace=False)
    h = harm[idx]; f = flagged[idx]
    return (f & h).sum() / h.sum(), h.sum()
ests = [srs_estimate(20_000, s) for s in range(200)]
e = np.array([x[0] for x in ests]); nh = np.mean([x[1] for x in ests])
print(f"SRS 20,000: mean harmful found {nh:.0f}; recall estimate mean {e.mean():.3f}, sd across repeats {e.std():.3f}")
assert abs(e.mean() - true_recall) < 0.01

# Unbiased estimate 2: stratified sample with the same budget (20,000), inverse-probability weights
strata = {"flagged": flagged, "mid": mid, "low": score < 0.3}
alloc = {"flagged": 3_000, "mid": 5_000, "low": 12_000}
def strat_estimate(seed):
    r = np.random.default_rng(seed); caught = 0.0; harm_tot = 0.0
    for k, m in strata.items():
        idx = np.flatnonzero(m); take = r.choice(idx, alloc[k], replace=False)
        w = len(idx) / alloc[k]
        h = harm[take]
        harm_tot += w * h.sum()
        if k == "flagged": caught += w * h.sum()
    return caught / harm_tot
es = np.array([strat_estimate(s) for s in range(200)])
print(f"stratified 20,000: recall estimate mean {es.mean():.3f}, sd across repeats {es.std():.3f}")
assert abs(es.mean() - true_recall) < 0.01 and es.std() < e.std()

# How many items does a +-3 point 95% interval need under simple random sampling?
prev = harm.mean()
n_harm = 1.96 ** 2 * true_recall * (1 - true_recall) / 0.03 ** 2
print(f"harmful items needed {n_harm:.0f}; sampled items needed {n_harm / prev:,.0f}")
assert 1000 < n_harm < 1100
```

**Output (my run):**
```text
true recall 0.565   reported recall (reviewed items only) 0.894   reviewed 62,333 of 1,000,000
harmful total 20,038  flagged harmful 11,323  harmful seen by reviewers but not flagged 1,337
SRS 20,000: mean harmful found 399; recall estimate mean 0.566, sd across repeats 0.025
stratified 20,000: recall estimate mean 0.565, sd across repeats 0.018
harmful items needed 1049; sampled items needed 52,352
```
The run reproduces the prompt's pattern in a simulation: reported recall 0.894 against true recall 0.565; the simple random sample (20,000 items, about 399 harmful) recovers 0.566; the stratified design recovers 0.565 with a smaller spread (0.018 versus 0.025); and about 52,000 items would be needed for plus or minus 3 points by simple random sampling.

**Follow-ups:**
- Cheaper than 52,000 reviews? Stratify by model score and oversample the low-score stratum; or run the random sample only for a few strata at a time (rolling by content type).
- Can I fix the biased metric by weighting only the reviewed items? Only if every item has a known, non-zero chance of being reviewed; items with probability zero cannot be recovered, so keep some random review for everyone.
- What if the harm is very rare? Use stratification and sample size by harmful counts (about 1,000 harmful items for plus or minus 3 points), and report the interval honestly.

**Common mistakes:** Computing recall only on reviewed items. Reviewing a random sample but showing reviewers the model score. Using the sample unweighted after a stratified draw. Treating user reports as an unbiased measure. Skipping the interval.

### Q39 ⭐⭐ 🔴 In one week three things changed together: a model release, a large marketing campaign that brought in new users, and an upstream schema update. The conversion model's metric fell 5% and everyone blames a different cause. Explain how you would attribute the drop, which analyses and rollbacks you would use to isolate each cause, and how you would run the incident.
**Asked at:** Production-degradation question banks (Dataford pages such as 'if a model's performance drops in production, what is your step-by-step diagnostic process', a Prepfully 'diagnose and fix a model deployed to production that underperformed' answer page, a TryExponent production-ML course page); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** I would freeze further changes, decompose the 5% by who (mix) and where (platform, version, feature), and then test each suspect with a targeted experiment: a holdback on the old model for the release, a segment comparison for the campaign, and null-rate checks for the schema change; only then roll back what the evidence blames.

**Clarifying questions:**
- What exactly fell: conversion rate, or a model metric such as AUC or precision? And is "5%" relative or percentage points? Why: it sets the arithmetic and the owner. I would treat it as conversion rate down 5% relative (4.00% to 3.80%).
- What are the exact timestamps of the three changes, and did they roll out gradually or at once? Why: staggered timing separates them; a simultaneous rollout needs a holdback.
- Is there a holdback, shadow traffic or a feature flag for the model release? Why: it is the cleanest way to isolate the model.
- How were campaign users acquired, and can I tag them (channel, campaign id, install date)? Why: mix effects need a cohort label.
- Which fields did the schema update change, and which features use them? Why: it points to a null-rate or unit check.

**Approach:**
1. Run it as an incident: one owner, a shared channel, a freeze on other changes, a timeline of the three changes, and a decision deadline. Rolling back a safe, reversible change early is fine if it is cheap.
2. Decompose the metric into who and what. Split users into existing and new (campaign) users and into platform and version. Mix effect: new users with a different base rate change the average with no change in the model. Rate effect: the same type of user converting differently. The identity is: change = rate change among existing + share of new x (new rate minus existing rate).
3. Isolate the model release: compare old versus new model on the same users in the same week, using a holdback or a shadow run. Use paired or randomised comparison, not before and after.
4. Isolate the schema update: null rate, unit and category changes per feature before and after; compare conversion for rows with and without the affected feature, and check training-serving skew on those features.
5. Isolate the campaign: compare campaign users with comparable organic users, and existing users before and after. If existing users are flat, the campaign is a mix effect, not a model failure.
6. Act on evidence: fix or roll back the schema issue, keep the model if the holdback is clean, and accept (and re-baseline) the mix change; then re-measure. Write a short blameless postmortem with the evidence table.

**Metrics:**
- Conversion = conversions / eligible sessions (or users); report overall and by segment.
- Contribution to change by cause, in percentage points, adding to the total (mix + existing-user rate; within rate, by platform).
- Model effect = conversion with new model minus conversion with old model in a concurrent holdback, with a confidence interval.
- Schema health: null rate and distribution per feature, rows with the feature versus null.
- Guardrails: revenue per session, latency, error rate.

**Risks:**
- Before-and-after comparisons confound all three changes.
- Simpson-like mix effects: every segment can look fine while the total drops.
- A holdback that is too small gives a confidence interval wide enough to blame anything (see Code).
- Rolling back several things at once: you learn nothing and may revert a good change.
- Attribution is not additive if the causes interact; say so.
- Blame culture: people defend their change instead of sharing data.

**What the interviewer scores:**
- Strong: a decomposition that adds up, with numbers, then a targeted test per suspect.
- Strong: knows a holdback or shadow run is the cleanest isolation and states the sample-size limit.
- Strong: runs the incident (owner, freeze, timeline, decision rule, postmortem).
- Weak: rolls back everything, or picks the most likely cause by gut.
- Cross-reference: Book 6 Part 1 has "A 12% drop in orders is concentrated in one metro city and started on a Tuesday" (Q15 in Part 1) for the metric-drop side, and Book 4 Part 8 has "Scenario: your drift dashboard fires an alert for feature X. What do you do, in order?".

**Example:** (illustrative numbers) Conversion fell from 4.00% to 3.80%. Before: 50% iOS at 4.40% and 50% Android at 3.60%. After: 35% existing iOS at 4.40%, 35% existing Android at 3.50%, 30% new campaign users at 3.45%. Existing users average 3.95% versus 4.00% before: a -0.05 point rate effect. New users convert 0.50 points below the existing average on 30% of traffic: -0.15 points mix effect. Total -0.20 points (75% mix, 25% rate). The whole rate effect is Android: 20% of Android rows have a null feature and convert at 3.0%; Android rows with the feature are flat at about 3.6%. A 10% holdback on the old model shows no difference (-0.02 points, interval -0.15 to +0.11). Weak answer: "The model release did it, roll it back." Strong answer: "Three quarters is campaign mix, a quarter is the schema bug on Android, the model is clean; I fix the null feature, keep the model, and set a campaign-specific baseline."

**Code:**
```python
# Q39: three changes in one week, conversion metric -5% (illustrative numbers, hand-checkable)
import numpy as np

# Segment table: (share, conversion %) before and after
before = {"existing iOS": (0.50, 4.40), "existing Android": (0.50, 3.60)}
after = {"existing iOS": (0.35, 4.40), "existing Android": (0.35, 3.50), "new campaign users": (0.30, 3.45)}
tot = lambda d: sum(s * r for s, r in d.values())
b, a = tot(before), tot(after)
print(f"overall conversion {b:.2f}% -> {a:.2f}%  ({a / b - 1:+.1%})")
assert round(b, 2) == 4.00 and round(a, 2) == 3.80 and round(a / b - 1, 3) == -0.05

# Decomposition: existing-user rate change + new-user mix effect
ex_b = (0.50 * 4.40 + 0.50 * 3.60) / 1.0
ex_a = (0.35 * 4.40 + 0.35 * 3.50) / 0.70
new = 3.45; s_new = 0.30
rate_effect = ex_a - ex_b                       # existing users, same people-type, before vs after
mix_effect = s_new * (new - ex_a)               # replacing 30% of traffic by users who convert lower
print(f"existing-user rate effect {rate_effect:+.3f} pp, new-user mix effect {mix_effect:+.3f} pp, sum {rate_effect + mix_effect:+.3f} pp")
assert abs(rate_effect + mix_effect - (a - b)) < 1e-9
assert abs(rate_effect - (-0.05)) < 1e-9 and abs(mix_effect - (-0.15)) < 1e-9
print(f"share of the drop: mix {mix_effect / (a - b):.0%}, existing-user rate {rate_effect / (a - b):.0%}")

# Where is the existing-user rate effect? By platform: iOS flat, Android -0.10 pp
android_drop = 3.50 - 3.60
print(f"existing Android change {android_drop:+.2f} pp; existing iOS change {4.40 - 4.40:+.2f} pp")
assert abs(0.5 * android_drop - rate_effect) < 1e-9     # all of it sits in Android

# Schema suspect: a feature became null for part of Android. Conversion with feature vs null rows
null_share, rate_null, rate_ok = 0.20, 3.00, 3.625
android_after = (1 - null_share) * rate_ok + null_share * rate_null
print(f"Android after = {android_after:.3f}% = 80% x {rate_ok}% + 20% null rows x {rate_null}%")
assert abs(android_after - 3.50) < 1e-9
print(f"Android rows WITH the feature: {rate_ok}% vs {3.60}% before (flat within noise); the drop sits in null rows")

# Model release: a 10% holdback of existing users stayed on the old model during the same week
rng = np.random.default_rng(39)
n_old, n_new, p = 100_000, 900_000, 0.0395             # true rate identical in both arms
c_old = rng.binomial(n_old, p) / n_old; c_new = rng.binomial(n_new, p) / n_new
se = np.sqrt(c_old * (1 - c_old) / n_old + c_new * (1 - c_new) / n_new)
d = c_new - c_old
print(f"holdback test: new model minus old model {d * 100:+.3f} pp, 95% CI [{(d - 1.96 * se) * 100:+.3f}, {(d + 1.96 * se) * 100:+.3f}] pp")
assert abs(d) < 0.001 and (d - 1.96 * se) < 0 < (d + 1.96 * se)
```

**Output (my run):**
```text
overall conversion 4.00% -> 3.80%  (-5.0%)
existing-user rate effect -0.050 pp, new-user mix effect -0.150 pp, sum -0.200 pp
share of the drop: mix 75%, existing-user rate 25%
existing Android change -0.10 pp; existing iOS change +0.00 pp
Android after = 3.500% = 80% x 3.625% + 20% null rows x 3.0%
Android rows WITH the feature: 3.625% vs 3.6% before (flat within noise); the drop sits in null rows
holdback test: new model minus old model -0.023 pp, 95% CI [-0.150, +0.105] pp
```

**Follow-ups:**
- What if there is no holdback? Use a staged rollback or a canary now (roll the model back for a random 10% of traffic), and use pre-period comparisons only as a hint.
- What if the effects interact (the new model is worse on new users)? Estimate the model effect separately for new and existing users in the holdback and report the interaction.
- What do you put in the postmortem? Timeline, evidence table, contribution by cause, what we changed in the release process (no simultaneous risky changes, holdbacks by default, schema contract tests).

**Common mistakes:** Rolling back all three. Comparing only before and after. Reading a segment's percentage change instead of its contribution. Ignoring mix. Letting each owner defend their own change without a shared dashboard.

### Q40 ⭐ 🟡 A fraud model's decisions block flagged transactions, so only the flagged ones gain a quick label. Meanwhile its apparent precision rises over time while missed fraud found by other channels also rises. Explain how to run a small randomised exploration slice to measure the truth, how large it needs to be, and how you would justify its cost to the business.
**Asked at:** No interview question page located for this exact scenario; practitioner fraud and retraining guides (a Firstsource fraud-model post, a datainterview.com 'when to retrain' course page) describe the retrain-versus-rollback and adaptive-fraud themes, so editor-designed; search snippets only, not opened
**Say this first (1 line):** If only flagged transactions get quick labels, the model's own metrics look better as it gets narrower, so I would add two small randomised slices: a labelled audit of unflagged traffic (to measure recall and missed fraud) and a capped release of a few flagged transactions (to measure true precision), sized by simple interval maths and priced against the fraud they uncover.

**Clarifying questions:**
- How do labels arise: analyst review of flagged items, customer disputes, chargebacks (with weeks of delay)? Why: it defines who is labelled quickly and who is not.
- Is the model's score the only gate, or do rules and other channels also block or flag? Why: it changes what "unflagged" means.
- What is the average loss per fraud transaction, the cost of one manual review, and the cost of a wrongly blocked good customer? Why: the exploration slice must be priced.
- What are the legal, risk and customer-experience limits on letting a flagged transaction through (amount caps, step-up authentication, per-customer limits)? Why: they decide the design of the release slice.
- How much traffic and how many weekly flagged cases do we have? Why: it sets how big a slice is feasible.

**Approach:**
1. Name the loop. The model is trained and judged on labels it chose, and fraud that it does not flag only shows up late through other channels. Better-looking precision on flagged cases can come with falling recall (in the run: precision 58% to 71%, recall 85% to 51%, missed fraud 768 to 2,510 a week).
2. Slice 1, audit of unflagged traffic: draw a random sample of transactions the model did not flag, label them (review, or follow-up with the customer, no extra block or release), and estimate the fraud rate among unflagged. Recall = flagged fraud / (flagged fraud + estimated unflagged fraud). This costs review time but no extra fraud loss.
3. Slice 2, capped release: for a random small share of flagged transactions, let them through (with amount caps, step-up checks or velocity limits) and record the true outcome. This gives true precision and unbiased training labels for the region the model usually blocks. It costs fraud loss, so keep it small, capped, and approved by risk.
4. Size them. Audit: n = 1.96^2 x (1-p) / (relative error^2 x p). With p = 0.25% missed-fraud rate and plus or minus 20% relative error you need about 38,000 labelled unflagged transactions. Release: n = 1.96^2 x precision x (1-precision) / 0.05^2, about 319 releases for plus or minus 5 points at 71% precision (8.6% of the 3,713 flagged that week; spread it over weeks).
5. Reduce cost: stratify the audit by score band and weight the estimate; rotate the audit across segments; start with a pilot on one segment; use step-up authentication so a released transaction still has a safety check.
6. Use the output: a recall and missed-fraud dashboard, honest thresholds, and training data that includes the unflagged and released outcomes (with their inverse sampling weights).
7. Justify the cost: compare it with the loss it measures (in the run, the slices cost about 19% of one week of missed fraud, once, and the audit can then shrink to a standing small slice).

**Metrics:**
- Audit fraud rate = fraud found in audited unflagged transactions / audited unflagged transactions; missed fraud per week = rate x unflagged volume.
- Recall = flagged fraud / (flagged fraud + estimated missed fraud).
- True precision = fraud among released flagged transactions / released flagged transactions.
- Cost of exploration = releases x precision x average loss + audited transactions x cost per review. Benefit = losses found and avoided, plus better thresholds.
- Guardrails: customer complaints, chargeback rate on the released slice, a per-customer cap.

**Risks:**
- Delay: fraud labels from disputes arrive over weeks, so recent audits are incomplete; use matured windows or follow up directly.
- Released fraud is a real loss and a regulatory and customer risk; cap amounts and use step-up checks.
- Fraudsters learn that a random slice passes; keep the sampling secret and random per transaction, not per user rule.
- Small slices give wide intervals (the sizes above are the minimum).
- Weights: forgetting to weight the exploration data when retraining re-introduces bias.

**What the interviewer scores:**
- Strong: identifies the feedback loop, with the counter-intuitive pair (precision up, recall down).
- Strong: sizes both slices with formulas and separates the cost-free audit from the costly release.
- Strong: speaks about money, risk approval and a cap, and about using the data for retraining with weights.
- Weak: "just label more data" or "retrain on more fraud", or a design with no cost estimate.
- Cross-reference: Book 4 Part 8 has "Retraining pitfalls and feedback loops" and "Design question: the monitoring system for a card-fraud model with chargeback labels that arrive 30 to 90 days late"; Book 4 Part 8 also has "Canary labels and label budgets".

**Example:** (illustrative numbers) 1,000,000 transactions a week, 0.5% fraud (about 5,000). In week 12 the model flags 3,713, of which about 2,620 are fraud (precision 70.6%) and 2,510 fraud transactions go unflagged (recall 51%). Missed-fraud rate among unflagged = 2,510 / 996,287 = 0.25%. A random audit of about 38,000 unflagged transactions finds around 96 fraud and pins the rate to within about plus or minus 20%. Weak answer: "Precision went up, so the model is improving." Strong answer: "Flagged-only labels flatter the model. I would audit a random 38,000 unflagged transactions and release a few hundred capped flagged ones, measure real recall and precision, and show that this costs about a fifth of one week of what we are missing."

**Code:**
```python
# Q40: a fraud model that only learns from what it flags; random exploration slices (illustrative simulation)
import math
import numpy as np

rng = np.random.default_rng(40)
weeks, N = 12, 1_000_000
fraud_rate = 0.005
share_B = np.linspace(0.10, 0.50, weeks)          # new evasive fraud pattern grows
fp_rate = np.linspace(0.003, 0.001, weeks)        # model gets sharper on the easy cases
catch_A, catch_B = 0.92, 0.10

rows = []
for w in range(weeks):
    n_fraud = rng.binomial(N, fraud_rate)
    nB = rng.binomial(n_fraud, share_B[w]); nA = n_fraud - nB
    tpA = rng.binomial(nA, catch_A); tpB = rng.binomial(nB, catch_B)
    fp = rng.binomial(N - n_fraud, fp_rate[w])
    tp = tpA + tpB; flagged = tp + fp
    rows.append((n_fraud, tp, fp, flagged))
rows = np.array(rows)
prec = rows[:, 1] / rows[:, 3]; rec = rows[:, 1] / rows[:, 0]
print("week  apparent precision  true recall   missed fraud")
for w in (0, 5, 11):
    print(f"{w:>4}  {prec[w]:>17.1%}  {rec[w]:>11.1%}  {rows[w, 0] - rows[w, 1]:>12,}")
assert prec[-1] > prec[0] + 0.10 and rec[-1] < rec[0] - 0.25
assert (rows[-1, 0] - rows[-1, 1]) > 2 * (rows[0, 0] - rows[0, 1])

# Exploration 1: a random audit of unflagged transactions (label only, no extra fraud loss)
w = 11
unflag = N - rows[w, 3]; missed = rows[w, 0] - rows[w, 1]; p_u = missed / unflag
def n_for_rel_error(p, rel): return 1.96 ** 2 * (1 - p) / (rel ** 2 * p)
n_aud = n_for_rel_error(p_u, 0.20)
print(f"week 12 missed-fraud rate among unflagged {p_u:.4%}; audit size for +-20% relative error: {n_aud:,.0f} labels")
assert 35_000 < n_aud < 45_000
# repeat the audit many times at that size to check the claim
est = np.array([rng.binomial(round(n_aud), p_u) / round(n_aud) for _ in range(2000)])
cover = (np.abs(est - p_u) / p_u < 0.20).mean()
print(f"share of audits within +-20% of the truth: {cover:.1%}")
assert 0.93 < cover < 0.97
# recall estimate = TP / (TP + estimated missed)
rec_hat = rows[w, 1] / (rows[w, 1] + est.mean() * unflag)
print(f"recall estimate {rec_hat:.3f} vs true {rec[w]:.3f}")
assert abs(rec_hat - rec[w]) < 0.02

# Exploration 2: release a random share of flagged transactions (with a cap) to measure true precision
flagged = rows[w, 3]; tp = rows[w, 1]
n_rel = 1.96 ** 2 * prec[w] * (1 - prec[w]) / 0.05 ** 2
print(f"flagged {flagged:,}; releases needed for +-5 points on precision: {n_rel:,.0f} ({n_rel / flagged:.1%} of flagged)")
avg_loss = 3_000                                    # Rs per fraud transaction (illustrative)
cost_release = n_rel * prec[w] * avg_loss
cost_audit_review = n_aud * 20                      # Rs 20 per review (illustrative)
loss_week = missed * avg_loss
print(f"cost of releases Rs {cost_release:,.0f}; cost of audit reviews Rs {cost_audit_review:,.0f}; weekly missed-fraud loss Rs {loss_week:,.0f}")
assert (cost_release + cost_audit_review) < 0.25 * loss_week
print(f"exploration cost is {(cost_release + cost_audit_review) / loss_week:.1%} of one week of missed fraud")
```

**Output (my run):**
```text
week  apparent precision  true recall   missed fraud
   0              58.1%        84.8%           768
   5              61.4%        68.5%         1,559
  11              70.6%        51.1%         2,510
week 12 missed-fraud rate among unflagged 0.2519%; audit size for +-20% relative error: 38,025 labels
share of audits within +-20% of the truth: 95.7%
recall estimate 0.511 vs true 0.511
flagged 3,713; releases needed for +-5 points on precision: 319 (8.6% of flagged)
cost of releases Rs 675,370; cost of audit reviews Rs 760,497; weekly missed-fraud loss Rs 7,530,000
exploration cost is 19.1% of one week of missed fraud
```

**Follow-ups:**
- Could the audit be smaller? Yes, if you accept a wider interval, or stratify by score and oversample the high-risk unflagged band; the formula shows the size is driven by the rarity of fraud.
- How do you use exploration data in retraining? Weight each item by 1 / its sampling probability, and keep a flag for "exploration" so you can check the model on it separately.
- What if risk will not allow releasing flagged transactions? Use the audit for recall, use step-up authentication or delayed settlement for the release slice, or release only low-amount, low-risk-tier flagged cases.

**Common mistakes:** Trusting precision on flagged cases alone. Sampling "randomly" by customer segment instead of by transaction. Not weighting exploration data. Pricing the slice with no comparison to the loss. Making the slice so small that the interval is useless.

### Q41 ⭐ 🔴 A classifier had a validation true-positive rate of 80% and a false-positive rate of 10%. In production without labels it flags 29% of cases as positive, where at training the positive rate was 20%. Explain how you would estimate the production prior under a label-shift assumption using the confusion-matrix approach, state the estimate, and say how you would then adjust the threshold or the model.
**Asked at:** Calibration, prior-shift and threshold-review material (an arXiv paper on calibrating metrics under class-prior change, a futureagi model-versus-data-drift post, a fraud-score vendor page on reviewing thresholds); no interview page for the exact scenario, so editor-designed; search snippets only, not opened
**Say this first (1 line):** If only the share of positives changed, the flag rate is a known mix of the true-positive and false-positive rates, so I solve 0.29 = pi x 0.80 + (1 - pi) x 0.10 and get pi = 0.19 / 0.70 = 27.1%, then I correct the threshold for that new prior.

**Clarifying questions:**
- Are the 80% TPR and 10% FPR measured on a validation set whose positive share is the 20% training prior? Why: TPR and FPR do not depend on the prior, but only if they were measured per class.
- Is the 29% a share of cases at the same threshold as validation? Why: a different cut gives a different TPR and FPR pair.
- What changed in the world (new channel, new region, a campaign)? Why: label shift assumes only the class mix moved. If the features of each class also moved, the formula is wrong.
- How many production cases is the 29% based on? Why: it sets the width of the interval around the estimate.
- Is the score calibrated? Why: it decides whether I move the threshold with the odds correction or have to recalibrate.
- Can I get a small random labelled sample now? Why: it is the only direct check of the estimate.

**Approach:**
1. Name the assumption: label shift, meaning P(y) moves and P(x | y) does not. Then the classifier's TPR and FPR stay at 0.80 and 0.10.
2. Write the flag rate as a mix: q = pi x TPR + (1 - pi) x FPR. Solve: pi = (q - FPR) / (TPR - FPR) = (0.29 - 0.10) / 0.70 = 0.271.
3. Sanity check: at the training prior 0.20 I would expect 0.20 x 0.80 + 0.80 x 0.10 = 24% flagged. I see 29%, so the extra 5 points of flags are the shift. The 20% in the prompt is the prior, not the training flag rate, so I do not compare 29% with 20%.
4. Put an interval on it. With 10,000 cases the flag rate has a standard error of 0.45 points, and dividing by TPR - FPR = 0.70 gives about 0.65 points on the prior.
5. Adjust the decisions. For a calibrated model, multiply the odds by w = (0.271 / 0.729) / (0.20 / 0.80) = 1.49. A 0.50 cut on the adjusted probability equals a 0.40 cut on the old probability.
6. Check the assumption: if I can get even a few hundred random labels, compare the estimate with the sample, and check feature drift within each predicted class.

**Metrics:**
- Estimated prior pi = (q - FPR) / (TPR - FPR); q = flagged cases / all scored cases.
- Precision at the new prior = pi x TPR / q. Recall stays at TPR under this assumption.
- Odds multiplier w = [pi / (1 - pi)] / [pi0 / (1 - pi0)].
- Guardrails: the formula needs TPR > FPR, the interval around pi, and a check that the estimate is between 0 and 1.

**Risks:**
- The formula assumes P(x | y) is unchanged. If the false-positive rate also drifted, the estimate is biased (see the code: FPR 0.14 would give 31%).
- A noisy TPR - FPR in the denominator magnifies noise when the classifier is weak.
- Treating 29% as the new prior by itself ignores that part of the 29% is false positives.
- Moving the threshold on an uncalibrated score.

**What the interviewer scores:**
- Strong: writes the mixing equation and solves it by hand; states the label-shift assumption out loud.
- Strong: separates "estimate the prior" from "change the decision", and gives an interval.
- Strong: says what breaks the method and how to check it with a small random label sample.
- Weak: "the positive rate went from 20% to 29%", reading the flag rate as the prior.
- Weak: retrains first without asking whether the classes changed or only their mix.

**Example:** (illustrative numbers) TPR 0.80, FPR 0.10, flag rate 0.29. pi = 0.19 / 0.70 = 0.271. Precision was 0.20 x 0.80 / 0.24 = 66.7% at the old prior and is 0.271 x 0.80 / 0.29 = 74.9% now, so the model is not worse, the cases are more often positive. Weak answer: "29% are positive now." Strong answer: "About 27%, give or take a point; I would adjust the odds by 1.49 and verify on a small random labelled sample."

**Code:**
```python
# Q41: label-shift estimate (confusion-matrix / BBSE style). Illustrative numbers.
import numpy as np
tpr, fpr = 0.80, 0.10
flag_rate = 0.29          # production share flagged positive (no labels)
train_prior = 0.20

# flag_rate = pi*TPR + (1-pi)*FPR  ->  pi = (flag_rate - FPR) / (TPR - FPR)
pi = (flag_rate - fpr) / (tpr - fpr)
print(f"estimated production prior = {pi:.4f}")
assert abs(pi - 0.19/0.70) < 1e-12 and round(pi, 3) == 0.271

# naive reading would say 29% positive; flag rate at the training prior would have been:
exp_flag_train = train_prior*tpr + (1-train_prior)*fpr
print(f"expected flag rate at prior 0.20 = {exp_flag_train:.3f} (observed {flag_rate})")
assert abs(exp_flag_train - 0.24) < 1e-12

# precision before and after the shift (TPR, FPR assumed unchanged)
prec_old = train_prior*tpr/exp_flag_train
prec_new = pi*tpr/flag_rate
print(f"precision at prior 0.20 = {prec_old:.3f}, at prior {pi:.3f} = {prec_new:.3f}")
assert round(prec_old, 3) == 0.667 and round(prec_new, 3) == 0.749

# prior-odds correction for calibrated probabilities
w = (pi/(1-pi)) / (train_prior/(1-train_prior))
print(f"odds multiplier w = {w:.3f}")
assert round(w, 3) == 1.490
t_old = 0.5
# adjusted p' = p*w/(p*w+1-p); p' >= 0.5  <=>  p >= 1/(1+w)
t_equiv = 1/(1+w)
print(f"a 0.50 cut on adjusted probability = {t_equiv:.3f} on the old probability")
assert round(t_equiv, 3) == 0.402
p = t_equiv; assert abs(p*w/(p*w+1-p) - 0.5) < 1e-12

# uncertainty: n production cases, bootstrap of the flag rate
rng = np.random.default_rng(41)
n = 10_000
flags = rng.random(n) < flag_rate
boots = []
for _ in range(2000):
    fr = rng.choice(flags, n).mean()
    boots.append((fr - fpr)/(tpr - fpr))
lo, hi = np.percentile(boots, [2.5, 97.5])
print(f"n={n}: prior 95% interval ({lo:.3f}, {hi:.3f})")
se = np.sqrt(flag_rate*(1-flag_rate)/n)/(tpr-fpr)
print(f"analytic SE = {se:.4f}")
assert 0.0055 < se < 0.0075 and lo < 0.271 < hi

# check the method on simulated data where we know the truth (true prior 0.2714)
true_pi = 0.19/0.70
y = rng.random(200_000) < true_pi
pred = np.where(y, rng.random(y.size) < tpr, rng.random(y.size) < fpr)
est = (pred.mean() - fpr)/(tpr - fpr)
print(f"simulation: flag rate {pred.mean():.3f}, estimate {est:.3f}, truth {true_pi:.3f}")
assert abs(est - true_pi) < 0.01
# if the class-conditionals also moved, the estimate is wrong: FPR drifts to 0.14
pred2 = np.where(y, rng.random(y.size) < tpr, rng.random(y.size) < 0.14)
est2 = (pred2.mean() - fpr)/(tpr - fpr)
print(f"with FPR secretly 0.14 the same formula says {est2:.3f} (truth {true_pi:.3f})")
assert est2 > true_pi + 0.04
```

**Output (my run):**
```text
estimated production prior = 0.2714
expected flag rate at prior 0.20 = 0.240 (observed 0.29)
precision at prior 0.20 = 0.667, at prior 0.271 = 0.749
odds multiplier w = 1.490
a 0.50 cut on adjusted probability = 0.402 on the old probability
n=10000: prior 95% interval (0.262, 0.288)
analytic SE = 0.0065
simulation: flag rate 0.291, estimate 0.273, truth 0.271
with FPR secretly 0.14 the same formula says 0.312 (truth 0.271)
```

**Follow-ups:**
- What if the model is not calibrated? Recalibrate first on recent labels, or fit the new prior with an EM step on the scores; the odds multiplier is only right for calibrated probabilities.
- Why not retrain? Label shift changes the prior, not the relationship, so a threshold or odds correction is cheaper and reversible. See also Q9 in this part (precision fell because the fraud rate fell).

**Common mistakes:** Reading the flag rate as the prior. Forgetting that false positives are part of the 29%. No uncertainty on the estimate. Applying the method when the features themselves moved. Moving the cut on uncalibrated scores.

### Q42 ⭐ 🔴 A model's accuracy loses roughly 0.3 percentage points each week after training, each percentage point is worth about Rs 4 lakh per week, and a retrain costs Rs 6 lakh. Explain how you would model the cost of decay against the cost of retraining to choose a cadence, show the rough optimum, and name the assumptions (linear decay, constant stakes) that would break it.
**Asked at:** No interview question page located for this exact scenario; practitioner fraud and retraining guides (a Firstsource fraud-model post, a datainterview.com 'when to retrain' course page) describe the retrain-versus-rollback and adaptive-fraud themes, so editor-designed; search snippets only, not opened
**Say this first (1 line):** Add the cost of retraining to the cost of running an ageing model, divide by the cycle length, and pick the cadence that minimises cost per week; with these numbers that is about every 3 weeks, costing roughly Rs 3.8 lakh a week.

**Clarifying questions:**
- Does a retrain restore the fresh accuracy, or does it only catch part of the drop? Why: a partial reset shifts the optimum.
- Is the Rs 6 lakh all-in (compute, review, deployment, risk of a bad release)? Why: people time and incident risk are often left out.
- Is the 0.3 pp per week measured or assumed? Why: the whole answer rests on that slope.
- Is the Rs 4 lakh per point constant through the year? Why: festival weeks multiply the stakes.
- Can retraining be automated at low marginal cost? Why: cheap retraining shortens the optimal cycle.

**Approach:**
1. Loss rate: 0.3 pp per week x Rs 4 lakh per pp = Rs 1.2 lakh per week for each week of model age. Call it k.
2. In a cycle of T weeks, week j has average age j - 0.5, so decay cost = k x (0.5 + 1.5 + ... ) = k x T^2 / 2 = 0.6 T^2.
3. Cost per cycle = 6 + 0.6 T^2. Cost per week = 6 / T + 0.6 T.
4. Minimise: the two terms are equal when T = sqrt(6 / 0.6) = sqrt(10) = 3.16 weeks. Minimum cost = 2 x sqrt(6 x 0.6) = Rs 3.79 lakh per week.
5. Round to whole weeks: 3 weeks gives 3.80, 4 weeks gives 3.90, 2 weeks gives 4.20. The curve is flat near the minimum, so 3 to 4 weeks is fine; do not argue about decimals.
6. Turn it into a rule: retrain when the accumulated loss since the last retrain reaches the retrain cost, as a trigger, rather than by the calendar alone.

**Metrics:**
- Cost per week = (retrain cost + sum of decay losses in the cycle) / T.
- Decay loss in week j = k x (j - 0.5) with k = slope in pp per week x value per pp.
- Guardrails: accuracy floor, validation pass on each retrain, and the observed decay slope tracked monthly.

**Risks:**
- Decay is rarely linear: a shock (new product, outage) causes a step, so a monitored trigger beats a fixed cadence.
- Constant stakes: festival season makes k bigger; T* scales as 1 / sqrt(k), so doubling the stakes shortens the cycle by 1.41 times (to 2.2 weeks).
- Retrain cost is not flat: a 4x cost doubles the cycle (to 6.3 weeks).
- Each retrain has a risk of a worse model; that is a cost term I have left out of the Rs 6 lakh.
- The decay slope may be an artefact of label delay (see Q28 in this part).

**What the interviewer scores:**
- Strong: writes the cost per week and solves for T analytically, then rounds.
- Strong: states the assumptions and how each moves the answer (square-root rule).
- Strong: converts the optimum into a trigger.
- Weak: "retrain weekly to be safe" with no cost comparison.
- Weak: mixes up the cost per cycle and per week.

**Example:** (illustrative numbers) Retrain every 3 weeks: cost = (6 + 1.2 x (0.5 + 1.5 + 2.5)) / 3 = (6 + 5.4) / 3 = Rs 3.80 lakh per week. Every 4 weeks: (6 + 9.6) / 4 = 3.90. Every week: 6.60. Never retraining for 26 weeks averages Rs 15.6 lakh per week. Weak answer: "retrain as often as possible". Strong answer: "About every 3 to 4 weeks, and sooner if the measured decay speeds up."

**Code:**
```python
# Q42: retrain cadence from decay cost vs retrain cost. Illustrative numbers.
import numpy as np
decay_pp_per_week = 0.3
value_per_pp = 4.0      # Rs lakh per week per percentage point
retrain_cost = 6.0      # Rs lakh per retrain

k = decay_pp_per_week*value_per_pp          # loss rate grows 1.2 lakh/week each week
print(f"loss grows by Rs {k:.1f} lakh per week, per week of age")
assert abs(k - 1.2) < 1e-12

def avg_cost(T):
    # week j of a cycle is j-0.5 weeks old on average, loss = k*(j-0.5); sum_{j=1..T} = k*T^2/2
    weeks = np.arange(1, T+1)
    decay = (k*(weeks-0.5)).sum()
    assert abs(decay - k*T*T/2) < 1e-9
    return (retrain_cost + decay)/T

for T in range(1, 9):
    print(f"retrain every {T} wk: Rs {avg_cost(T):.2f} lakh/week")
best = min(range(1, 13), key=avg_cost)
T_star = (2*retrain_cost/k)**0.5
c_star = (2*retrain_cost*k)**0.5
print(f"continuous optimum T* = sqrt(2R/k) = {T_star:.2f} weeks, cost {c_star:.2f} lakh/week")
assert best == 3 and abs(T_star - 3.162) < 0.001 and abs(c_star - 3.795) < 0.001
assert round(avg_cost(3), 2) == 3.80 and round(avg_cost(4), 2) == 3.90 and round(avg_cost(2), 2) == 4.20

# never retraining: loss grows without bound; after 26 weeks
print(f"never retrain, week 26: loss that week Rs {k*25.5:.1f} lakh; average over 26 wk Rs {k*26/2:.1f} lakh/week")
assert abs(k*26/2 - 15.6) < 1e-9

# assumption breaks: decay is not linear, e.g. a step at week 5 after a shock
def cost_step(T, step_week=5, step_pp=2.0):
    w = np.arange(1, T+1)-0.5
    loss = k*w + np.where(w > step_week, step_pp*value_per_pp, 0.0)
    return (retrain_cost + loss.sum())/T
bestS = min(range(1, 13), key=cost_step)
print("with an extra 2 pp step after week 5, best cadence (whole weeks):", bestS,
      f"cost {cost_step(bestS):.2f}")
# stakes double (e.g. festival season): value_per_pp 8 -> T* shrinks by sqrt(2)
k2 = decay_pp_per_week*8.0
print(f"stakes double: T* = {(2*retrain_cost/k2)**0.5:.2f} weeks")
assert abs((2*retrain_cost/k2)**0.5 - T_star/2**0.5) < 1e-9
# cost rises 4x if retrain costs 24: T* doubles
print(f"retrain cost 4x: T* = {(2*24/k)**0.5:.2f} weeks")
assert abs((2*24/k)**0.5 - 2*T_star) < 1e-9
# slope uncertainty: 0.2 and 0.4 pp per week
for slope in (0.2, 0.4):
    kk = slope*value_per_pp
    print(f"slope {slope} pp/week: T* = {(2*retrain_cost/kk)**0.5:.2f} weeks")
assert abs((2*retrain_cost/(0.2*4))**0.5 - 3.873) < 0.001 and abs((2*retrain_cost/(0.4*4))**0.5 - 2.739) < 0.001
```

**Output (my run):**
```text
loss grows by Rs 1.2 lakh per week, per week of age
retrain every 1 wk: Rs 6.60 lakh/week
retrain every 2 wk: Rs 4.20 lakh/week
retrain every 3 wk: Rs 3.80 lakh/week
retrain every 4 wk: Rs 3.90 lakh/week
retrain every 5 wk: Rs 4.20 lakh/week
retrain every 6 wk: Rs 4.60 lakh/week
retrain every 7 wk: Rs 5.06 lakh/week
retrain every 8 wk: Rs 5.55 lakh/week
continuous optimum T* = sqrt(2R/k) = 3.16 weeks, cost 3.79 lakh/week
never retrain, week 26: loss that week Rs 30.6 lakh; average over 26 wk Rs 15.6 lakh/week
with an extra 2 pp step after week 5, best cadence (whole weeks): 3 cost 3.80
stakes double: T* = 2.24 weeks
retrain cost 4x: T* = 6.32 weeks
slope 0.2 pp/week: T* = 3.87 weeks
slope 0.4 pp/week: T* = 2.74 weeks
```

**Follow-ups:**
- What if decay is concave (fast at first, then slows)? The optimum moves later, because early weeks cost most; fit the real curve from backtests.
- How would you handle uncertainty in the slope? Take a range such as 0.2 to 0.4 pp; T* moves by the square root of the slope: 0.2 pp gives 3.9 weeks and 0.4 pp gives 2.7 weeks, so the cadence stays between about 3 and 4 weeks.

**Common mistakes:** Forgetting the retrain cost is paid every cycle. Using end-of-cycle age instead of average age. Treating the optimum as exact. Ignoring step changes. Assuming a retrain always restores full accuracy.

### Q43 ⭐ 🔴 After a credit-scoring model was published and people learned what moves the score, applicants began gaming a few features and the score lost power. Explain this as performativity or Goodhart's law, how you would detect it, what features and monitoring are more robust, and how model transparency trades off against gaming risk.
**Asked at:** No public page found, editor-designed from standard production-ML judgement themes that the degradation guides describe in general terms; search snippets only, not opened
**Say this first (1 line):** Once the score is used to decide things about people, people change the inputs to move the score, so the feature stops measuring what it measured (Goodhart's law); I detect it from shifts in the gameable features and a weaker link to outcomes, and I lean on features that are costly to fake.

**Clarifying questions:**
- Which features are public or easy to change, and at what cost to the applicant? Why: gameability is about cost, not visibility.
- Was the scoring logic or feature list published, or only inferred? Why: it decides how fast and how widely gaming spreads.
- Do we get outcome labels for the people who gamed? Why: without outcomes I can only see the inputs shift, not the loss of power.
- Is there a legal duty to give reasons for decisions? Why: transparency may be required, so I design around it instead of removing it.
- What does it cost the lender when the model is gamed (default loss) versus when it blocks good applicants? Why: it sets how defensive to be.

**Approach:**
1. Name it: the model is performative. Publishing it changes behaviour, so the data it later learns from is no longer the data it was built on. Goodhart: a measure that becomes a target stops being a good measure.
2. Detect from inputs: for each feature track its distribution, the share of values at "good-looking" edges, and the gap between a gameable feature and a hard-to-fake one for the same person (declared balance versus repayment history).
3. Detect from outcomes: the feature's correlation with default (or its coefficient) weakens as the cohort matures, while the score improves. A better score with worse realised defaults is the signature.
4. Respond: shift weight to features that are costly or slow to fake (verified repayment history, bureau data, cash-flow from bank statements), cap the influence of any single gameable feature, use monotone constraints and rate-of-change checks.
5. Keep a refresh rhythm and a holdout of unpublished signals, so a model that is attacked can be replaced quickly.
6. Transparency: explain reasons at the level the law needs, but not the weights; give actionable reasons that match real creditworthiness (improving them helps both sides), and use human review for edge cases.

**Metrics:**
- Per-feature PSI against the pre-publication distribution; share of applicants at a threshold edge.
- Feature-outcome link: correlation or AUC of that feature alone, by cohort month.
- Gap statistic: mean(gameable feature standardised - hard feature standardised).
- Guardrails: approval rate, default rate on matured loans, and complaint rate.

**Risks:**
- Defaults are labelled months later, so outcome evidence is slow; the input signals come first.
- Dropping a useful feature because a few people game it loses real signal.
- Hiding everything harms fairness and trust; publishing everything invites gaming.
- Tighter rules push applicants to new tricks; it is an ongoing contest.

**What the interviewer scores:**
- Strong: gives the mechanism (feedback from the score to the inputs) and both input-side and outcome-side detection.
- Strong: picks robust features by cost to fake and states the trade-off with transparency.
- Strong: notes label delay and says what to watch before labels arrive.
- Weak: "retrain on new data" (that trains on the gamed data).
- Weak: "make the model a secret", ignoring explanation duties.

**Example:** (illustrative simulation) The model's AUC for predicting default was 0.791 with two features. After 60% of applicants inflate the cheap feature, it falls to 0.705. A model on the hard-to-fake feature alone had 0.727 before and 0.730 after: weaker on day one, but it does not decay, and it wins once gaming is heavy enough. The cheap feature's mean moved from -0.01 to 1.49 and its link to default weakened (correlation -0.395 to -0.255). Weak answer: "retrain it." Strong answer: "Watch the gameable inputs and their link to outcomes, and move weight to costly-to-fake signals."

**Code:**
```python
# Q43: gaming of a published scorecard. Illustrative simulation.
import numpy as np
from scipy.optimize import minimize
from scipy.stats import rankdata
rng = np.random.default_rng(43)
n = 40_000
risk = rng.normal(size=n)                       # latent creditworthiness
default = rng.random(n) < 1/(1+np.exp(2.0 + 1.5*risk))   # higher risk value -> fewer defaults
# features: x_hard is costly to fake (repayment history), x_easy is cheap to fake (declared balance)
x_hard = risk + rng.normal(0, 1.0, n)
x_easy = risk + rng.normal(0, 0.5, n)
def feats(xh, xe): return np.column_stack([np.ones(len(xh)), xh, xe])

def fit(X, y):
    def nll(b):
        z = X@b
        return np.mean(np.logaddexp(0, z) - y*z)
    return minimize(nll, np.zeros(X.shape[1]), method="BFGS").x
def auc(score, y):   # AUC for predicting y=1
    r = rankdata(score); n1 = y.sum(); n0 = len(y)-n1
    return (r[y == 1].sum() - n1*(n1+1)/2)/(n1*n0)

b_full = fit(feats(x_hard, x_easy), default.astype(float))
b_hard = fit(feats(x_hard, np.zeros(n))[:, :2], default.astype(float))
print("weights full model (const, hard, easy):", np.round(b_full, 2))

# after publication: 60% of applicants inflate the easy feature (the model reads them as safer)
m = 40_000
risk2 = rng.normal(size=m)
d2 = rng.random(m) < 1/(1+np.exp(2.0 + 1.5*risk2))
xh2 = risk2 + rng.normal(0, 1.0, m)
xe2 = risk2 + rng.normal(0, 0.5, m)
gamers = rng.random(m) < 0.6
xe2_g = xe2 + gamers*rng.uniform(1.5, 3.5, m)    # inflation unrelated to true risk
before = auc(feats(x_hard, x_easy)@b_full, default.astype(int))
after = auc(feats(xh2, xe2_g)@b_full, d2.astype(int))
hard_only_after = auc(feats(xh2, xe2_g)[:, :2]@b_hard[:2], d2.astype(int))
hard_only_before = auc(feats(x_hard, x_easy)[:, :2]@b_hard[:2], default.astype(int))
print(f"full model AUC before {before:.3f} after gaming {after:.3f}")
print(f"hard-feature-only model AUC before {hard_only_before:.3f} after {hard_only_after:.3f}")
assert after < before - 0.03
assert hard_only_before < before        # robustness costs some power today
assert abs(hard_only_after - hard_only_before) < 0.01   # but it does not decay
assert hard_only_after > after            # and wins once gaming starts

# detection: the easy feature's distribution moves and its link to the outcome weakens
print(f"mean easy feature before {x_easy.mean():.2f}, after {xe2_g.mean():.2f}")
corr_b = np.corrcoef(x_easy, default)[0, 1]; corr_a = np.corrcoef(xe2_g, d2)[0, 1]
print(f"corr(easy, default) before {corr_b:.3f}, after {corr_a:.3f}")
assert xe2_g.mean() > x_easy.mean() + 0.5 and abs(corr_a) < abs(corr_b)
# gap between easy and hard features: gamers show easy >> hard
gap_b = (x_easy - x_hard).mean(); gap_a = (xe2_g - xh2).mean()
print(f"mean(easy - hard) before {gap_b:.2f}, after {gap_a:.2f}")
assert gap_a > gap_b + 0.5
```

**Output (my run):**
```text
weights full model (const, hard, easy): [-1.87 -0.24 -0.92]
full model AUC before 0.791 after gaming 0.705
hard-feature-only model AUC before 0.727 after 0.730
mean easy feature before -0.01, after 1.49
corr(easy, default) before -0.395, after -0.255
mean(easy - hard) before -0.00, after 1.49
```

**Follow-ups:**
- Is all gaming bad? No. If changing the feature really reduces risk (paying bills on time), gaming it helps. The problem is features that can be changed without changing risk.
- Related question in this part: Q38 (selection bias in monitoring labels) matters here too, since rejected applicants have no outcomes.

**Common mistakes:** Retraining directly on gamed data. Treating a better score as better performance. Assuming secrecy fixes it. Dropping every visible feature. Forgetting that outcomes arrive late.

### Q44 ⭐ 🔴 A shared embedding model was upgraded by the platform team, and three downstream models that consume its vectors each lost between 2 and 6 points of accuracy without any code change of their own. Explain the dependency chain problem, how you would detect it, and what versioning, contracts and canary practices the platform team should adopt.
**Asked at:** Upstream schema and silent feature-pipeline failure write-ups (Towards AI schema-migration post, RisingWave feature-pipeline observability, ActiveWizards Kafka schema-evolution post, dataexpert.io schema-drift post); practitioner posts rather than interview banks, so scenario is editor-designed; search snippets only, not opened
**Say this first (1 line):** The three models depend on the exact coordinate system of the old embedding, so a new embedding model silently changes what every input number means; I would detect it with a per-consumer regression check on a frozen set, and ask the platform team for versioned embeddings, contracts and a staged rollout.

**Clarifying questions:**
- Did the platform team replace vectors in place, or serve both versions? Why: in-place means every consumer changed on the same day.
- Did the dimension, normalisation or tokenisation change? Why: a shape change fails loudly, while a same-shape change fails silently.
- Are the three models fine-tuned on the old vectors, or do they use them as frozen inputs? Why: it decides whether a quick fix (alignment) or a retrain is needed.
- Who owns the frozen evaluation sets? Why: without consumer-owned tests, nobody sees the loss.
- Can I get a paired sample of the same items in both spaces? Why: pairs allow a cheap alignment fix.

**Approach:**
1. Frame the dependency chain: platform embedding -> feature store -> three models -> products. The platform team tested the embedding on its own benchmark and called it better. Consumers were never in that test.
2. Confirm the cause: re-score a frozen validation set using the old vectors and the new vectors, with the same model. If accuracy drops only with the new vectors, the embedding is the cause. Check the vector statistics too (norm, mean, cosine to the old vector for the same item).
3. Contain: pin the old embedding version for the three consumers (roll back the dependency, not the consumer code).
4. Repair: retrain each consumer on the new vectors, or learn a small alignment map from paired items (orthogonal Procrustes) as a bridge while retraining.
5. Prevent it: versioned embeddings with a version tag stored with every vector, side-by-side serving for a deprecation window, a compatibility contract (dimension, normalisation, a published cosine-similarity-to-previous report), and a canary with per-consumer gates.
6. Process: consumers register a frozen test with the platform team; an upgrade can only be promoted if every registered consumer stays within an agreed tolerance, for example 1 point.

**Metrics:**
- Per-consumer accuracy delta on a frozen set = accuracy(new vectors) - accuracy(old vectors).
- Mean cosine similarity between old and new vectors for the same items.
- Gate: block promotion if any consumer's delta is below -1 point.
- Guardrail: share of traffic on each embedding version.

**Risks:**
- Averaging across consumers hides one badly hit model.
- The old space may not be reproducible later if the old model is deleted; keep it.
- An alignment map only works if the new space is roughly a linear transformation of the old one.
- Mixing versions in one index is a separate failure (see Q23 in this part).

**What the interviewer scores:**
- Strong: describes this as an interface change with no interface contract.
- Strong: re-scores with old versus new vectors to isolate the cause.
- Strong: proposes consumer-owned tests, version tags and staged rollout, not "be careful".
- Weak: debugging each downstream model separately.
- Weak: blames the platform team without a process fix.

**Example:** (illustrative simulation) A consumer scores 85.6% accuracy on the old vectors. If the new space is a rotation of the old one by 0.4 (arbitrary units), the unchanged consumer scores 84.7%; at 0.8 it scores 81.7%; at 1.2 it scores 79.0%; a full re-spacing gives 67.2%. After a Procrustes alignment from 500 paired items, accuracy returns to 85.6%. This is a pure rotation, so the recovery is easy; real upgrades are not pure rotations, so alignment is a bridge only. A 1-point gate blocks the 1.2 case (drop 6.6 points) and passes the 0.4 case (drop 0.9). Weak answer: "each team should retrain." Strong answer: "Version the embedding, test each consumer before promotion, and pin until they have moved."

**Code:**
```python
# Q44: upstream embedding upgrade breaks consumers. Illustrative simulation.
import numpy as np
from scipy.optimize import minimize
rng = np.random.default_rng(44)
d, n = 16, 6000
Z = rng.normal(size=(n, d))                      # "true" semantic factors
w_true = rng.normal(size=d)
y = (Z@w_true + rng.normal(0, 1.0, n) > 0).astype(float)
E_old = Z + rng.normal(0, 0.3, (n, d))           # v1 embedding

from scipy.linalg import expm
def new_space(E, theta, rng):
    # v2 = v1 rotated by a random rotation of size theta (a different, equally good space)
    A = rng.normal(size=(d, d)); A = A - A.T
    A = A/np.linalg.norm(A, 2)
    return E@expm(theta*A)

def fit(X, y):
    X1 = np.column_stack([np.ones(len(X)), X])
    f = lambda b: np.mean(np.logaddexp(0, X1@b) - y*(X1@b))
    return minimize(f, np.zeros(X1.shape[1]), method="L-BFGS-B").x
def acc(b, X, y):
    X1 = np.column_stack([np.ones(len(X)), X])
    return np.mean(((X1@b) > 0) == (y == 1))

tr, te = slice(0, 4000), slice(4000, n)
b = fit(E_old[tr], y[tr])
a0 = acc(b, E_old[te], y[te])
print(f"consumer on v1 vectors: accuracy {a0:.3f}")
res = {}
for frac in (0.4, 0.8, 1.2, 3.0):
    E_new = new_space(E_old, frac, np.random.default_rng(7))
    res[frac] = acc(b, E_new[te], y[te])
    print(f"v2 = {frac} rotation, old consumer unchanged: accuracy {res[frac]:.3f}")
assert res[0.4] > res[0.8] > res[1.2] > res[3.0]      # the bigger the change, the bigger the loss
assert a0 - res[3.0] > 0.15                   # full re-spacing is near-chance
# alignment on a small paired sample (orthogonal Procrustes) recovers most of it, without retraining
E_new = new_space(E_old, 3.0, np.random.default_rng(7))
idx = slice(0, 500)
U, _, Vt = np.linalg.svd(E_new[idx].T@E_old[idx]); R = U@Vt          # maps new -> old
acc_aligned = acc(b, (E_new@R)[te], y[te])
print(f"after Procrustes alignment from 500 paired items: accuracy {acc_aligned:.3f}")
assert a0 - acc_aligned < 0.01
# canary gate: per-consumer accuracy drop vs frozen eval set, block above 1 point
gate = 0.01
for frac in (0.4, 1.2):
    E_new = new_space(E_old, frac, np.random.default_rng(7))
    drop = a0 - acc(b, E_new[te], y[te])
    print(f"gate at {gate:.0%}: rotation {frac} -> drop {drop:.3f} -> {'BLOCK' if drop > gate else 'pass'}")
```

**Output (my run):**
```text
consumer on v1 vectors: accuracy 0.856
v2 = 0.4 rotation, old consumer unchanged: accuracy 0.847
v2 = 0.8 rotation, old consumer unchanged: accuracy 0.817
v2 = 1.2 rotation, old consumer unchanged: accuracy 0.790
v2 = 3.0 rotation, old consumer unchanged: accuracy 0.672
after Procrustes alignment from 500 paired items: accuracy 0.856
gate at 1%: rotation 0.4 -> drop 0.009 -> pass
gate at 1%: rotation 1.2 -> drop 0.066 -> BLOCK
```

**Follow-ups:**
- Why not freeze embeddings forever? You can lose real quality gains; the point is controlled migration with dual serving.
- What would you put in the contract? Dimension, normalisation, version id, a changelog with similarity-to-previous, deprecation date and a named consumer list.

**Common mistakes:** Replacing vectors in place. Testing only the platform's own benchmark. No version tag on stored vectors. Rolling back consumer code that did not change. Assuming a same-shape upgrade is compatible.

### Q45 ⭐ 🔴 A team monitors an LLM app with an LLM-as-judge that scored 4.2 last month and 4.5 this month, but a human spot-check of 100 outputs shows no improvement. Explain how the judge itself can drift or be biased, how you would calibrate it against human labels, and what governance you would put around automated quality scores.
**Asked at:** AI-era RAG and LLM quality-regression guides (Braintrust RAG-observability article, Dataiku RAG-observability post, an Apptension RAG quality guide, practitioner posts on silent AI degradation); reported as a current theme in practitioner guides, not tied to a named employer; search snippets only, not opened
**Say this first (1 line):** An LLM judge is a measuring instrument that can drift and can have biases (it likes long answers, its own style, a particular position), so a score going up is not quality going up until I have checked the judge against human labels and a frozen anchor set.

**Clarifying questions:**
- Did the judge model, its prompt or its rubric change between the two months? Why: a changed instrument makes the two scores incomparable.
- Did the application's outputs change in length or style (a prompt edit, a new model)? Why: judges often reward length and fluency.
- How were the 100 human outputs sampled and how many raters scored them? Why: 100 samples are noisy and rater disagreement matters.
- Is the judge a different model family from the one being judged? Why: a judge tends to prefer its own family's style.
- What decisions hang on this score (release gate, bonus, dashboard)? Why: higher stakes need stricter governance.

**Approach:**
1. Check the human check can see a change: with a rating spread of 0.9 and 100 samples per month, the standard error of the difference is 0.127, so the 95% half-width is about 0.25. A true gain of 0.3 would be detected only about 65% of the time. So "no improvement" from 100 humans is weak evidence, not proof.
2. Check the instrument: score a frozen anchor set (same outputs, fixed rubric) every month with the same judge version. A change on the anchor set means the judge moved.
3. Check biases: regress the human score on the judge score plus suspect nuisance variables (length, position, format). A negative length coefficient means the judge over-rewards length.
4. Calibrate: build a human-labelled set of a few hundred items covering both months and all segments, with two raters and an agreement figure. Fit a mapping from judge score to human score, report correlation, and apply the length adjustment.
5. Re-estimate the change: use the adjusted judge, or a larger human sample, and report the interval.
6. Governance: pin and log the judge version and prompt, refresh the human calibration on a schedule, report the judge with its agreement figure, never use it alone for a release gate, and re-calibrate on any change of judge or application.

**Metrics:**
- Judge-human agreement: Spearman correlation, or Cohen's kappa on pass/fail, on a labelled set.
- Anchor drift = mean judge score on the frozen anchor set this month - last month.
- Length coefficient c in human = a + b x judge + c x (words - baseline).
- Adjusted change = change in the length-adjusted judge score, with an interval.
- Guardrail: the judge's score on known-bad outputs stays low.

**Risks:**
- Calibrating on last month's labels misses a bias that appears only in the new style of output.
- Using the same model as generator and judge inflates scores.
- Humans are noisy too; the human label is a reference, not the truth.
- A fixed anchor set goes stale as the product changes.

**What the interviewer scores:**
- Strong: treats the judge as an instrument and tests it with an anchor set and bias regression.
- Strong: notices that 100 human ratings have limited power, in numbers.
- Strong: sets governance (versions, schedule, never the sole gate).
- Weak: trusts the judge because it is "an LLM".
- Weak: dismisses the judge entirely instead of calibrating it.

**Example:** (illustrative simulation, same story as the prompt with different levels) True quality is flat at 3.87 to 3.89. A prompt edit makes answers 30 words longer and the judge adds 0.01 per word, so its mean rises from 4.09 to 4.34. Over 400 labelled items the judge-human Spearman is 0.81, so the judge is useful, but the length coefficient is -0.0067 per word. Length-adjusted, the judge moves from 3.89 to 3.90 (+0.01), matching the human truth (+0.01). Weak answer: "Quality improved, the judge says 4.5." Strong answer: "The judge may be rewarding length; I calibrate against humans and use an anchor set."

**Code:**
```python
# Q45: LLM-as-judge drift/bias and calibration against human labels. Illustrative simulation.
import numpy as np
from scipy.stats import spearmanr, norm
rng = np.random.default_rng(45)
n = 100  # human spot check per month

# 1) the human check on its own: can 100 ratings see a +0.3 change?
sd = 0.9
se_diff = sd*np.sqrt(2/n)
print(f"SE of a difference of two 100-sample means (sd {sd}) = {se_diff:.3f}; 95% half-width {1.96*se_diff:.3f}")
assert abs(1.96*se_diff - 0.249) < 0.001
power = 1 - norm.cdf(1.96 - 0.3/se_diff) + norm.cdf(-1.96 - 0.3/se_diff)
print(f"power to detect a true +0.3 with 100 vs 100 humans = {power:.2f}")
assert 0.6 < power < 0.7

# 2) simulate: true quality unchanged, outputs got longer, judge likes length
def month(n_out, mean_len):
    quality = np.clip(rng.normal(3.9, 0.8, n_out), 1, 5)           # what humans would say
    length = rng.normal(mean_len, 25, n_out)                          # words
    judge = np.clip(quality + 0.3 + 0.01*(length - 150) + rng.normal(0, 0.4, n_out), 1, 5)
    return quality, length, judge
q1, l1, j1 = month(5000, 150)
q2, l2, j2 = month(5000, 180)      # prompt change made answers 30 words longer
print(f"judge mean {j1.mean():.2f} -> {j2.mean():.2f}; true quality {q1.mean():.2f} -> {q2.mean():.2f}")
assert j2.mean() - j1.mean() > 0.2 and abs(q2.mean() - q1.mean()) < 0.05

# 3) calibrate: on a labelled set from BOTH months, regress human on judge and length
idx1 = rng.choice(5000, 200, replace=False); idx2 = rng.choice(5000, 200, replace=False)
H = np.concatenate([q1[idx1], q2[idx2]]); J = np.concatenate([j1[idx1], j2[idx2]]); L = np.concatenate([l1[idx1], l2[idx2]])
rho = spearmanr(H, J)[0]
print(f"Spearman(human, judge) over labelled 400 = {rho:.2f}")
X = np.column_stack([np.ones(len(H)), J, L - 150])
beta = np.linalg.lstsq(X, H, rcond=None)[0]
print(f"human ~ a + b*judge + c*(length-150): b={beta[1]:.2f}, c={beta[2]:.4f} (negative c = judge over-rewards length)")
assert beta[2] < -0.003
corr_j = X@beta
adj1 = (np.column_stack([np.ones(5000), j1, l1-150])@beta).mean()
adj2 = (np.column_stack([np.ones(5000), j2, l2-150])@beta).mean()
print(f"length-adjusted judge: {adj1:.2f} -> {adj2:.2f} (change {adj2-adj1:+.2f}); human truth change {q2.mean()-q1.mean():+.2f}")
assert abs((adj2 - adj1) - (q2.mean() - q1.mean())) < 0.08
# agreement check by band: judge >= 4.5 vs human >= 4.5 (illustrative threshold)
hi_j = J >= 4.5
print(f"judge >=4.5 share {hi_j.mean():.2f}; of those humans also >=4.5: {(H[hi_j] >= 4.5).mean():.2f}")
```

**Output (my run):**
```text
SE of a difference of two 100-sample means (sd 0.9) = 0.127; 95% half-width 0.249
power to detect a true +0.3 with 100 vs 100 humans = 0.65
judge mean 4.09 -> 4.34; true quality 3.87 -> 3.89
Spearman(human, judge) over labelled 400 = 0.81
human ~ a + b*judge + c*(length-150): b=0.86, c=-0.0067 (negative c = judge over-rewards length)
length-adjusted judge: 3.89 -> 3.90 (change +0.01); human truth change +0.01
judge >=4.5 share 0.44; of those humans also >=4.5: 0.42
```

**Follow-ups:**
- How many human labels do you need? Enough to estimate agreement within a few points; a few hundred, stratified by segment, and more when the decision is risky.
- Could you use two judges? Yes, from different families, and flag disagreement for human review; it reduces self-preference but does not remove shared biases.

**Common mistakes:** Believing the judge because the number moved. Comparing scores across judge or prompt changes. Calibrating once and never again. Ignoring length and position bias. Treating a 100-item human check as conclusive.

### Q46 ⭐ 🔴 A tool-using LLM agent's task success rate fell from 82% to 74% after a third-party tool API changed its response format, and the failure was not visible in latency or error-rate dashboards. Explain how you would trace the failing step, what regression suite and contract tests would have caught it, and how to pick between prompt fixes, parsing fixes and fallback paths.
**Asked at:** AI-era RAG and LLM quality-regression guides (Braintrust RAG-observability article, Dataiku RAG-observability post, an Apptension RAG quality guide, practitioner posts on silent AI degradation); reported as a current theme in practitioner guides, not tied to a named employer; search snippets only, not opened
**Say this first (1 line):** Latency and error dashboards only see that a call returned; they do not see that the tool's answer was read wrongly, so I trace failed runs step by step to the tool call, confirm with a contract test on the tool response, and fix the parsing layer first, not the prompt.

**Clarifying questions:**
- When did success start falling, and does it line up with the vendor's change date? Why: a step change on one date points at the API.
- What share of tasks use that tool? Why: a few points of overall drop can be a big drop on one path (here 8 points overall is 32 points on a quarter of the traffic).
- Is the tool response parsed by code, or read by the model from raw text? Why: it decides where the silent failure lives.
- Do we store full traces (prompt, tool call, tool response, final answer)? Why: without traces I cannot find the failing step.
- Does the vendor offer versioned endpoints or a changelog? Why: it decides whether I can pin the old format.

**Approach:**
1. Confirm it is real: 82% to 74% on 1,000 tasks each gives z = 4.3 (p about 0.00002), so it is not noise.
2. Slice by tool: success for tasks that call the changed tool versus those that do not. In the example the tool path fell from 76% to 44% and everything else was unchanged.
3. Trace the failing step: in failed runs, compare the tool response before and after the change date. Look for the first step where the agent's belief differs from the real response (for example price read as 0).
4. Add a contract test: a schema check on every tool response in production and in CI, with real recorded responses as fixtures. A missing key or wrong type raises an alert.
5. Pick the fix by layer: (a) parsing fix (a versioned adapter that maps the new format to the old) is the first choice because it is deterministic; (b) a prompt fix only if the model must read free text and the new format is ambiguous; (c) a fallback path (fail loudly, say "unavailable", use a cached or alternative source) while the fix ships.
6. Prevent: a regression suite of tasks that exercise each tool with recorded responses, run nightly against the live API, and track task success per tool as a dashboard metric.

**Metrics:**
- Task success rate = tasks completed correctly / tasks started, per tool path and overall.
- Tool-response validity rate = responses that pass the schema / responses received.
- Fallback rate and time to detect (days from vendor change to alert).
- Guardrails: wrong-answer rate (not just failure rate), latency, cost per task.

**Risks:**
- A lenient parser returns a default instead of failing, so the wrong answer looks like success.
- Fixing in the prompt can hide the problem and break again at the next change.
- A regression suite built on mocks does not see real vendor changes; some tests must call the live API.
- Ignoring the 75% of tasks that do not use the tool is fine for diagnosis but not for the final regression check.

**What the interviewer scores:**
- Strong: slices by tool path, so 8 points overall becomes 32 points where it happened.
- Strong: contract tests on tool responses, with fail-loud behaviour.
- Strong: orders fixes: adapter, then fallback, then prompt.
- Weak: "tune the prompt" first.
- Weak: relies on error rate and latency.

**Example:** (illustrative numbers) 1,000 tasks: 750 do not use the tool and succeed 84% (630); 250 use the tool. Before: 820 successes total, so the tool path is 190 / 250 = 76%. After: 740 total, so the tool path is 110 / 250 = 44%. The 0.25 x 32 = 8-point overall drop is all in the tool path. The new response nests the price under data and the old parser's default of 0 made it a silent wrong answer. Weak answer: "The model got worse; rewrite the prompt." Strong answer: "Slice by tool, diff the responses, add a contract test and an adapter."

**Code:**
```python
# Q46: agent success fell 82% -> 74% after a tool API format change. Illustrative numbers.
import json, numpy as np
from scipy.stats import norm
N = 1000
tool_share = 0.25
non_tool_ok = 0.84
tool_before = (0.82*N - non_tool_ok*N*(1-tool_share))/(N*tool_share)
tool_after = (0.74*N - non_tool_ok*N*(1-tool_share))/(N*tool_share)
print(f"tasks using the changed tool: {int(N*tool_share)}; success before {tool_before:.1%}, after {tool_after:.1%}")
assert round(tool_before, 3) == 0.76 and round(tool_after, 3) == 0.44
# whole drop is explained by the tool path: 0.25 * (0.76-0.44) = 0.08
assert abs(tool_share*(tool_before - tool_after) - 0.08) < 1e-9

# is 8 points on 1000 vs 1000 tasks real?
p1, p2 = 0.82, 0.74
pbar = (p1+p2)/2
z = (p1-p2)/np.sqrt(pbar*(1-pbar)*2/N)
print(f"two-proportion z = {z:.2f}, p = {2*(1-norm.cdf(z)):.5f}")
assert z > 3

# contract test: the old and new response formats
old = json.loads('{"price": 249.0, "currency": "INR", "in_stock": true}')
new = json.loads('{"data": {"price": {"amount": "249.00", "currency": "INR"}, "stock": "AVAILABLE"}}')
REQUIRED = {"price": (int, float), "currency": str, "in_stock": bool}
def check_contract(resp):
    errs = []
    for k, t in REQUIRED.items():
        if k not in resp: errs.append(f"missing {k}")
        elif not isinstance(resp[k], t): errs.append(f"{k} wrong type")
    return errs
print("old format:", check_contract(old) or "ok")
print("new format:", check_contract(new))
assert check_contract(old) == [] and len(check_contract(new)) == 3

# a lenient parse that "works" but is wrong: reading price as 0 when the key is missing
def lenient(resp): return resp.get("price", 0.0)
print("lenient parser on new format returns price", lenient(new), "(silent wrong answer, no error, no latency change)")
assert lenient(new) == 0.0

# a versioned adapter plus a fail-loud fallback
def adapter(resp):
    if "data" in resp:   # v2 format
        d = resp["data"]
        return {"price": float(d["price"]["amount"]), "currency": d["price"]["currency"], "in_stock": d["stock"] == "AVAILABLE"}
    return resp
fixed = adapter(new)
print("adapter output:", fixed)
assert check_contract(fixed) == [] and fixed["price"] == 249.0
# unknown format -> fail loudly and use the fallback path (tell the user it is unavailable)
def safe_fetch(resp):
    try: return adapter(resp) if not check_contract(adapter(resp)) else None
    except (KeyError, TypeError): return None
assert safe_fetch({"weird": 1}) is None and safe_fetch(new)["price"] == 249.0
print("unknown format -> None -> fallback path; known formats parse")
```

**Output (my run):**
```text
tasks using the changed tool: 250; success before 76.0%, after 44.0%
two-proportion z = 4.32, p = 0.00002
old format: ok
new format: ['missing price', 'missing currency', 'missing in_stock']
lenient parser on new format returns price 0.0 (silent wrong answer, no error, no latency change)
adapter output: {'price': 249.0, 'currency': 'INR', 'in_stock': True}
unknown format -> None -> fallback path; known formats parse
```

**Follow-ups:**
- What if the vendor changes a field's meaning but not its format? A schema test will not catch it; use value-level checks (ranges, known examples) and the regression suite of expected answers.
- Where do you put the contract test? At the boundary in production (validate and alert) and in CI nightly against recorded plus live responses.

**Common mistakes:** Watching only latency and errors. Parsers with silent defaults. Fixing in the prompt first. Testing against mocks only. Looking at the overall rate instead of the per-tool path.

### Q47 ⭐ 🔴 A retrained recommender showed a 3% conversion lift in week one of its A/B test, but the lift decayed to near zero by week four. Explain novelty effects, interference between buckets and cannibalised demand, how you would use a long-term holdout to settle it, and what you would tell the business about shipping.
**Asked at:** Safe-rollout and shadow/canary guides (Qwak shadow-versus-canary post, Atlan shadow-deployment page, a NerdLevelTech MLOps-interview deployment-strategies lesson, a datainterview.com safe-rollout drill); commonly reported in public MLOps guides; search snippets only, not opened
**Say this first (1 line):** A lift that fades from 3% to about zero is usually a novelty effect, sometimes compounded by bucket interference or demand that was only moved from one place to another, so I would not ship on week-one numbers and I would settle it with a long-term holdout.

**Clarifying questions:**
- What was the unit of randomisation (user, session, item)? Why: bucket interference depends on it.
- Do treatment and control share limited resources (inventory, ad slots, drivers)? Why: shared supply means treatment can steal from control.
- Is the lift fading for new and returning users alike? Why: novelty hits returning users most, because they see something new.
- Did anything else change in weeks 2 to 4 (a campaign, seasonality)? Why: a time effect can mimic decay.
- Which metric matters: conversion, revenue, or long-term retention? Why: a short-term conversion lift may cost retention.

**Approach:**
1. Plot the effect by week, with intervals. In the example: 3.0%, 2.0%, 1.0%, 0.2% relative, a steady fall. A decaying curve is the novelty signature; a flat 3% would not be.
2. Split by user age and exposure count: users seeing the new recommendations for the first time versus repeat exposure. Novelty effect shrinks with repeats.
3. Check interference: if both buckets draw on the same pool, the treatment's gain can come from control. A test can read 6.2% when the company-wide gain is 0% (see the code, with a pool of 4,000 units). Look at total sales across both arms, not the treated arm alone.
4. Check cannibalisation: a rise on recommended items matched by a fall on other items or channels. Measure total basket or total revenue, not item clicks.
5. Settle it with a long-term holdout: keep a share of users on the old recommender for 8 to 12 weeks while the rest get the new one, and compare long-run outcomes. A 5% holdout of 10 million users is 500,000 users and can detect about a 2% relative change; a 0.2% residual lift needs far more users or time.
6. Tell the business: the 3% was a launch bump; the durable lift looks small or zero. Ship only if cost is low and the holdout shows a positive, durable effect; otherwise do not claim the 3%.

**Metrics:**
- Weekly relative lift = (treatment rate / control rate) - 1, with a 95% interval, by weeks since exposure.
- Total conversions across both arms (interference check).
- Holdout comparison on long-run metric: revenue per user, 8-week retention.
- Guardrails: catalogue diversity, returns, complaints.

**Risks:**
- Peeking at week one and shipping.
- Calling it novelty when it is a seasonal change that hit both arms equally (the lift is a ratio between arms, so seasonality alone does not make it fade, but an interaction can).
- A holdout too small to see a small durable effect.
- A holdout that is costly in lost revenue (see Q48 in this part).

**What the interviewer scores:**
- Strong: names the three mechanisms and a check for each.
- Strong: uses total across arms to expose interference, and sizes the holdout with numbers.
- Strong: a clear message for the business, not just "inconclusive".
- Weak: "run the test longer" with no plan.
- Weak: ignores shared supply.

**Example:** (illustrative numbers) Baseline conversion 4.00%. Week 1: 4.12% (+3.0%). Week 4: 4.008% (+0.2%). To detect a 3% lift you need about 418,607 users per arm; for a 1% lift about 3.77 million. With 10 million users and a 5% holdout (500,000 versus 9.5 million) the smallest detectable lift is about 2%, so the holdout can confirm that the week-one 3% is gone but not a 0.2% residual. Weak answer: "It is a 3% win, ship it." Strong answer: "It decays like a novelty effect; I would hold out 5% for 8 weeks and tell the business the durable gain is unproven."

**Code:**
```python
# Q47: novelty effect, cannibalisation, long-term holdout. Illustrative numbers.
import numpy as np
from scipy.stats import norm
base = 0.040   # control conversion
lift_rel = {1: 0.030, 2: 0.020, 3: 0.010, 4: 0.002}   # observed relative lift by week
for w, l in lift_rel.items():
    print(f"week {w}: relative lift {l:.1%}  (conversion {base*(1+l):.4f} vs {base:.4f})")
assert abs(base*(1+lift_rel[1]) - 0.0412) < 1e-12

# exponential-decay fit: ratio between weeks
r = np.exp(np.diff(np.log([lift_rel[w] for w in (1, 2, 3)]))).mean()
print(f"week-over-week lift ratio (weeks 1-3) ~ {r:.2f}; week 4 predicted {0.03*r**3:.4f}")

def n_per_arm(p, rel, alpha=0.05, power=0.8):
    d = p*rel
    return int(np.ceil(2*(norm.ppf(1-alpha/2)+norm.ppf(power))**2*p*(1-p)/d**2))
n_3 = n_per_arm(base, 0.03)
n_1 = n_per_arm(base, 0.01)
print(f"users per arm to detect 3% relative lift: {n_3:,}; 1% relative lift: {n_1:,}")
assert 400_000 < n_3 < 430_000 and 3_700_000 < n_1 < 4_000_000

# holdout sizing: 10M users, 5% held out on old model gives 500k vs 9.5M
n_h, n_t = 500_000, 9_500_000
se = np.sqrt(base*(1-base)*(1/n_h + 1/n_t))
mde_rel = (norm.ppf(0.975)+norm.ppf(0.8))*se/base
print(f"5% holdout of 10M users: detectable relative lift ~ {mde_rel:.2%} (80% power)")
assert 0.018 < mde_rel < 0.021

# cannibalised demand: 1,000 units of stock a day, shared by both buckets
# treatment shows items that are in demand; it wins sales from control during the test
buyers_control_alone = 0.040*50_000        # if both buckets got the old model (50k users each)
supply = 4_000                              # units (limited)
# during the A/B test treatment takes 3% more of the same pool: control loses what treatment wins
treat_sales = buyers_control_alone*1.03
ctrl_sales = supply - treat_sales
ab_lift = treat_sales/ctrl_sales - 1
print(f"limited pool: A/B reads {ab_lift:.1%} lift; full rollout total sales stay {supply}")
assert abs(ab_lift - (2060/1940 - 1)) < 1e-9 and ab_lift > 0.06
assert treat_sales + ctrl_sales == supply
print(f"true company-wide lift from the pool: 0%, yet the test reads {ab_lift:.1%}: interference")
```

**Output (my run):**
```text
week 1: relative lift 3.0%  (conversion 0.0412 vs 0.0400)
week 2: relative lift 2.0%  (conversion 0.0408 vs 0.0400)
week 3: relative lift 1.0%  (conversion 0.0404 vs 0.0400)
week 4: relative lift 0.2%  (conversion 0.0401 vs 0.0400)
week-over-week lift ratio (weeks 1-3) ~ 0.58; week 4 predicted 0.0060
users per arm to detect 3% relative lift: 418,607; 1% relative lift: 3,767,463
5% holdout of 10M users: detectable relative lift ~ 1.99% (80% power)
limited pool: A/B reads 6.2% lift; full rollout total sales stay 4000
true company-wide lift from the pool: 0%, yet the test reads 6.2%: interference
```

**Follow-ups:**
- How long should the holdout run? Until the lift curve is flat for a few weeks, typically more than one full cycle of the user behaviour. Related ideas on novelty in onboarding are in Book 6 Part 1, Q33, and on short-term versus long-term lift in Book 6 Part 1, Q39.
- What if the holdout shows a small positive lift? Ship if the cost is low; the number to quote is the holdout's, not week one's.

**Common mistakes:** Shipping on week one. Reading the treated arm alone when supply is shared. Holdouts too small. Blaming seasonality without a check. Not saying what to do.

### Q48 ⭐ 🔴 A company keeps 2% of traffic permanently on a frozen old model so it can measure model decay and the value of retraining, but finance says this costs up to about 2% of the model's revenue benefit. Explain the case for and against a permanent holdout, how you would size it, and cheaper alternatives for measuring decay.
**Asked at:** No public page found, editor-designed from standard production-ML judgement themes that the degradation guides describe in general terms; search snippets only, not opened
**Say this first (1 line):** A permanent frozen holdout is insurance that measures decay directly, and it is worth it when the model carries a lot of value; but 2% is rarely the cheapest design, so I would size it to the smallest effect I need to detect and consider a rotating or smaller holdout first.

**Clarifying questions:**
- What does "2% of the model's benefit" mean: 2% of the gain over no model, or of the gain over the frozen model? Why: the real cost is the new model's gain over the frozen one on that 2% of traffic, which is smaller.
- How big is the benefit in rupees per year? Why: it sets the budget for insurance.
- What smallest decay would change a decision (for example 2% relative)? Why: the holdout size follows from it.
- Are users sticky (the same user stays in the holdout) or do they rotate? Why: it affects fairness and what the holdout shows.
- Is there a regulatory or fairness issue in keeping some customers on an old model? Why: it can limit the design.

**Approach:**
1. Frame the trade: holdout cost is certain and small; the value is catching decay early.
2. Compute the cost properly. The holdout customers still get a working (frozen) model, so the cost is 2% x (new model gain minus frozen model gain), which is at most 2% of the total benefit. For a benefit of Rs 500 lakh a year (illustrative) the cap is Rs 10 lakh; if the new model adds 30% over the frozen one it is Rs 3 lakh.
3. Compute the value: a 10% decay in benefit that goes unseen for one quarter is Rs 500 x 0.10 x 0.25 = Rs 12.5 lakh, more than a year of holdout cost in the capped case.
4. Size it by detectability: with 20 million decisions a week and a 5% base rate, a 2% holdout (400,000 users) detects about a 1.95% relative gap in a week at 80% power; pooled over 4 weeks about 1%. A 0.5% holdout detects 3.9% weekly and about 1% after 16 weeks.
5. Cheaper alternatives: (a) a smaller holdout (0.5%) read over longer windows, (b) a rotating holdout where each user is frozen only 4 weeks, (c) periodic challenger tests (a frozen model against the current one for 2 weeks every quarter), (d) shadow scoring of the old model plus off-policy estimates, (e) delayed-label accuracy trends with proxy metrics.
6. Recommend: a small rotating holdout for the high-value model, reviewed yearly; none for low-value models.

**Metrics:**
- Holdout cost = share x (new model gain - frozen model gain).
- Smallest detectable relative gap = (z_alpha/2 + z_power) x sqrt(p(1 - p)(1/n_h + 1/n_m)) / p.
- Decay estimate = metric(current) - metric(frozen), with an interval, tracked weekly.
- Guardrails: harm to holdout users, fairness across segments, holdout contamination.

**Risks:**
- A permanently frozen model gets so stale that the comparison is no longer realistic.
- Holdout leakage (users switching devices, shared features) biases the gap towards zero.
- Pooling weeks assumes a stable gap.
- Ethical or contractual limits on treating customers differently.

**What the interviewer scores:**
- Strong: computes the real cost (the gain over the frozen model, not the whole benefit).
- Strong: sizes with power and shows the trade between share and time.
- Strong: names cheaper alternatives and a recommendation.
- Weak: "always keep a holdout" or "never, it costs money" without numbers.
- Weak: ignores that the holdout users still get a working model.

**Example:** (illustrative numbers) Benefit Rs 500 lakh a year. Holdout 2%: cost cap Rs 10 lakh, realistic Rs 3 lakh. Detectability: 1.95% relative weekly. A 0.5% holdout costs 25% as much, detects 3.9% weekly and about 1% after 16 weeks pooled. One missed 10% decay quarter costs Rs 12.5 lakh. Weak answer: "Finance is right, drop it." Strong answer: "Shrink and rotate it; the insurance is worth more than it costs."

**Code:**
```python
# Q48: permanent holdout sizing and cost. Illustrative numbers.
import numpy as np
from scipy.stats import norm
weekly_decisions = 20_000_000
p = 0.05                      # conversion on the metric we care about
for share in (0.02, 0.005, 0.01):
    n_h = weekly_decisions*share; n_m = weekly_decisions - n_h
    se = np.sqrt(p*(1-p)*(1/n_h + 1/n_m))
    mde = (norm.ppf(0.975)+norm.ppf(0.8))*se
    print(f"holdout {share:.1%}: {int(n_h):,} users/week, detectable gap {mde*100:.3f} pp = {mde/p:.2%} relative (80% power, weekly)")
n_h = weekly_decisions*0.02; n_m = weekly_decisions - n_h
mde_rel = (norm.ppf(0.975)+norm.ppf(0.8))*np.sqrt(p*(1-p)*(1/n_h+1/n_m))/p
assert 0.018 < mde_rel < 0.021
# accumulate 4 weeks: noise falls by sqrt(4)
print(f"4 weeks pooled at 2%: ~{mde_rel/2:.2%} relative")
assert abs(mde_rel/2 - 0.0098) < 0.0005

# cost: the holdout loses (new model - frozen model) benefit on 2% of traffic
annual_benefit = 500.0     # Rs lakh per year: value of the model over the "no model" baseline (Rs 5 crore)
uplift_new_over_frozen = 0.30*annual_benefit  # new model adds 30% over the frozen one after a year of drift
cost_upper = 0.02*annual_benefit
cost_real = 0.02*uplift_new_over_frozen
print(f"upper bound (frozen = no model): Rs {cost_upper:.0f} lakh/yr; realistic (frozen model keeps most value): Rs {cost_real:.0f} lakh/yr")
assert cost_upper == 10.0 and abs(cost_real - 3.0) < 1e-9

# value: a decay of 10% of benefit that goes unseen for a quarter
decay_missed = 0.10*annual_benefit*0.25
print(f"undetected 10% decay for one quarter costs Rs {decay_missed:.1f} lakh; one such quarter costs more than a year of holdout (Rs {cost_upper:.0f} lakh)")
assert abs(decay_missed - 12.5) < 1e-9 and decay_missed > cost_upper

# cheaper design: rotating 0.5% holdout, each user frozen for 4 weeks only, new users each cycle
share = 0.005
n_h = weekly_decisions*share; n_m = weekly_decisions - n_h
mde = (norm.ppf(0.975)+norm.ppf(0.8))*np.sqrt(p*(1-p)*(1/n_h+1/n_m))/p
print(f"0.5% holdout: weekly MDE {mde:.1%} relative; pooled over 16 weeks {mde/4:.1%}")
assert 0.036 < mde < 0.040 and abs(mde/4 - mde/np.sqrt(16)) < 1e-12
print("cost scales with share:", f"{0.005/0.02:.0%} of the 2% holdout cost")
assert abs(0.005/0.02 - 0.25) < 1e-12
```

**Output (my run):**
```text
holdout 2.0%: 400,000 users/week, detectable gap 0.098 pp = 1.95% relative (80% power, weekly)
holdout 0.5%: 100,000 users/week, detectable gap 0.194 pp = 3.87% relative (80% power, weekly)
holdout 1.0%: 200,000 users/week, detectable gap 0.137 pp = 2.74% relative (80% power, weekly)
4 weeks pooled at 2%: ~0.98% relative
upper bound (frozen = no model): Rs 10 lakh/yr; realistic (frozen model keeps most value): Rs 3 lakh/yr
undetected 10% decay for one quarter costs Rs 12.5 lakh; one such quarter costs more than a year of holdout (Rs 10 lakh)
0.5% holdout: weekly MDE 3.9% relative; pooled over 16 weeks 1.0%
cost scales with share: 25% of the 2% holdout cost
```

**Follow-ups:**
- When is a holdout not worth it? When the model's value is small or decay is slow and visible in cheap proxies. Related ideas appear in Book 6 Part 1, Q39 (long-term holdouts for a recommender).
- How do you keep the holdout honest? Fix assignment by hashed user ID, log exposure, and check balance (sample-ratio check) each week.

**Common mistakes:** Treating the cost as 2% of everything. Under-sizing the holdout so it cannot see the effect. Letting holdout users leak into treatment. Choosing a share without a detectable-effect target.

### Q49 ⭐ 🔴 A regulation change in payments suddenly makes most of two years of transaction history unrepresentative, and only six weeks of new-regime data exists. Explain how you would keep a risk model running, which parts of the old data you would reuse, how you would use priors, simple models or human oversight in the interim, and how you would decide when to trust a new model.
**Asked at:** No interview page located; forecast-monitoring practitioner pages (demandplanning.net MAPE and bias, John Galt Solutions, 42signals forecast-drift post) describe bias, structural breaks and MAPE blind spots, so editor-designed; search snippets only, not opened
**Say this first (1 line):** I would keep the old model running under tight guardrails and human review, build a new model on the six weeks of new-regime data (using old data only where the relationship has not changed), and promote it only when it beats the interim model by more than the noise in a six-week sample.

**Clarifying questions:**
- Which inputs and which outcomes does the regulation change (fees, limits, authentication, customer behaviour)? Why: it shows which features and relationships changed and which did not.
- How many positive events (defaults, frauds) are in the six weeks? Why: events, not rows, decide how complex a model I can fit.
- Is there a rules or policy fallback today? Why: a known fallback is the safe interim.
- How fast do outcomes mature? Why: if labels take months, six weeks of "new data" may have few labels.
- What is the cost of a wrong decision in each direction and who signs off on risk? Why: it sets how much human oversight is needed.

**Approach:**
1. Triage the data: split features into stable (their relationship with the outcome should survive the change) and regime-sensitive (fees, limits, flows the rule touched). Use domain knowledge and a test on the six weeks for each group.
2. Interim: keep the old model but add guardrails: tighter thresholds on the regime-sensitive part, human review for the middle band, daily monitoring of score mix and approval rate, and a simple rule overlay where the regulation requires one.
3. Build the new model: a simple model (logistic regression with few features) on the six weeks, optionally with a prior: start from the old coefficients and penalise only deviations (shrink toward old), or add old data at low weight.
4. Compare on held-out new-regime data, by time (train on the first four weeks, test on the last two).
5. Quantify noise: repeat the evaluation on resampled six-week samples. In my run the AUC varies by about 0.008 between samples, so I would not promote on a 0.01 gain.
6. Decide when to trust the new model: pre-agree a rule: it beats the interim model by more than twice the sample-to-sample sd on a time-held-out set, passes a segment check, runs in shadow, then ramps behind a canary. Re-train every few weeks as data accumulates and phase out the interim.

**Metrics:**
- AUC (or the business metric) on a time-held-out slice of the new regime, with a resampling interval.
- Calibration: predicted versus observed rate in the new regime, once labels mature.
- Events per feature (aim for at least 10 to 20 events per model parameter as a rough guide).
- Guardrails: approval rate, loss rate, human-review rate, segment gaps.

**Risks:**
- Pooling old and new data at equal weight pulls the model back to the old rules (naive pooling at weight 0.02 was clearly worse than new-only in my run).
- Six weeks may not cover a full cycle (month-end, festival), so seasonal patterns are missing.
- Overfitting a complex model to few events.
- Labels in new regime may still be immature (see Q28 in this part).

**What the interviewer scores:**
- Strong: separates stable from regime-sensitive features and says which old data to reuse.
- Strong: interim safety with guardrails and human oversight, plus an explicit promotion rule.
- Strong: acknowledges small-sample noise with a number.
- Weak: "retrain on everything" or "wait for more data".
- Weak: no interim plan.

**Example:** (illustrative simulation with 30 features, four of which change meaning) The old model scores AUC 0.832 on future new-regime data, a model trained on 500 new-regime rows (86 events) scores 0.910, naive pooling with a low old weight scores 0.856, and shrinking toward the old coefficients scores 0.911. So the old model is clearly stale and naive pooling is worse than new-only, but shrinking gives no clear gain in my run (30 samples: 0.906 versus 0.903, sd 0.008 and 0.006). The promotion margin is therefore twice the sd, about 0.012. Weak answer: "Wait six months for data." Strong answer: "Interim guardrails, a simple new model, shrink toward the old where stable, a pre-agreed promotion test."

**Code:**
```python
# Q49: regime change; 2 years of old data, 6 weeks of new data. Illustrative simulation.
import numpy as np
from scipy.optimize import minimize
from scipy.stats import rankdata
rng = np.random.default_rng(49)
d = 30
beta_old = rng.normal(0, 0.4, d)
beta_new = beta_old.copy()
beta_new[:4] = [1.0, -1.0, 0.8, -0.8]          # four features change meaning, 26 keep it
b0 = -3.5
def gen(n, beta):
    X = rng.normal(size=(n, d))
    y = rng.random(n) < 1/(1+np.exp(-(b0 + X@beta)))
    return X, y.astype(float)
n_old, n_new = 200_000, 500
Xo, yo = gen(n_old, beta_old)
Xn, yn = gen(n_new, beta_new)
Xt, yt = gen(100_000, beta_new)               # future new-regime data

def fit(X, y, w=None, l2=0.0, center=None):
    X1 = np.column_stack([np.ones(len(X)), X]); w = np.ones(len(y)) if w is None else w
    c = np.zeros(d+1) if center is None else center
    f = lambda b: np.sum(w*(np.logaddexp(0, X1@b) - y*(X1@b)))/w.sum() + l2*np.sum((b[1:]-c[1:])**2)
    return minimize(f, c, method="L-BFGS-B").x
def auc(b, X, y):
    s = np.column_stack([np.ones(len(X)), X])@b
    r = rankdata(s); n1 = y.sum(); n0 = len(y)-n1
    return (r[y == 1].sum() - n1*(n1+1)/2)/(n1*n0)
print(f"new-regime events in 6 weeks: {int(yn.sum())} of {n_new}")
b_old = fit(Xo, yo)
res = {"old model unchanged": auc(b_old, Xt, yt), "new data only": auc(fit(Xn, yn, l2=0.0), Xt, yt)}
res["new data only, ridge 0.01"] = auc(fit(Xn, yn, l2=0.01), Xt, yt)
for lam in (0.01, 0.03, 0.1):
    res[f"new data, shrink to old, lam {lam}"] = auc(fit(Xn, yn, l2=lam, center=b_old), Xt, yt)
X = np.vstack([Xo, Xn]); y = np.concatenate([yo, yn])
res["pooled, old weight 0.02"] = auc(fit(X, y, np.concatenate([np.full(n_old, 0.02), np.ones(n_new)])), Xt, yt)
res["oracle (true new coefficients)"] = auc(np.concatenate([[b0], beta_new]), Xt, yt)
for k, v in res.items(): print(f"{k:38s} AUC on future new-regime data = {v:.3f}")
shrink = {k: v for k, v in res.items() if "shrink" in k}
best_shrink = max(shrink.values())
assert best_shrink > res["old model unchanged"] + 0.05 and res["new data only"] > res["old model unchanged"] + 0.05
assert res["oracle (true new coefficients)"] >= best_shrink
print(f"best shrink-to-old = {best_shrink:.3f} vs new-only {res['new data only']:.3f} vs old {res['old model unchanged']:.3f}")
# six weeks is a small sample, so one fit is noisy: repeat the new-only vs shrink comparison on 15 different six-week samples
a_new, a_shr = [], []
for s in range(30):
    r = np.random.default_rng(1000+s)
    Xs = r.normal(size=(n_new, d)); ys = (r.random(n_new) < 1/(1+np.exp(-(b0 + Xs@beta_new)))).astype(float)
    a_new.append(auc(fit(Xs, ys), Xt, yt)); a_shr.append(auc(fit(Xs, ys, l2=0.03, center=b_old), Xt, yt))
print(f"30 six-week samples: new-only mean {np.mean(a_new):.3f} (sd {np.std(a_new):.3f}); shrink-to-old mean {np.mean(a_shr):.3f} (sd {np.std(a_shr):.3f})")
assert abs(np.mean(a_shr) - np.mean(a_new)) < 0.01     # no clear gain from shrinking in this run
assert res['pooled, old weight 0.02'] < res['new data only'] - 0.03   # naive pooling is clearly worse
print("promotion rule used: new model must beat the interim model by more than twice the sample-to-sample sd:", round(2*np.std(a_shr), 3))
```

**Output (my run):**
```text
new-regime events in 6 weeks: 86 of 500
old model unchanged                    AUC on future new-regime data = 0.832
new data only                          AUC on future new-regime data = 0.910
new data only, ridge 0.01              AUC on future new-regime data = 0.907
new data, shrink to old, lam 0.01      AUC on future new-regime data = 0.911
new data, shrink to old, lam 0.03      AUC on future new-regime data = 0.903
new data, shrink to old, lam 0.1       AUC on future new-regime data = 0.878
pooled, old weight 0.02                AUC on future new-regime data = 0.856
oracle (true new coefficients)         AUC on future new-regime data = 0.928
best shrink-to-old = 0.911 vs new-only 0.910 vs old 0.832
30 six-week samples: new-only mean 0.906 (sd 0.008); shrink-to-old mean 0.903 (sd 0.006)
promotion rule used: new model must beat the interim model by more than twice the sample-to-sample sd: 0.012
```

**Follow-ups:**
- When would old data help more? When more coefficients are stable and the new sample is tiny; the prior then stabilises the fit. Test it on a time-held-out slice rather than assume.
- What do you tell the business now? The interim model is less accurate than before; here is the guardrail, the expected error range and the date to review.

**Common mistakes:** Pooling old and new at equal weight. Throwing away all old data. A complex model on a few events. Promoting on a small gain. No interim plan or human oversight.

### Q50 ⭐ 🔴 A degraded model went unnoticed for three weeks and leadership wants a written account and a plan. Explain how you would structure a blameless postmortem for an ML failure, which detection and ownership gaps you would look for, how you would size the business impact, and what you would commit to as concrete monitoring and process changes.
**Asked at:** Production-degradation question banks (Dataford pages such as 'if a model's performance drops in production, what is your step-by-step diagnostic process', a Prepfully 'diagnose and fix a model deployed to production that underperformed' answer page, a TryExponent production-ML course page); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** A blameless postmortem asks why the system allowed a three-week failure to go unseen, not who caused it; I write a timeline, find the detection and ownership gaps, size the loss as a range, and commit to a few monitoring and process changes with owners and dates.

**Clarifying questions:**
- What was the root trigger (a data change, a code release, a world change)? Why: it shapes the prevention actions, but the detection gap is the bigger lesson.
- Who owned the model's health, and was it written down? Why: an unowned model has no one to be alerted.
- What alerts existed, and which fired or should have? Why: it separates "no monitor" from "monitor ignored".
- How do we know the start date of the degradation? Why: the loss estimate depends on it.
- Who reads the postmortem and what do they decide? Why: leadership needs impact and commitments, engineers need causes.

**Approach:**
1. Rules of the room: blameless; focus on conditions that let it happen; no names in the root cause.
2. Timeline: when the change happened, when metrics first moved, when each signal could have fired, when a human noticed, when it was fixed. Use logs, not memory.
3. Gaps: (a) detection: no monitor on inputs, scores or labelled metrics, or a threshold nobody read; (b) ownership: no on-call or named owner; (c) change control: the change shipped without a model owner knowing; (d) validation: no consumer test; (e) label delay: the true metric appears after weeks (see Q4 in this part).
4. Impact: attempts per day x change in catch rate x loss per case x days. In the example 1,000 attempts a day, catch rate 85% to 70% and Rs 5,000 per missed fraud over 21 days is Rs 157.5 lakh (Rs 1.575 crore). If the drop ramped in over 7 days it is Rs 131 lakh. Quote the range with the assumptions and say which costs are excluded (chargeback fees, customer harm).
5. Counterfactual: which monitor would have caught it and when (see the code: a null-rate alert on day 4, a score-mean alert on day 4, the labelled metric around day 18, a human on day 24).
6. Commitments: each with an owner, a date and a check: input and score-distribution monitors with thresholds, a labelled-metric dashboard with maturity rules, an owner and on-call, a pre-release consumer test, a runbook, and a review of the monitors after 30 days. Publish the postmortem.

**Metrics:**
- Time to detect = detection time - start of degradation; time to mitigate = fix time - detection time.
- Impact = extra missed cases x average loss per case, as a range.
- Share of incidents caught by monitors (not by humans).
- Guardrail: alert precision (alerts that were real) so new monitors do not cause alert fatigue.

**Risks:**
- A blame culture hides facts.
- Over-precise impact numbers invite challenge; give a range and method.
- Too many action items: nothing gets done.
- Commitments with no owner or date.

**What the interviewer scores:**
- Strong: timeline first, causes as conditions, and detection and ownership gaps.
- Strong: impact as a range with a formula, not a headline number.
- Strong: few, concrete, owned commitments with a measure of success.
- Weak: names a person or says "be more careful".
- Weak: no numbers, or a single exact number without assumptions.

**Example:** (illustrative numbers) Change on day 3, noticed on day 24, so 21 days undetected. Pipeline monitors would have fired on day 4 (1 day); the labelled metric needs a 14-day delay and would have shown on day 18 (15 days after the change). A null-rate monitor alone would have avoided about 20 days of loss, Rs 150 lakh. Weak answer: "The model owner should have checked." Strong answer: "We had no input monitor and no owner; adding both would have cut detection from 21 days to 1."

**Code:**
```python
# Q50: postmortem numbers: impact sizing and detection timeline. Illustrative numbers.
import numpy as np
rng = np.random.default_rng(50)
# impact: fraud model catch rate fell after a feature pipeline change
attempts_per_day = 1_000
avg_loss = 5_000           # Rs per missed fraud
catch_before, catch_after = 0.85, 0.70
days = 21
extra_missed_per_day = attempts_per_day*(catch_before - catch_after)
extra_loss = extra_missed_per_day*avg_loss*days
print(f"extra missed fraud/day {extra_missed_per_day:.0f}; extra direct loss over {days} days = Rs {extra_loss/1e5:.1f} lakh = Rs {extra_loss/1e7:.3f} crore")
assert round(extra_missed_per_day) == 150 and round(extra_loss) == 15_750_000
# counterfactual honesty: range of impact if catch_after was only reached gradually (linear ramp over 7 days)
ramp = np.concatenate([np.linspace(0, 0.15, 7), np.full(days-7, 0.15)])
loss_ramp = (ramp*attempts_per_day*avg_loss).sum()
print(f"if the drop ramped linearly over the first 7 days: Rs {loss_ramp/1e5:.1f} lakh")
assert loss_ramp < extra_loss
low, high = loss_ramp, extra_loss
print(f"quote a range: Rs {low/1e5:.0f} to {high/1e5:.0f} lakh direct loss, before chargeback fees and customer cost")

# detection timeline: which monitor would have fired when
label_delay = 14
t = np.arange(40)
shift = np.clip((t - 3)/1.0, 0, 1)      # pipeline change at day 3: null-rate jumps at once
null_rate = 0.005 + 0.15*shift + rng.normal(0, 0.002, t.size)
score_mean = 0.10 - 0.03*shift + rng.normal(0, 0.003, t.size)
catch = 0.85 - 0.15*shift + rng.normal(0, 0.01, t.size)
def first_alert(series, thr, above=True):
    idx = np.where(series > thr if above else series < thr)[0]
    return int(idx[0]) if len(idx) else None
d_null = first_alert(null_rate, 0.02)
d_score = first_alert(score_mean, 0.085, above=False)
d_label_visible = first_alert(catch, 0.80, above=False) + label_delay    # label-based metric only appears after delay
d_complaints = 24                         # analysts noticed in week 4 (illustrative)
print(f"change on day 3. null-rate alert day {d_null}; score-mean alert day {d_score}; labelled catch-rate alert day {d_label_visible}; humans noticed day {d_complaints}")
assert d_null == 4 and d_score is not None and d_score <= 5 and d_label_visible >= 17
print(f"time to detect: pipeline monitors {d_null-3} day(s); label-based {d_label_visible-3} days; actual {d_complaints-3} days")
assert d_complaints - 3 == 21
saved = (d_complaints - d_null)*ramp[-1]*attempts_per_day*avg_loss
print(f"loss avoided with a null-rate monitor: about Rs {saved/1e5:.0f} lakh")
assert abs(saved - 20*0.15*1000*5000) < 1  # 20 days x 150 x Rs 5,000 = Rs 150 lakh
```

**Output (my run):**
```text
extra missed fraud/day 150; extra direct loss over 21 days = Rs 157.5 lakh = Rs 1.575 crore
if the drop ramped linearly over the first 7 days: Rs 131.2 lakh
quote a range: Rs 131 to 158 lakh direct loss, before chargeback fees and customer cost
change on day 3. null-rate alert day 4; score-mean alert day 4; labelled catch-rate alert day 18; humans noticed day 24
time to detect: pipeline monitors 1 day(s); label-based 15 days; actual 21 days
loss avoided with a null-rate monitor: about Rs 150 lakh
```

**Follow-ups:**
- How do you avoid it being a paper exercise? Track each action to closure, test the new alerts with a drill, and review at 30 and 90 days.
- How do you size impact when labels are delayed? Use the proxy (score or catch rate on matured samples) for a first range, then update when labels mature.

**Common mistakes:** Hunting for a culprit. One exact loss figure. A long list of vague actions. No owner. Skipping the timeline. Forgetting the labelled-metric delay when judging what monitors could have caught.

