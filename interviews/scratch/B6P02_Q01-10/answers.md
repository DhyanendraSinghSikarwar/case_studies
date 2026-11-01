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
