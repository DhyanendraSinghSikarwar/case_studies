# Book 6 — Part 3: Imbalanced, Noisy and Missing Data Situations

**Topic:** Scenario-based "what do you do when the data looks like this" questions for Data Scientist and ML Engineer loops: extreme class imbalance (fraud, churn, rare disease), resampling, class weights, focal loss and their pitfalls (resampling before the split), metric and threshold choice (PR-AUC versus ROC-AUC), calibration after resampling, noisy and wrong labels and annotator disagreement, estimating label noise, missing-data mechanisms (MCAR, MAR, MNAR), imputation traps and leakage, missingness as signal, outliers versus errors, duplicates and near-duplicates across train and test, sampling bias and survivorship, small data, delayed, partial and positive-unlabelled labels, unit and encoding bugs, data-quality gates, subgroup under-representation, time-based and group splits, and AI-era twists (synthetic data, LLM-labelled data, weak supervision, model collapse).

**Target:** 50  |  **Actual:** 50 (⭐⭐⭐ 16, ⭐⭐ 23, ⭐ 11)  |  **Date:** 2026-10-30  |  **Status:** Complete (answers merged, checked, reviewed)

**Scope note:** this part owns the judgement angle (what do you do, in what order, with what evidence). It does not repeat the concept coverage in Book 1 (Part 3 on classification metrics, imbalance handling, resampling, thresholds and calibration; Part 2 on feature engineering and encoding); Wave B answers should cross-reference those and Book 6 Parts 1 and 2 only by checked headings. Book 6 Part 2 owns models that degrade after launch, and here the object is the data in hand. All numbers in the prompts are invented illustrative numbers, not data from any company; every percentage names its base in the prompt. Stars: 3 means reported in most loops, 2 regular, 1 senior or niche; they are editorial judgements.

**Evidence limits:** WebFetch was unavailable, so no page was opened; every source is a WebSearch snippet or result summary only (see research_notes/Book6_Part03_sources.md). Searches returned imbalance and fraud-evaluation guides (techinterview.org, Dataford, KDnuggets), missing-data explainers, noisy-label research, leakage and duplicate guides, data-cleaning question banks, small-data prompts, data-quality-gate posts and AI-era labelling and synthetic-data papers. Positive-unlabelled, subgroup and label-noise estimation searches found research and practitioner pages, not interview pages. No result tied a scenario to a named employer, so 'Asked at' lines name guide families only ('commonly reported in public guides'); scenarios marked editor-designed have no located public page. Star counts and difficulty tags are editorial. No salary figures appear anywhere in this part.

---

### Q1 ⭐⭐⭐ 🟢 A fraud dataset has 2,000,000 transactions of which 2,000 are fraud (0.1%), and a baseline that flags nothing scores 99.9% accuracy. Your manager asks why the new model's 99.8% accuracy should be seen as a failure rather than a near match. Explain what you would report instead and how you would split and evaluate the data.
**Asked at:** Imbalanced-data and fraud-evaluation guides (techinterview.org 'Handling Imbalanced Datasets in Machine Learning', Dataford fraud-evaluation prompts such as 'how do you evaluate a fraud detection model on imbalanced data', a KDnuggets piece on SMOTE misuse, a Coresignal 'class imbalance interview trap' post); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Accuracy cannot tell a good fraud model from a useless one at 0.1% fraud, so I would report recall, precision and a PR curve at the operating point, measured on a time-based, untouched test set.

**Clarifying questions:**
- What does a missed fraud cost versus a false alarm (money, customer friction)? This sets the operating point, because accuracy treats both errors as equal.
- How many cases can the review team or the auto-decline path handle? A capacity limit turns the question into precision and recall at a fixed volume.
- When do labels mature (chargebacks)? Recent transactions may look cleaner than they are, so the test window must be mature.
- Is the 99.8% measured on a random split or on later weeks? A random split can flatter a fraud model.
- Is the 0.1% the real production rate? If the test set was resampled, precision on it is not the live precision.

**Approach:**
1. Do the arithmetic first. Flag-nothing scores 99.9%, so 99.8% is below a model that does nothing. But do not stop there: 99.8% can also hide a very good model (see Example). Accuracy carries no information at this base rate.
2. Split by time, not by row: train on older months, validate on the next, test on the most recent matured month. Keep the test set at the true 0.1% rate. Group by card or account if the same entity appears many times (see Book 1 Part 3 Q15, fraud model with a 0.1% positive rate: design the evaluation end to end).
3. Count positives in the test slice. A 20% random slice holds about 400 frauds; a one-week slice might hold far fewer. The interval on recall depends on that count, not on the 2,000,000 rows.
4. Report the confusion matrix, precision, recall, PR-AUC with the no-skill line at 0.001, and precision at the capacity the team can handle (Book 1 Part 3 Q25, capacity-constrained operating point).
5. Translate to money: expected frauds caught, expected false alarms per day, and the cost of each.

**Metrics:**
- Recall = TP / (TP + FN). Denominator is all 2,000 frauds.
- Precision = TP / (TP + FP). Denominator is everything flagged.
- PR-AUC (average precision). No-skill baseline = prevalence = 2,000 / 2,000,000 = 0.001.
- False-alarm rate per 1,000 transactions = FP / 2,000,000 x 1,000, or customers blocked per day.
- Guardrails: approval rate of good customers, review-queue size, interval on recall from the positive count.

**Risks:**
- Reading "99.8% below 99.9%" as proof the model is bad. It is not proof either way.
- Random split with many rows per card: the same card sits in train and test.
- A test set too small in positives, so recall moves by several points from sampling noise.
- Resampled test data: precision on it is not the live precision.

**What the interviewer scores:**
- Strong: names that accuracy is uninformative here and shows two models with the same accuracy. Weak: "accuracy is low, so improve it".
- Strong: time-based split, mature labels, test left at the true rate. Weak: random split and a balanced test set.
- Strong: gives recall with an interval and precision at a capacity. Weak: one F1 number.
- Strong: converts errors to money and queue size. Weak: stops at metric names.

**Example:** (illustrative numbers) Model A catches 1,500 of 2,000 frauds with 3,500 false alarms: 4,000 errors, accuracy 99.8%, recall 0.75, precision 0.30. Model B catches nothing and wrongly flags 2,000 good transactions: also 4,000 errors, accuracy 99.8%, recall 0, precision 0. Same accuracy, opposite value. A is 300 times better than random flagging (0.30 versus 0.001). On a 20% random test slice (400 frauds) recall 0.75 has an interval of about 0.705 to 0.792; on a 5% slice (100 frauds) it widens to about 0.653 to 0.831.
- Weak: "99.8% is almost the same as 99.9%, ship it" or "it is lower than the baseline, so it fails".
- Strong: "Accuracy cannot separate these. Show me recall 0.75 at precision 0.30 on a mature, time-split test of 400 frauds, with the interval, and the queue it creates."

**Code:**
```python
# Q1 fraud 0.1%: accuracy cannot tell a good model from a bad one (illustrative numbers)
import numpy as np
from scipy.stats import beta

N, P = 2_000_000, 2_000
Nn = N - P
assert P / N == 0.001
base_acc = Nn / N
print(f"flag-nothing accuracy: {base_acc:.4f}")
assert abs(base_acc - 0.999) < 1e-12

def report(name, tp, fp):
    fn = P - tp; tn = Nn - fp
    assert tp + fp + fn + tn == N
    acc = (tp + tn) / N
    prec = tp / (tp + fp) if tp + fp else float('nan')
    rec = tp / P
    print(f"{name:34s} errors={fp+fn:5d} acc={acc:.4f} precision={prec:.3f} recall={rec:.3f}")
    return acc, prec, rec

# Two very different models, both with accuracy 99.8% (4,000 errors out of 2,000,000)
accA, precA, recA = report("A: catches 1,500, 3,500 false alarms", 1500, 3500)
accB, precB, recB = report("B: catches 0, 2,000 false alarms", 0, 2000)
assert abs(accA - 0.998) < 1e-9 and abs(accB - 0.998) < 1e-9
assert recB == 0 and recA == 0.75 and abs(precA - 0.3) < 1e-9

# PR-AUC baseline for a no-skill model equals the prevalence
print(f"no-skill precision at any recall = {P/N:.4f}; model A is {precA/(P/N):.0f}x better than random flagging")
assert round(precA / (P / N)) == 300

# How many frauds does a random test slice hold, and how wide is the recall interval?
for frac in (0.20, 0.05):
    pos = int(P * frac)
    lo, hi = beta.ppf(0.025, int(0.75*pos), pos - int(0.75*pos) + 1), beta.ppf(0.975, int(0.75*pos) + 1, pos - int(0.75*pos))
    print(f"test slice {frac:.0%}: {pos} frauds, recall 0.75 has 95% interval [{lo:.3f}, {hi:.3f}]")
    if frac == 0.20: assert (hi - lo) < 0.10 and pos == 400
    else: assert (hi - lo) > 0.15 and pos == 100
```

**Output (my run):**
```text
flag-nothing accuracy: 0.9990
A: catches 1,500, 3,500 false alarms errors= 4000 acc=0.9980 precision=0.300 recall=0.750
B: catches 0, 2,000 false alarms   errors= 4000 acc=0.9980 precision=0.000 recall=0.000
no-skill precision at any recall = 0.0010; model A is 300x better than random flagging
test slice 20%: 400 frauds, recall 0.75 has 95% interval [0.705, 0.792]
test slice 5%: 100 frauds, recall 0.75 has 95% interval [0.653, 0.831]
```

**Follow-ups:**
- Which single number would you give the manager? None alone. Recall at a precision or queue size that the business agrees (for example recall at 30% precision), plus PR-AUC.
- Would you balance the test set? No. Balance only the training data if needed. The test set keeps the true rate so precision is honest.
- What if the test slice has only 100 frauds? Widen the window (more weeks) or use repeated time-based folds, and report the interval.

**Common mistakes:** Quoting accuracy at all. Random row split with repeated cards. Balancing the test set. Reporting recall with no count of positives. Calling 99.8% "a failure" without saying it is meaningless in both directions.

### Q2 ⭐⭐⭐ 🟢 A colleague balanced a table of 10,000 rows (500 positives, 5%) to 50/50 with SMOTE and only then split it into train and test, and test recall came out at 0.93. After launch the recall measured on real traffic is 0.55. Explain what most likely went wrong and how you would redo the experiment.
**Asked at:** Imbalanced-data and fraud-evaluation guides (techinterview.org 'Handling Imbalanced Datasets in Machine Learning', Dataford fraud-evaluation prompts such as 'how do you evaluate a fraud detection model on imbalanced data', a KDnuggets piece on SMOTE misuse, a Coresignal 'class imbalance interview trap' post); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Most likely the test set contained synthetic copies of training neighbours, so 0.93 measured memory, not skill; I would split first, oversample only the training fold, and test on real untouched rows.

**Clarifying questions:**
- Was SMOTE (or any resampling, dedup, scaling, imputation) applied to the whole table before the split? That is the leakage path.
- Is the real-traffic recall measured on the same label definition and a matured window? Otherwise part of 0.93 versus 0.55 is label timing.
- Does the same customer or entity appear in several rows? Then a plain split also leaks, apart from SMOTE.
- What is the live positive rate and the live threshold? Recall depends on the threshold chosen on the balanced data.
- Which model was used? A flexible model (trees, nearest neighbours) memorises neighbours and shows the leak more.

**Approach:**
1. State the mechanism. SMOTE makes each synthetic positive by interpolating between two real positives. After a random split, a synthetic point in the test set has its parents (or their close siblings) in the training set. The model "recognises" the neighbourhood. That is not generalisation.
2. Check it. Count how many test positives are synthetic. Here that count is the clue.
3. Redo the experiment in order: split the real rows first (stratified, time-based or grouped as the problem needs), fit resampling and all preprocessing inside the training fold only, tune with cross-validation where the resampling is inside each fold, then score once on real, untouched, 5%-positive test rows. See Book 1 Part 3 Q10 (where in the pipeline do you apply SMOTE or resampling).
4. Report on the real test set: recall and precision at the live threshold, PR-AUC, with the interval from the positive count.
5. Compare with the alternatives that do not touch the data: class weights or threshold tuning (Book 1 Part 3 Q11, class weights versus resampling).

**Metrics:**
- Recall = TP / all real positives in the real test set (not synthetic ones).
- Precision = TP / flagged, on the real 5% test set, not on a 50/50 set. Precision on a balanced test set is not the live precision.
- Count of real positives in test, and the interval on recall.
- Guardrail: share of test positives that are synthetic must be zero.

**Risks:**
- Synthetic neighbours in test make every flexible model look excellent.
- A balanced test set also inflates precision and distorts the threshold.
- Cross-validation with SMOTE outside the fold has the same leak.
- Blaming "distribution shift" when the offline number was never valid.

**What the interviewer scores:**
- Strong: names the mechanism (synthetic points near their parents) and checks it. Weak: "overfitting" with no cause.
- Strong: exact fix order (split, then resample the train fold only, test untouched). Weak: "use a bigger test set".
- Strong: notes the balanced test also breaks precision. Weak: only talks about recall.
- Strong: offers weights or thresholds as simpler options. Weak: "use ADASYN instead".

**Example:** (illustrative numbers, my run) 10,000 rows, 500 positives (5%), weak signal. Oversampling the whole table to 50/50 adds 9,000 synthetic positives, giving 19,000 rows. After an 80/20 random split the test set has 3,800 rows, 1,800 of them synthetic, which is 95% of the test positives. A 1-nearest-neighbour model scores recall 0.996 there. Done correctly (split first, 100 real test positives out of 2,000 real rows) the same model scores recall 0.220. The 0.93 versus 0.55 in the prompt has the same direction: the big gap is the clue, not "bad luck".
- Weak: "Recall dropped, the live data must have drifted."
- Strong: "0.93 was measured on a test set built from the training neighbourhood. I would re-split first, resample inside the training fold, and expect a number near the live 0.55."

**Code:**
```python
# Q2 SMOTE before the split: synthetic points leak into the test set (illustrative data)
import numpy as np
from scipy.spatial import cKDTree

rng = np.random.default_rng(11)
n, d = 10_000, 6
y = np.zeros(n, int); y[:500] = 1                      # 500 positives = 5%
rng.shuffle(y)
assert y.sum() == 500 and y.mean() == 0.05
X = rng.normal(size=(n, d)); X[y == 1] += 0.5          # weak signal, classes overlap

def smote(X, y, rng, k=5):
    """Oversample class 1 to a 50/50 mix: new point = a + u*(neighbour - a), neighbour among k nearest positives."""
    P = X[y == 1]; need = (y == 0).sum() - len(P)
    nn = cKDTree(P).query(P, k + 1)[1][:, 1:]
    i = rng.integers(0, len(P), need); j = nn[i, rng.integers(0, k, need)]
    u = rng.random((need, 1))
    Xs = P[i] + u * (P[j] - P[i])
    return np.vstack([X, Xs]), np.r_[y, np.ones(need, int)]

def one_nn_recall(Xtr, ytr, Xte, yte):
    pred = ytr[cKDTree(Xtr).query(Xte, 1)[1]]            # 1-nearest-neighbour: memorises its neighbourhood
    return pred[yte == 1].mean(), pred[yte == 0].mean()

# WRONG: SMOTE the whole table, then split
Xb, yb = smote(X, y, rng)
assert abs(yb.mean() - 0.5) < 1e-9 and len(yb) == 19_000
idx = rng.permutation(len(yb)); cut = int(0.8 * len(yb))
tr, te = idx[:cut], idx[cut:]
r_wrong, fpr_wrong = one_nn_recall(Xb[tr], yb[tr], Xb[te], yb[te])
n_syn_in_test = (te >= n).sum()
print(f"WRONG: test rows={len(te)}, synthetic positives in test={n_syn_in_test} ({n_syn_in_test/(yb[te]==1).sum():.0%} of test positives)")
print(f"WRONG: test recall = {r_wrong:.3f}")

# RIGHT: split the real rows first (stratified), SMOTE the training part only, test on real untouched rows
idx1 = np.flatnonzero(y == 1); idx0 = np.flatnonzero(y == 0)
rng.shuffle(idx1); rng.shuffle(idx0)
te_real = np.r_[idx1[:100], idx0[:1900]]; tr_real = np.r_[idx1[100:], idx0[1900:]]
assert len(te_real) == 2000 and y[te_real].mean() == 0.05
Xtr, ytr = smote(X[tr_real], y[tr_real], rng)
r_right, fpr_right = one_nn_recall(Xtr, ytr, X[te_real], y[te_real])
print(f"RIGHT: real test rows={len(te_real)}, positives={y[te_real].sum()}, test recall = {r_right:.3f}, false-positive rate = {fpr_right:.3f}")
assert r_wrong > 0.85 and r_right < r_wrong - 0.3
```

**Output (my run):**
```text
WRONG: test rows=3800, synthetic positives in test=1800 (95% of test positives)
WRONG: test recall = 0.996
RIGHT: real test rows=2000, positives=100, test recall = 0.220, false-positive rate = 0.126
```

**Follow-ups:**
- Is live 0.55 now "correct"? It is the honest number for that threshold and population. If it is too low, tune the threshold or weights on a clean validation set.
- Does SMOTE inside each CV fold fix it? Yes for the leak. Whether SMOTE helps at all is a separate question; with strong learners, weights and thresholds are often as good.
- Any other leak possible here? Yes: duplicates and repeated entities across train and test. Split by entity.

**Common mistakes:** Resampling before the split. Resampling the validation or test fold. Reading precision off a balanced test set. Fitting scalers or imputers on all rows. Keeping the leaky number because "it is just the test set".

### Q3 ⭐⭐⭐ 🟢 A model on a data set with 0.2% positives reports ROC-AUC 0.97 but PR-AUC only 0.18, and the stakeholder asks which number to believe. Explain what each metric measures here, what a no-skill model would score on PR-AUC, and what you would show the business.
**Asked at:** Imbalanced-data and fraud-evaluation guides (techinterview.org 'Handling Imbalanced Datasets in Machine Learning', Dataford fraud-evaluation prompts such as 'how do you evaluate a fraud detection model on imbalanced data', a KDnuggets piece on SMOTE misuse, a Coresignal 'class imbalance interview trap' post); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Both numbers can be true at once; ROC-AUC ignores how many negatives there are, PR-AUC does not, and at 0.2% positives a no-skill model scores 0.002 on PR-AUC, so I would show the business precision and recall at a workable queue size.

**Clarifying questions:**
- How many positives are in the evaluation set? PR-AUC is noisy with few positives, so it needs an interval.
- Is the evaluation set at the real 0.2% rate? If it was resampled, PR-AUC is not the live PR-AUC.
- What is the action and capacity (review 1,000 a day, block automatically)? That fixes where on the curve we operate.
- What does a false alarm cost compared with a miss? That decides the point on the curve.
- Which PR-AUC computation is it: average precision or trapezoid? They differ slightly (Book 1 Part 3 Q27, PR-AUC: what is its random baseline, and what is the difference between average precision and trapezoidal area under the PR curve).

**Approach:**
1. Say what each measures. ROC-AUC = chance that a random positive scores above a random negative; the false-positive rate uses all negatives as its denominator, so a tiny rate looks great. PR-AUC averages precision over recall levels; precision has false positives in its numerator, so it feels the huge negative class.
2. Give the baseline. No-skill PR-AUC equals the prevalence, 0.002. So 0.18 is about 90 times better than random. It is real skill, and it is also far from "0.97".
3. Believe both, but use PR-AUC to judge usefulness. Book 1 Part 3 Q6 (ROC-AUC versus PR-AUC on imbalanced problems) covers the choice.
4. Show the business a table: for queue sizes 500, 1,000, 5,000: true positives found, precision, recall, compared with a random queue.
5. Put an interval on it (bootstrap on the positives) and confirm on a later time window.

**Metrics:**
- ROC-AUC = P(score of random positive > score of random negative); ties count half.
- PR-AUC (average precision) = mean of precision at each true positive, with the cut-off going down the ranking.
- Precision at k = positives in the top k / k. Recall at k = positives in the top k / all positives.
- Lift at k = precision at k / prevalence.
- Guardrail: number of positives in the evaluation set.

**Risks:**
- Showing the ROC curve to the business: it hides the false-alarm volume.
- Comparing PR-AUC across data sets with different prevalence.
- Averaging precision from a small, noisy positive count.
- Reading 0.18 as "bad" without the 0.002 baseline.

**What the interviewer scores:**
- Strong: states the denominator difference and the no-skill baseline. Weak: "PR-AUC is better, trust it".
- Strong: translates to queue size, hits and false alarms. Weak: gives two AUCs and stops.
- Strong: notes the interval and prevalence dependence. Weak: compares PR-AUC across different data sets.
- Strong: does not drop ROC-AUC; it is still a valid ranking measure. Weak: "ROC-AUC is wrong".

**Example:** (illustrative simulation, my run) 1,000,000 transactions, 2,001 positives (0.20%). ROC-AUC 0.971, PR-AUC 0.143, no-skill 0.002, so about 70 times random. To catch 80% of positives the false-positive rate is only 0.041, which sounds tiny, but 0.041 of about 998,000 negatives is 41,163 false alarms against 1,601 hits: precision 0.037. A 1,000-transaction review queue finds 274 true positives (precision 0.274, recall 0.137), where a random queue finds 2. The same score shape at 20% prevalence gives ROC-AUC 0.970 and PR-AUC 0.889: same ranking quality, very different PR-AUC. The prompt's 0.18 is in the same range; my 0.143 is from my simulated scores.
- Weak: "AUC is 0.97, the model is excellent."
- Strong: "The ranking is good, but at 0.2% a useful queue needs precision, so I would show hits per 1,000 reviews against a random queue."

**Code:**
```python
# Q3 ROC-AUC 0.97 vs PR-AUC 0.18 at 0.2% positives (illustrative simulation)
import numpy as np
from scipy.stats import rankdata, norm

rng = np.random.default_rng(3)
n, prev = 1_000_000, 0.002
y = (rng.random(n) < prev).astype(int)
pos = int(y.sum())
sg = 1.3                                         # negatives are more spread out than positives
d = norm.ppf(0.97) * (1 + sg**2) ** 0.5          # shift that gives ROC-AUC = 0.97
s = rng.normal(size=n) * np.where(y == 1, 1.0, sg) + d * y

def roc_auc(y, s):
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)

def avg_precision(y, s):
    o = np.argsort(-s); yy = y[o]
    tp = np.cumsum(yy); k = np.arange(1, len(yy) + 1)
    return (tp / k)[yy == 1].mean()                # mean precision at each true positive

auc = roc_auc(y, s); ap = avg_precision(y, s)
print(f"positives={pos} ({pos/n:.2%}); ROC-AUC={auc:.3f}; PR-AUC (average precision)={ap:.3f}; no-skill PR-AUC={prev}")
assert 0.965 < auc < 0.975 and 0.10 < ap < 0.30
assert ap / prev > 50                              # far better than random, but far from 0.97

# Why: at recall 0.80 the false-positive rate looks tiny, yet false alarms swamp the hits
thr = np.quantile(s[y == 1], 0.20)                 # keeps 80% of positives
flag = s >= thr
tp = (flag & (y == 1)).sum(); fp = (flag & (y == 0)).sum()
fpr = fp / (y == 0).sum(); prec = tp / (tp + fp)
print(f"at recall 0.80: FPR={fpr:.3f}, flagged={flag.sum()}, TP={tp}, FP={fp}, precision={prec:.3f}")
assert fpr < 0.06 and prec < 0.05

# Same scores shape, but 20% prevalence: ROC-AUC unchanged, PR-AUC much higher
y2 = (rng.random(200_000) < 0.2).astype(int); s2 = rng.normal(size=200_000) * np.where(y2 == 1, 1.0, sg) + d * y2
print(f"prevalence 20%: ROC-AUC={roc_auc(y2,s2):.3f}, PR-AUC={avg_precision(y2,s2):.3f}")
assert abs(roc_auc(y2, s2) - auc) < 0.01 and avg_precision(y2, s2) > 0.8

# Business view: a review queue of 1,000 transactions out of 1,000,000
top = np.argsort(-s)[:1000]
print(f"top 1,000 flagged: {y[top].sum()} true positives (precision {y[top].mean():.3f}), recall {y[top].sum()/pos:.3f}; random queue would find {1000*prev:.0f}")
assert y[top].sum() > 100
```

**Output (my run):**
```text
positives=2001 (0.20%); ROC-AUC=0.971; PR-AUC (average precision)=0.143; no-skill PR-AUC=0.002
at recall 0.80: FPR=0.041, flagged=42764, TP=1601, FP=41163, precision=0.037
prevalence 20%: ROC-AUC=0.970, PR-AUC=0.889
top 1,000 flagged: 274 true positives (precision 0.274), recall 0.137; random queue would find 2
```

**Follow-ups:**
- Can ROC-AUC still be useful? Yes, for comparing rankers on the same population and for the front of the ranking (partial AUC), but not for volume decisions.
- Could precision at 0.037 still be acceptable? If a false alarm is cheap (an automated step-up check) and a miss is expensive, yes. The cost ratio decides.
- Does PR-AUC change if the live rate changes? Yes. Precision depends on prevalence; ROC-AUC does not (Book 1 Part 3 Q30, precision depends on class prevalence).

**Common mistakes:** Quoting ROC-AUC alone. Forgetting the PR no-skill baseline. Comparing PR-AUC across different prevalences. Showing the ROC curve to non-technical stakeholders. Resampling the evaluation set and quoting PR-AUC as if live.

### Q4 ⭐⭐⭐ 🟢 In a survey of 10,000 users, income is missing for 2,200 (22%). The missing share is 40% among the 4,000 users over 55 (1,600 users) and 10% among the other 6,000 users (600 users). Explain whether this looks like MCAR, MAR or MNAR, what you can and cannot test from the data, and what you would do before modelling.
**Asked at:** Missing-data interview explainers (a PrachHub 'Missing Data, Imputation, And Selection Bias' concept page, ydata.ai 'understanding missing data mechanisms', a Towards Data Science 'Talking About Missing Data' article, a Daily Dose of Data Science post on three types of missing values); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** It is not MCAR, because missingness clearly depends on age; it looks like MAR given age, but the data alone can never rule out MNAR, so I would model it with age and a missing flag and test sensitivity.

**Clarifying questions:**
- How was income asked (open field, range bucket, optional)? Optional sensitive fields are often skipped for reasons tied to the value itself.
- Is the gap in older users due to survey channel or device (for example phone survey versus app)? A channel effect is a MAR cause I can observe.
- What is income used for: a feature, a segment, or a population estimate? An estimate of the mean needs more care than a feature.
- Is there any external anchor (a verified subsample, a census-style margin)? It is the only way to check MNAR.
- Can we re-contact a random sample of the missing users? A small follow-up sample is the strongest fix.

**Approach:**
1. Define the three cases in one line each. MCAR: missingness unrelated to anything. MAR: related to things I observed (age). MNAR: related to the missing value itself (rich people hide income).
2. Test what I can. Missing rate by age is 40% versus 10%, a chi-square on that table gives p near 1e-275 in my run. So MCAR is rejected. Next, look at missingness against other observed variables (city, device, tenure).
3. State what I cannot test. Whether income itself drives missingness, after conditioning on age, is not visible, because the missing values are missing. MAR versus MNAR rests on knowledge of the process and an outside anchor, not on a test.
4. Before modelling: do not drop rows (complete-case analysis over-weights the young group). Add the missing flag, impute inside the training fold using age (or multiple imputation), and keep age in the model. See Book 1 Part 12 Q2 (audit missing values, impute sensibly, statistics from the training split only).
5. Run a sensitivity check: shift imputed incomes up or down by plausible amounts and see whether the conclusion changes. If it does, collect data (follow-up sample).

**Metrics:**
- Missing rate by group = missing in group / users in group. Here 1,600 / 4,000 = 40% and 600 / 6,000 = 10%; overall 2,200 / 10,000 = 22%.
- Chi-square test of independence of missing flag and age group (numerators: observed minus expected counts).
- Bias of the estimate: estimated mean minus truth (only known in a simulation or an anchor sample).
- Guardrails: model metric with and without the missing flag; shift of the income distribution after imputation.

**Risks:**
- Saying "MAR" with confidence. It is an assumption.
- Complete-case mean: it over-represents the 10%-missing group.
- Mean imputation shrinks variance and hides the relationship.
- Treating a significant chi-square as proof of MNAR. It only shows that missingness depends on age.

**What the interviewer scores:**
- Strong: correct definitions, and says what is and is not testable. Weak: "run a test to find out if it is MNAR".
- Strong: uses the observed pattern (age) in the imputation and keeps a missing flag. Weak: drop rows or fill with the global mean.
- Strong: proposes sensitivity analysis or a follow-up sample. Weak: stops at the label.
- Strong: leakage-safe imputation in the training fold. Weak: impute on the full table.

**Example:** (illustrative index units, not currency) Counts: 40% of 4,000 older users (1,600) and 10% of 6,000 younger ones (600) are missing, 22% overall. In my simulation both worlds show the same 40% / 10% pattern. In the MAR world only age drives missingness, the true mean is 88.8, the complete-case mean is 91.7 (biased up because younger, higher earners dominate), and the age-adjusted estimate is 88.9. In the MNAR world high earners also hide income inside each age group: true mean 88.0, complete-case 87.0, age-adjusted 83.6, so the adjustment overcorrects and is wrong by 4.4. From the observed data the two worlds look the same.
- Weak: "It is MAR because age explains it."
- Strong: "Age explains much of it, so not MCAR. Whether it is only age I cannot test, so I model with age and a missing flag and check sensitivity."

**Code:**
```python
# Q4 income missing 22%: pattern by age, what the data can and cannot say (illustrative data)
import numpy as np
from scipy.stats import chi2_contingency

# Counts from the prompt
old_n, young_n = 4_000, 6_000
old_miss, young_miss = 1_600, 600
assert old_miss / old_n == 0.40 and young_miss / young_n == 0.10
assert old_miss + young_miss == 2_200 and (old_miss + young_miss) / (old_n + young_n) == 0.22
tab = np.array([[old_miss, old_n - old_miss], [young_miss, young_n - young_miss]])
chi2, p, _, _ = chi2_contingency(tab, correction=False)
print(f"missing vs age group: chi2={chi2:.0f}, p={p:.2e}  -> not MCAR (missingness depends on age)")
assert p < 1e-100

# Two worlds with the SAME observed missing rates by age (40% / 10%) but different mechanisms
rng = np.random.default_rng(5)
def world(mnar):
    old = np.r_[np.ones(old_n, bool), np.zeros(young_n, bool)]
    mean = np.where(old, 70.0, 100.0)                    # income index: older group lower on average
    inc = mean * rng.lognormal(0, 0.4, len(old)) / np.exp(0.08)
    base = np.where(old, 0.40, 0.10)
    if mnar:                                             # within each age group, high earners hide income more
        miss = np.zeros(len(old), bool)
        for g, rate in ((True, 0.40), (False, 0.10)):
            idx = np.flatnonzero(old == g)
            rank = inc[idx].argsort().argsort() / len(idx)          # 0..1 within group
            w = 0.2 + 1.6 * rank; w = w / w.mean() * rate           # exact group mean = rate
            miss[idx] = rng.random(len(idx)) < np.minimum(w, 1)
    else:
        miss = rng.random(len(old)) < base                          # depends on age only
    return old, inc, miss

for label, mnar in (("MAR (age only)", False), ("MNAR (also income)", True)):
    old, inc, miss = world(mnar)
    obs = ~miss
    true_mean = inc.mean()
    cc = inc[obs].mean()                                             # complete-case mean
    # MAR repair: group means among observed, weighted by the true age mix
    adj = old.mean() * inc[obs & old].mean() + (1 - old.mean()) * inc[obs & ~old].mean()
    print(f"{label:20s} missing by age: {miss[old].mean():.3f} / {miss[~old].mean():.3f}  "
          f"true mean={true_mean:.1f}  complete-case={cc:.1f}  age-adjusted={adj:.1f}")
    if not mnar:
        assert abs(adj - true_mean) < 1.5 and abs(cc - true_mean) > 2     # adjustment works under MAR
    else:
        assert abs(adj - true_mean) > 3                                    # adjustment fails under MNAR
```

**Output (my run):**
```text
missing vs age group: chi2=1259, p=1.05e-275  -> not MCAR (missingness depends on age)
MAR (age only)       missing by age: 0.406 / 0.104  true mean=88.8  complete-case=91.7  age-adjusted=88.9
MNAR (also income)   missing by age: 0.400 / 0.107  true mean=88.0  complete-case=87.0  age-adjusted=83.6
```

**Follow-ups:**
- Which imputation would you use? Group-aware (regression or multiple imputation on age and other fields) plus a missing flag, fitted inside the training fold. Trees can also use missing natively (Book 1 Part 4 Q14, how tree-based models handle missing values).
- How would you check MNAR? A verified subsample of the missing users, or an external margin, or sensitivity scenarios. Not a test on the observed data.
- Does the missing flag leak? Not by itself, but check it will exist at serving time with the same meaning (Q7).

**Common mistakes:** Calling it MAR as a fact. Dropping incomplete rows. Imputing the global mean. Computing imputation statistics before the split. Forgetting that a chi-square on age says nothing about the income value itself.

### Q5 ⭐⭐⭐ 🟡 A churn model runs on 100,000 customers a month, of whom 4% (4,000) actually churn, and the retention team can only phone 2,000 customers a month. The data scientist proposes optimising F1 at the default 0.5 threshold. Explain which metric and threshold rule you would use instead and how you would report the expected result.
**Asked at:** Imbalanced-data and fraud-evaluation guides (techinterview.org 'Handling Imbalanced Datasets in Machine Learning', Dataford fraud-evaluation prompts such as 'how do you evaluate a fraud detection model on imbalanced data', a KDnuggets piece on SMOTE misuse, a Coresignal 'class imbalance interview trap' post); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** With only 2,000 calls, F1 at 0.5 is the wrong target; I would rank by churn probability, call the top 2,000, and report precision at 2,000, recall at 2,000 and lift over a random list, with the money attached.

**Clarifying questions:**
- Is the call limit hard (2,000 a month) and are calls to the same person repeatable? A hard cap makes this a ranking problem.
- What does a successful save earn, and what does a call cost? That decides whether using the full 2,000 is worth it.
- Does the offer work on everybody, or only on those who would leave and can be persuaded? Churn risk is not the same as being saveable (uplift).
- Are the scores calibrated? A threshold in probability units only means something if they are.
- How soon after the call is churn measured? That fixes the evaluation window.

**Approach:**
1. Frame it as a budgeted ranking: pick the 2,000 customers with the highest expected value. If scores are calibrated, expected value is p x save-rate x value minus call cost.
2. Choose the rule: contact the top 2,000 by score, but stop earlier if the score falls below break-even (cost / (save-rate x value)). The threshold then comes from capacity and money, not from 0.5 or from F1 (Book 1 Part 3 Q12, how do you choose the classification threshold, and Q25, capacity-constrained operating point).
3. Report in the business unit: expected churners reached, precision at 2,000, recall at 2,000 and the maximum possible recall, lift over random.
4. Validate with a time-based hold-out and a random control group that is not called, so the benefit is measured and not assumed.
5. If the team says the offer only works on persuadable people, move to uplift modelling (a separate problem).

**Metrics:**
- Precision@2,000 = churners among the 2,000 called / 2,000.
- Recall@2,000 = churners among the 2,000 called / all churners that month (about 4,000). Its ceiling is 2,000 / 4,000 = 50%, even with a perfect model.
- Lift@2,000 = precision@2,000 / base rate (4%).
- Expected profit = sum over called of (p x save-rate x value - cost).
- Guardrails: calibration of scores in the top decile, call volume, complaint or opt-out rate.

**Risks:**
- Quoting recall without the 50% ceiling: 0.20 can look poor when the ceiling is 0.48.
- Default 0.5 threshold flags too few; F1-optimal threshold flags more than capacity.
- Calibration drift: the break-even rule needs probabilities.
- Targeting the most likely churners wastes calls on customers who would leave anyway.

**What the interviewer scores:**
- Strong: converts capacity into a top-k rule and states the recall ceiling. Weak: "use F1, tune the threshold".
- Strong: ties the cut-off to value and cost. Weak: ignores money.
- Strong: asks about uplift and a control group. Weak: assumes risk equals benefit.
- Strong: reports expected results with units (churners reached per month). Weak: reports AUC.

**Example:** (illustrative simulation, my run; the simulation draws 4,130 churners, about the 4,000 in the prompt) 100,000 customers, 4.1% churn, calibrated scores.
| Rule | Flagged | Hits | Precision | Recall |
|---|---|---|---|---|
| Threshold 0.5 | 422 | 262 | 0.621 | 0.063 |
| F1-optimal (threshold 0.157) | 5,478 | 1,587 | 0.290 | 0.384 |
| Top 2,000 | 2,000 | 841 | 0.420 | 0.204 |
The default rule leaves 1,578 calls unused. The F1 rule needs 5,478 calls, nearly three times the capacity. The top-2,000 rule reaches 841 churners, lift 10.5 over random (80 hits). Max possible recall at 2,000 calls is 2,000 / 4,130 = 0.484. With invented value 100, save-rate 20% and call cost 3, break-even score is 0.15, so 5,900 customers are worth calling and the cap of 2,000 binds; expected profit about 10,550 units.
- Weak: "F1 at 0.5 is the standard metric."
- Strong: "I would call the top 2,000, report 841 expected hits and 42% precision against a ceiling of 48% recall, and keep a control group."

**Code:**
```python
# Q5 churn: 100,000 customers, 4% churn, capacity 2,000 calls (illustrative simulation)
import numpy as np

rng = np.random.default_rng(21)
N, CAP = 100_000, 2_000
z = rng.normal(size=N)
def sig(x): return 1 / (1 + np.exp(-x))
lo, hi = -8.0, 0.0
for _ in range(60):                         # find intercept so that mean probability = 4%
    mid = (lo + hi) / 2
    if sig(mid + 1.6 * z).mean() > 0.04: hi = mid
    else: lo = mid
p = sig(lo + 1.6 * z)                       # treat p as a calibrated model score
y = (rng.random(N) < p).astype(int)
print(f"churners={y.sum()} ({y.mean():.2%}); mean score={p.mean():.4f}")
assert abs(y.sum() - 4000) < 200

def stats(flag):
    tp = (flag & (y == 1)).sum(); k = flag.sum()
    prec = tp / k if k else float('nan'); rec = tp / y.sum()
    f1 = 2 * prec * rec / (prec + rec) if tp else 0.0
    return k, tp, prec, rec, f1

# 1) default 0.5 threshold
k, tp, pr, rc, f1 = stats(p >= 0.5)
print(f"threshold 0.5     : flagged={k:6d} TP={tp:4d} precision={pr:.3f} recall={rc:.3f} F1={f1:.3f}")
assert k < CAP / 4                                   # leaves most of the capacity unused

# 2) the F1-optimal threshold ignores the 2,000 limit
ths = np.quantile(p, np.linspace(0.5, 0.999, 400))
best = max(ths, key=lambda t: stats(p >= t)[4])
k, tp, pr, rc, f1 = stats(p >= best)
print(f"F1-optimal thr {best:.3f}: flagged={k:6d} TP={tp:4d} precision={pr:.3f} recall={rc:.3f} F1={f1:.3f}")
assert k > CAP                                       # asks for more calls than the team can make

# 3) capacity rule: call the top 2,000 by score
top = np.zeros(N, bool); top[np.argsort(-p)[:CAP]] = True
k, tp, pr, rc, f1 = stats(top)
exp_tp = p[top].sum()                                # expected hits from calibrated scores
print(f"top {CAP}          : flagged={k:6d} TP={tp:4d} precision={pr:.3f} recall={rc:.3f}  expected TP from scores={exp_tp:.0f}")
print(f"max possible recall at 2,000 calls = {CAP}/{y.sum()} = {CAP/y.sum():.3f}; random 2,000 would catch {CAP*0.04:.0f}; lift={pr/0.04:.1f}")
assert k == CAP and abs(tp - exp_tp) < 60 and pr / 0.04 > 5
assert rc <= CAP / y.sum() + 1e-12

# 4) value rule with a capacity cap: contact if p*save*value > cost  (invented: save 20%, value 100, call cost 3)
save, value, cost = 0.20, 100.0, 3.0
cut = cost / (save * value)
worth = p > cut
n_worth = int(worth.sum()); n_call = min(CAP, n_worth)
order = np.argsort(-p)[:n_call]
profit = (p[order] * save * value - cost).sum()
print(f"break-even score {cut:.2f}: {n_worth} customers above it; we call {n_call}; expected profit={profit:,.0f}")
assert n_call == CAP and profit > 0
# the lowest score among the 2,000 called, i.e. the threshold the capacity implies
print(f"implied threshold of the top-{CAP} rule: {p[order].min():.3f}")
```

**Output (my run):**
```text
churners=4130 (4.13%); mean score=0.0400
threshold 0.5     : flagged=   422 TP= 262 precision=0.621 recall=0.063 F1=0.115
F1-optimal thr 0.157: flagged=  5478 TP=1587 precision=0.290 recall=0.384 F1=0.330
top 2000          : flagged=  2000 TP= 841 precision=0.420 recall=0.204  expected TP from scores=828
max possible recall at 2,000 calls = 2000/4130 = 0.484; random 2,000 would catch 80; lift=10.5
break-even score 0.15: 5900 customers above it; we call 2000; expected profit=10,550
implied threshold of the top-2000 rule: 0.282
```

**Follow-ups:**
- What if capacity doubles? Recompute the cut at break-even: precision falls as we go down the list, so extra calls earn less each.
- What if scores are not calibrated? Calibrate on a held-out month first (Book 1 Part 3 Q14, model calibration), or use rank-based rules only.
- How do you prove it worked? Holdout: a random slice of the high-risk list is not called, and we compare churn.

**Common mistakes:** Optimising F1 at 0.5. Ignoring the call limit. Quoting recall without its ceiling. Treating churn risk as saveability. No control group.

### Q6 ⭐⭐⭐ 🟡 You trained a gradient-boosted model on data with a 1% positive rate using a class weight of 99 on positives, and the mean predicted probability on a validation sample is about 0.50 although the true rate is 1%. Finance wants to use the scores as probabilities to compute expected loss. Explain what happened and how you would restore usable probabilities.
**Asked at:** Imbalanced-data and fraud-evaluation guides (techinterview.org 'Handling Imbalanced Datasets in Machine Learning', Dataford fraud-evaluation prompts such as 'how do you evaluate a fraud detection model on imbalanced data', a KDnuggets piece on SMOTE misuse, a Coresignal 'class imbalance interview trap' post); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** A weight of 99 told the model that positives are as common as negatives, so it outputs probabilities for a 50/50 world; I would convert them back (divide the odds by 99) and then check calibration on an unweighted validation set.

**Clarifying questions:**
- Is the validation sample unweighted and at the real 1% rate? Calibration must be checked on data that looks like production.
- Is finance using the score as a probability per account (expected loss = probability x exposure), or only for ranking? Probabilities need calibration, ranking does not.
- Which library and what exactly was weighted (weights in the loss, `scale_pos_weight`, resampling)? The correction depends on the form.
- Do we have a recent holdout with matured labels? Calibration must be fitted on it, not on training rows.
- Does the model need to be stable across segments? A single global correction may not hold in every segment.

**Approach:**
1. Explain the cause. Weight 99 on 1% positives gives effective prevalence 99 x 0.01 / (99 x 0.01 + 0.99) = 0.50. The model learns the odds of a world where classes are balanced, so the mean score is near 0.50 (for a weak signal) instead of 0.01.
2. Check that ranking is fine. A monotone fix does not change AUC or the order of customers. Class weights are a reasonable training choice; they just break the scale (Book 1 Part 3 Q23, does class weighting, SMOTE or undersampling break probability calibration).
3. Repair with the prior (odds) correction: p_true = p_w / (p_w + 99 x (1 - p_w)).
4. Verify on an unweighted holdout: mean predicted versus observed rate, reliability by decile, log-loss, Brier score. For flexible models (boosted trees) the correction is only approximate, so also fit Platt or isotonic on the holdout (Book 1 Part 3 Q20).
5. Alternative: train without weights, and get ranking and thresholds from the clean probabilities directly. Hand finance the corrected, validated probability; document the version.

**Metrics:**
- Mean predicted probability versus observed positive rate on an unweighted holdout. Ratio near 1.
- Reliability by decile: mean prediction / observed rate per bin.
- Log-loss = mean of -[y log p + (1-y) log(1-p)]; Brier = mean of (p - y)^2.
- Expected positives = sum of p versus observed count.
- Guardrail: AUC unchanged by the correction.

**Risks:**
- Feeding weighted scores to finance: expected loss would be about 50x too high.
- Applying the correction formula to a model that was not weighted that way.
- Calibrating on the training data.
- One global correction hiding calibration errors in segments.

**What the interviewer scores:**
- Strong: derives the 0.50 from weights and prevalence. Weak: "the model is overfitting".
- Strong: gives the odds correction and verifies it on an unweighted holdout. Weak: "retrain without weights" with no check.
- Strong: notes ranking is unchanged. Weak: confuses ranking with probability.
- Strong: mentions Platt or isotonic as the empirical check. Weak: only the formula.

**Example:** (illustrative simulation, my run, positive rate about 1.1%, a weak-signal logistic model with weight 99 on positives) mean weighted score 0.4954 versus true rate 0.0113. After the odds correction the mean is 0.0112. AUC is 0.6538 before and after (same ranking). Log-loss drops from 0.7132 to 0.0600, equal to the unweighted model's 0.0600. Expected positives: 2,235 corrected versus 2,252 observed, while the raw weighted scores would imply 99,084 positives. With a much stronger signal the mean weighted score is lower (0.3318 in my run) but still about 30 times the true rate, so the prompt's "about 0.50" fits a weak-signal model; the diagnosis does not change.
- Weak: "The model is biased towards positives; use SMOTE."
- Strong: "The weight changed the base rate the model sees. Divide the odds by 99, check by decile on an unweighted holdout, and hand finance only the corrected scores."

**Code:**
```python
# Q6 class weight 99 at a 1% positive rate: scores become "weighted probabilities" (illustrative simulation)
import numpy as np
from scipy.stats import rankdata

rng = np.random.default_rng(9)
def sig(x): return 1 / (1 + np.exp(-x))
def make(n, rng, coef=(0.4, 0.3, 0.2), icpt=-4.6):
    X = rng.normal(size=(n, 3))
    logit = icpt + X @ np.array(coef)
    return X, (rng.random(n) < sig(logit)).astype(float)
Xtr, ytr = make(300_000, rng); Xva, yva = make(200_000, rng)
print(f"train positive rate={ytr.mean():.4f}, validation positive rate={yva.mean():.4f}")
assert 0.008 < ytr.mean() < 0.013

def fit(X, y, w, iters=30):                        # weighted logistic regression by Newton steps
    A = np.c_[np.ones(len(X)), X]; b = np.zeros(A.shape[1])
    for _ in range(iters):
        p = sig(A @ b); g = A.T @ (w * (p - y)); H = (A * (w * p * (1 - p))[:, None]).T @ A
        b -= np.linalg.solve(H, g)
    return b
def predict(b, X): return sig(np.c_[np.ones(len(X)), X] @ b)
def auc(y, s):
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
def logloss(y, p): return -np.mean(y * np.log(p) + (1 - y) * np.log(1 - p))

W = 99.0
b_plain = fit(Xtr, ytr, np.ones(len(ytr)))
b_w = fit(Xtr, ytr, np.where(ytr == 1, W, 1.0))
p_plain, p_w = predict(b_plain, Xva), predict(b_w, Xva)
print(f"mean predicted: unweighted={p_plain.mean():.4f}  weight-99={p_w.mean():.4f}  true rate={yva.mean():.4f}")
assert abs(p_plain.mean() - yva.mean()) < 0.002 and 0.4 < p_w.mean() < 0.6

# Why 0.50: the weight 99 makes positives count as many as negatives (effective prevalence)
eff = 99 * 0.01 / (99 * 0.01 + 0.99)
print(f"effective prevalence under weight 99 = {eff:.2f}")
assert abs(eff - 0.5) < 1e-9

# Fix 1: undo the weight in odds space: odds_true = odds_weighted / W
p_fix = p_w / (p_w + W * (1 - p_w))
print(f"after prior correction: mean predicted={p_fix.mean():.4f}")
assert abs(p_fix.mean() - yva.mean()) < 0.003

# Ranking is untouched (monotone transform), probabilities are repaired
print(f"AUC: weighted={auc(yva, p_w):.4f}  corrected={auc(yva, p_fix):.4f}  unweighted={auc(yva, p_plain):.4f}")
assert abs(auc(yva, p_w) - auc(yva, p_fix)) < 1e-12
print(f"log-loss: weighted raw={logloss(yva, p_w):.4f}  corrected={logloss(yva, p_fix):.4f}  unweighted={logloss(yva, p_plain):.4f}")
assert logloss(yva, p_fix) < logloss(yva, p_w) and abs(logloss(yva, p_fix) - logloss(yva, p_plain)) < 0.005

# Check by decile: expected loss uses probabilities, so compare mean prediction with observed rate per decile
q = np.quantile(p_fix, np.linspace(0, 1, 11)); d = np.clip(np.searchsorted(q, p_fix, side="right") - 1, 0, 9)
print("decile: observed rate vs mean corrected prediction")
for k in (0, 5, 9):
    m = d == k; print(f"  decile {k}: observed={yva[m].mean():.4f} predicted={p_fix[m].mean():.4f}")
tot_exp = p_fix.sum(); tot_obs = yva.sum()
print(f"expected positives={tot_exp:.0f} vs observed={tot_obs:.0f}; raw weighted scores would imply {p_w.sum():.0f}")
assert abs(tot_exp - tot_obs) / tot_obs < 0.1 and p_w.sum() > 20 * tot_obs

# Side note: with a much stronger signal the weighted mean is lower than 0.50 but still far above 1%
Xs, ys = make(300_000, rng, (1.2, 0.8, 0.5), -5.6); Xsv, ysv = make(200_000, rng, (1.2, 0.8, 0.5), -5.6)
bs = fit(Xs, ys, np.where(ys == 1, W, 1.0)); ps = predict(bs, Xsv)
print(f"strong-signal model: true rate={ysv.mean():.4f}, mean weight-99 score={ps.mean():.4f}")
assert ps.mean() > 10 * ysv.mean()
```

**Output (my run):**
```text
train positive rate=0.0112, validation positive rate=0.0113
mean predicted: unweighted=0.0112  weight-99=0.4954  true rate=0.0113
effective prevalence under weight 99 = 0.50
after prior correction: mean predicted=0.0112
AUC: weighted=0.6538  corrected=0.6538  unweighted=0.6540
log-loss: weighted raw=0.7132  corrected=0.0600  unweighted=0.0600
decile: observed rate vs mean corrected prediction
  decile 0: observed=0.0038 predicted=0.0040
  decile 5: observed=0.0103 predicted=0.0105
  decile 9: observed=0.0273 predicted=0.0247
expected positives=2235 vs observed=2252; raw weighted scores would imply 99084
strong-signal model: true rate=0.0114, mean weight-99 score=0.3318
```

**Follow-ups:**
- What if the model is a boosted tree? The same correction is a good first step, but check calibration on a holdout and fit isotonic or Platt there.
- Would you drop the weights? Weights can help trees find rare-class structure, so keep them if they help, and calibrate afterwards.
- Does finance need calibration by segment? If decisions differ by segment, yes: check reliability in each large segment.

**Common mistakes:** Using weighted scores as probabilities. Applying prior correction twice. Calibrating on the training data. Looking only at AUC. Assuming correction is exact for every model.

### Q7 ⭐⭐⭐ 🟡 In a loan dataset of 50,000 applications, income is missing for 15,000 (30%), and the default rate is 9% among applicants with missing income versus 4% among those who reported it. A teammate wants to fill the gaps with the median income and move on. Explain what you would investigate, how you would treat the missingness itself, and what could go wrong at serving time.
**Asked at:** Missing-data interview explainers (a PrachHub 'Missing Data, Imputation, And Selection Bias' concept page, ydata.ai 'understanding missing data mechanisms', a Towards Data Science 'Talking About Missing Data' article, a Daily Dose of Data Science post on three types of missing values); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Median fill alone throws away the strongest signal here, because applicants with missing income default at 9% versus 4%; I would investigate why it is missing, keep a missing flag next to the filled value, and make sure the flag is produced the same way at serving.

**Clarifying questions:**
- Why is income missing: optional form field, a channel (agent-assisted versus self-serve), a verification step that failed? The mechanism decides how to treat it.
- Does missingness correlate with other things we observe (channel, product, region, loan size)? Part of the 9% versus 4% may be explained by those.
- Is the field going to stay optional at serving time? If the form changes, the flag disappears.
- Is there another income proxy (bank-statement data, bureau data) we can use for those applicants? It reduces the need for imputation.
- May a missing field be used in a credit decision under policy and fair-lending rules? Missingness can proxy for a protected group or channel.

**Approach:**
1. Do the arithmetic. 15,000 missing x 9% = 1,350 defaults; 35,000 reported x 4% = 1,400 defaults; total 2,750 of 50,000 = 5.5%. The gap is large: two-proportion z about 22.5 in my run, so not sampling noise.
2. Investigate the mechanism. Compare missing versus reported on channel, product, region, loan size, time. Check if missingness rose at some date (a form change). Find who can say why the field is blank.
3. Treat the missingness as information: add the missing flag and fill the value inside the training fold (median or a model-based fill using other fields). Trees can handle it natively too (Book 1 Part 4 Q14).
4. Compare model versions on a time-based holdout: median fill only versus fill plus flag; also check calibration in the missing group.
5. Plan for serving: assert that nulls arrive as nulls, that the flag is computed in the same code path as in training, that the fill statistic is stored with the model, and monitor the missing share and the mean score for missing rows (Book 6 Part 2 Q5, the null rate jump after an upstream deploy).

**Metrics:**
- Default rate by group = defaults / applicants in the group: 9% (1,350 / 15,000) versus 4% (1,400 / 35,000).
- Test AUC and log-loss with and without the flag, on a time-based holdout.
- Calibration within the missing group: mean predicted versus observed default.
- Guardrails: share of missing at serving versus training, mean score of rows with a missing flag, imputation statistic fitted on training only.

**Risks:**
- Median fill hides the pattern and mixes missing applicants with real median earners.
- Flag lost or redefined at serving, so risky applicants get priced like average ones.
- Policy: a missing flag may act as a proxy for something we should not use.
- If the form later makes income mandatory, the flag's meaning changes, and the model needs retraining.

**What the interviewer scores:**
- Strong: checks the default-rate gap and investigates the cause. Weak: "median is fine".
- Strong: keeps a missing flag and fits the fill on the training fold. Weak: fills on the full table.
- Strong: thinks about serving behaviour and monitoring. Weak: stops at training.
- Strong: mentions policy and fairness review. Weak: ignores it.

**Example:** (illustrative simulation, my run) Prompt counts: 15,000 missing, 1,350 defaults; 35,000 reported, 1,400 defaults; overall 5.5%. In my simulation (26.9% missing, default rate 9.44% versus 4.09%, riskier applicants hide income more) a logistic model with median fill gets test AUC 0.6244; adding the missing flag gets 0.6777. If the flag is lost at serving while the fill continues, the mean predicted default for missing-income rows falls from 0.095 to 0.037 (actual 0.094), and AUC falls from 0.6777 to 0.6214: risky applicants are priced as average.
- Weak: "Fill with the median and move on."
- Strong: "The missing group defaults at more than twice the rate, so the missingness is a signal. I keep it as a flag, fit the fill on training data only, and monitor the flag at serving."

**Code:**
```python
# Q7 loan income 30% missing, defaults 9% vs 4%: median fill vs fill + missing flag (illustrative simulation)
import numpy as np
from scipy.stats import norm, rankdata

# Prompt arithmetic
n_all, n_miss = 50_000, 15_000
d_miss, d_obs = 0.09 * n_miss, 0.04 * (n_all - n_miss)
print(f"missing: {n_miss} rows, defaults {d_miss:.0f}; reported: {n_all-n_miss} rows, defaults {d_obs:.0f}; overall default rate {(d_miss+d_obs)/n_all:.3%}")
assert n_miss / n_all == 0.30 and d_miss == 1350 and d_obs == 1400 and abs((d_miss + d_obs) / n_all - 0.055) < 1e-12
p1, p2 = d_miss / n_miss, d_obs / (n_all - n_miss)
pp = (d_miss + d_obs) / n_all
z = (p1 - p2) / np.sqrt(pp * (1 - pp) * (1 / n_miss + 1 / (n_all - n_miss)))
print(f"two-proportion z for 9% vs 4%: {z:.1f}  (p={2*norm.sf(z):.1e})")
assert z > 15

rng = np.random.default_rng(4)
def sig(x): return 1 / (1 + np.exp(-x))
def fit(A, y, iters=25, ridge=1e-6):
    b = np.zeros(A.shape[1])
    for _ in range(iters):
        p = sig(A @ b); g = A.T @ (p - y); H = (A * (p * (1 - p))[:, None]).T @ A + ridge * np.eye(len(b))
        b -= np.linalg.solve(H, g)
    return b
def auc(y, s):
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)

def make(n, rng):
    inc = rng.normal(size=n)                          # standardised log-income
    other = rng.normal(size=n)
    lat = rng.normal(size=n)                          # unobserved stress that drives both default and hiding income
    default = rng.random(n) < sig(-3.4 - 0.5 * inc + 0.4 * other + 1.0 * lat)
    miss = rng.random(n) < sig(-1.3 + 1.2 * lat)      # riskier applicants more often leave income blank
    return inc, other, default.astype(float), miss
n = n_all
inc, oth, y, miss = make(n, rng)
print(f"simulated: missing share={miss.mean():.2%}, default rate missing={y[miss].mean():.2%} vs reported={y[~miss].mean():.2%}")
assert 0.25 < miss.mean() < 0.35 and y[miss].mean() > y[~miss].mean() * 1.5

tr = np.arange(n) < 35_000; te = ~tr
med = np.median(inc[tr & ~miss])                      # imputation statistic from the TRAIN fold only
filled = np.where(miss, med, inc)
def design(flag):
    cols = [np.ones(n), filled, oth] + ([miss.astype(float)] if flag else [])
    return np.c_[tuple(cols)]
res = {}
for flag in (False, True):
    A = design(flag); b = fit(A[tr], y[tr]); pr = sig(A[te] @ b)
    res[flag] = (auc(y[te], pr), pr)
    print(f"median fill{' + missing flag' if flag else '              '}: test AUC={res[flag][0]:.4f}")
assert res[True][0] > res[False][0] + 0.01

# Serving bug: the fill still happens but the missing flag is lost on the serving path (always 0)
A_flag = design(True); b = fit(A_flag[tr], y[tr])
bug = A_flag[te].copy(); m_te = miss[te]
bug[:, 3] = 0.0
p_ok = sig(A_flag[te] @ b); p_bug = sig(bug @ b)
print(f"rows with missing income: mean predicted default correct pipeline={p_ok[m_te].mean():.3f}, with lost flag={p_bug[m_te].mean():.3f}, actual={y[te][m_te].mean():.3f}")
print(f"AUC correct={auc(y[te], p_ok):.4f}, with bug={auc(y[te], p_bug):.4f}")
assert abs(p_ok[m_te].mean() - y[te][m_te].mean()) < 0.01 and p_bug[m_te].mean() < p_ok[m_te].mean() - 0.02
```

**Output (my run):**
```text
missing: 15000 rows, defaults 1350; reported: 35000 rows, defaults 1400; overall default rate 5.500%
two-proportion z for 9% vs 4%: 22.5  (p=7.6e-112)
simulated: missing share=26.90%, default rate missing=9.44% vs reported=4.09%
median fill              : test AUC=0.6244
median fill + missing flag: test AUC=0.6777
rows with missing income: mean predicted default correct pipeline=0.095, with lost flag=0.037, actual=0.094
AUC correct=0.6777, with bug=0.6214
```

**Follow-ups:**
- Would you drop the income column? No. It carries signal for the 70% who report it. Keep it plus the flag.
- What if the missing rate at serving drops to 5%? The model sees a different mix. Check that scores and approval rates still make sense, and retrain if needed.
- What about imputing with a model? Fine, but the flag still matters, because the imputed value cannot know why it was hidden.

**Common mistakes:** Median fill with no flag. Computing the median on all data before the split. Dropping missing rows. Different null handling in training and serving code. Ignoring the policy question.

### Q8 ⭐⭐⭐ 🟡 A model trained on 40,000 rows from 8,000 customers (five rows per customer on average) was split randomly by row, and offline AUC is 0.95. On entirely new customers the AUC is 0.78. Explain how you would confirm the cause, how you would re-split, and how you would report the honest number.
**Asked at:** Duplicate and leakage guides (a DEV Community post on a train-versus-test dedup gain vanishing, a Voxel51 near-duplicate glossary page, DataEval and Arize leakage pages); commonly reported as a leakage theme in public guides; search snippets only, not opened
**Say this first (1 line):** A random row split put the same customers on both sides, so 0.95 partly measures memorising customers; I would re-split by customer, compare, and report the group-split number with an interval as the honest one.

**Clarifying questions:**
- What will the model score in production: new customers, or existing customers with history? If existing, a row split may be closer to the truth, but still needs a time order.
- What identifies a "customer" (account, device, household)? Leakage also runs through devices and households.
- Do rows from one customer sit close in time? Then a time split also matters.
- Which features are stable per customer (demographics, region, tenure)? These let a model recognise a customer.
- How many customers are there in the final test set? The interval depends on customers, not rows.

**Approach:**
1. Confirm the cause with three quick checks. (a) How many test rows belong to a customer also in train? With 5 rows per customer and an 80/20 row split almost all of them do. (b) Re-run with a group split (all rows of a customer on one side). (c) Build a trivial "customer's other labels" predictor with no features, and see how well it scores.
2. Re-split: GroupKFold or StratifiedGroupKFold by customer for model selection (Book 1 Part 12 Q11, correct cross-validation when rows are grouped or time-ordered). Add a time order too when the model will predict the future (Q9).
3. Keep all preprocessing (encoders, target encodings, scalers) inside the training groups. Target encodings by customer are a classic leak (Book 1 Part 2 Q28).
4. Report the group-split score as the headline, with an interval from a customer-level bootstrap (resample customers, not rows).
5. Explain the gap: the old model used customer identity, which new customers do not have. If new-customer performance is the product need, tune and select on the group split, and consider the use-case split between new and returning customers.

**Metrics:**
- AUC on the group-split test set = P(random positive row scores above random negative row), customers disjoint from training.
- Share of test rows whose customer appears in training (should be 0% after the fix).
- 95% interval by resampling customers.
- Guardrails: number of test customers, positives per fold, per-fold spread.

**Risks:**
- The headline offline number is invalid for new customers.
- Hyper-parameters tuned on the leaky split select models that memorise.
- A bootstrap over rows understates the interval, because rows of one customer are correlated.
- Other group keys (household, device) still leaking.

**What the interviewer scores:**
- Strong: names the mechanism and runs a check before re-splitting. Weak: "the model is overfit".
- Strong: group split by the right key, preprocessing inside folds. Weak: "use more data".
- Strong: honest number with a customer-level interval. Weak: a single number.
- Strong: asks whether production sees new or known customers. Weak: assumes new.

**Example:** (illustrative simulation, my run) 39,905 rows from 8,000 customers (4.99 rows per customer). A random 80/20 row split leaves 98.2% of test rows with their customer also in train. A trivial predictor using only the same customer's other labels scores AUC 0.811 with no features. A 3-nearest-neighbour model scores AUC 0.668 on the row split and 0.571 on the customer-group split, a gap of 0.097. The honest number for new customers is 0.571, with a 95% customer-bootstrap interval of 0.555 to 0.588 on 1,600 test customers. The numbers differ from the prompt's 0.95 and 0.78, but the same mechanism produces the direction and the gap.
- Weak: "AUC dropped from 0.95 to 0.78, so the new customers are different."
- Strong: "98% of the test rows had a sibling row in train. I re-split by customer and report that number with an interval."

**Code:**
```python
# Q8 five rows per customer, random row split: same customers in train and test (illustrative simulation)
import numpy as np
from scipy.spatial import cKDTree
from scipy.stats import rankdata

rng = np.random.default_rng(8)
n_cust = 8_000
rows_per = 1 + rng.poisson(4, n_cust)                 # about five rows per customer
cust = np.repeat(np.arange(n_cust), rows_per)
n = len(cust)
print(f"rows={n}, customers={n_cust}, rows per customer={n/n_cust:.2f}")
assert abs(n / n_cust - 5) < 0.1

# Customer-level traits (stable across rows) and a customer-level outcome tendency; weak true row-level signal
d = 5
trait = rng.normal(size=(n_cust, d))
u = trait @ np.array([0.8, 0.6, 0.0, 0.0, 0.0]) + rng.normal(scale=2.0, size=n_cust)   # partly explained by traits
X = trait[cust] + rng.normal(scale=0.10, size=(n, d))                                  # rows of one customer look alike
rowfeat = rng.normal(size=n)
y = (rng.random(n) < 1 / (1 + np.exp(-(-0.5 + 1.0 * u[cust] + 0.3 * rowfeat)))).astype(int)
X = np.c_[X, rowfeat]

def auc(y, s):
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
def knn_scores(Xtr, ytr, Xte, k=3):
    idx = cKDTree(Xtr).query(Xte, k)[1]
    return ytr[idx].mean(axis=1)

# Confirm the cause: how many test rows have the same customer in train under a random row split?
perm = rng.permutation(n); cut = int(0.8 * n); tr, te = perm[:cut], perm[cut:]
seen = np.isin(cust[te], np.unique(cust[tr])).mean()
print(f"random row split: {seen:.1%} of test rows belong to a customer that is also in train")
assert seen > 0.9
a_row = auc(y[te], knn_scores(X[tr], y[tr], X[te]))

# Customer-only 'model': previous label average of the same customer (uses no features at all)
sums = np.bincount(cust[tr], weights=y[tr], minlength=n_cust); cnt = np.bincount(cust[tr], minlength=n_cust)
mean_y = y[tr].mean()
cust_score = (sums[cust[te]] + mean_y) / (cnt[cust[te]] + 1)
print(f"AUC of 'same customer's other labels' alone, row split: {auc(y[te], cust_score):.3f}")

# Group split: whole customers go to train or test
cperm = rng.permutation(n_cust); is_test_c = np.zeros(n_cust, bool); is_test_c[cperm[:int(0.2 * n_cust)]] = True
te_g = np.flatnonzero(is_test_c[cust]); tr_g = np.flatnonzero(~is_test_c[cust])
assert not set(cust[te_g]) & set(cust[tr_g])
a_grp = auc(y[te_g], knn_scores(X[tr_g], y[tr_g], X[te_g]))
print(f"kNN AUC: random row split={a_row:.3f}  customer-group split={a_grp:.3f}  gap={a_row-a_grp:.3f}")
assert a_row - a_grp > 0.08

# Honest number with an interval: bootstrap over test customers
sc = knn_scores(X[tr_g], y[tr_g], X[te_g]); cg = cust[te_g]; yg = y[te_g]
ucs = np.unique(cg); order = {c: np.flatnonzero(cg == c) for c in ucs}
boots = []
for _ in range(200):
    pick = rng.choice(ucs, len(ucs))
    ii = np.concatenate([order[c] for c in pick])
    boots.append(auc(yg[ii], sc[ii]))
lo, hi = np.percentile(boots, [2.5, 97.5])
print(f"honest AUC (new customers) = {a_grp:.3f}, 95% customer-bootstrap interval [{lo:.3f}, {hi:.3f}]; test customers={len(ucs)}")
assert lo < a_grp < hi
```

**Output (my run):**
```text
rows=39905, customers=8000, rows per customer=4.99
random row split: 98.2% of test rows belong to a customer that is also in train
AUC of 'same customer's other labels' alone, row split: 0.811
kNN AUC: random row split=0.668  customer-group split=0.571  gap=0.097
honest AUC (new customers) = 0.571, 95% customer-bootstrap interval [0.555, 0.588]; test customers=1600
```

**Follow-ups:**
- Is group split always right? Only if production scores new groups. For returning customers, use a time split instead: train on the past, test on the future.
- How would you split with both customer and time effects? Group the customers and keep the test period later than the train period.
- Can you still use per-customer history as a feature? Yes, if it is computed only from rows before the prediction time, and the evaluation includes customers with little history.

**Common mistakes:** Random row split with repeated entities. Bootstrap by row. Target encoding by customer on the full data. Tuning on the leaky split. Reporting only the leaky number "because it is bigger".

### Q9 ⭐⭐⭐ 🟡 A churn model scores AUC 0.88 under a random split of twelve months of data, but 0.74 when trained on months 1 to 9 and tested on months 10 to 12. The product manager says the random-split number is the more reliable one because it uses more data for testing. Explain which number to trust, why the two differ and how you would set up validation.
**Asked at:** Splitting and leakage guides (an arXiv paper on panel-data misuse of ML, a LetsDataScience 'science of data splitting' post, a Towards Data Science 'seven common causes of data leakage' article, an APXML recommender-splitting lesson); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Trust the time-split number, 0.74, because the model will be used on the future; a random split lets the model see the same months it is tested on, and more test rows do not fix that.

**Clarifying questions:**
- Is the model going to score future customers or months (almost always yes)? Then validation must mimic "train on the past, score the future".
- Was any feature built using information after the prediction date (for example 90-day activity measured at the end of the window)? That leak shows in both splits but is hidden more by the random one.
- Does the same customer appear in several months? Then a random split also leaks across rows (see Q8).
- Is churn defined with a lag (inactive for 60 days)? The last months of the window may not be fully labelled.
- Is there seasonality (festival months, quarter-end)? Months 10-12 may be unlike months 1-9 for known reasons.

**Approach:**
1. Say the principle. Validation should copy deployment. A random split shuffles the months, so the model is trained on months 10-12 and tested on months 10-12. In production it will have no such rows.
2. Explain why the two numbers differ. Relationships drift (the effect of price, tenure, promotions changes), and rows from the same period share unobserved conditions. A random split lets the model learn those. The time split charges the model for drift, which is the real cost.
3. Reject the PM's argument. Test-set size changes the noise of the estimate, not its bias. A random split with a 50% test set is just as optimistic (see Example).
4. Set up validation: a final time-based test (most recent matured months), rolling-origin folds (train 1..k, test k+1..k+3) for model selection and for the trend in AUC, and a gap between train end and test start if labels or features look ahead. See Book 1 Part 11 Q18 (preventing leakage when building training data for a time-dependent system).
5. Report the time-split AUC with an interval and the rolling-origin range, and note the drift: if AUC falls with distance, plan retraining cadence (Book 6 Part 2 Q37, retraining on the last four weeks).

**Metrics:**
- AUC on the later months = P(random churner scores above random non-churner), trained only on earlier months.
- Rolling-origin AUC per fold, plus its mean and spread.
- Decay: AUC by months since the end of training.
- Guardrails: label maturity of the last test month, number of churners per fold, calibration on the latest month.

**Risks:**
- A random split gives an optimistic number and a misplaced sense of safety.
- Final model chosen on the random split picks features that capture within-period quirks.
- A time split on a tiny test period is noisy; use rolling folds to see it.
- Seasonality: three months may not represent a full year.

**What the interviewer scores:**
- Strong: "validation must mimic deployment" and the drift explanation. Weak: "more test data is better".
- Strong: rolling-origin plus a final holdout, with a gap if needed. Weak: single time cut with no discussion.
- Strong: separates bias from variance in the PM's argument. Weak: agrees with the PM.
- Strong: connects the gap to retraining cadence. Weak: stops at the metric.

**Example:** (illustrative simulation, my run) 15 months of data, 6,000 customers per month, with two effects that drift (the first driver fades, the second grows). Random split of months 1-12 (25% test): AUC 0.813. Train on months 1-9, test on 10-12: 0.776. Then the real future: train on all 12 months and score months 13-15: AUC 0.770, which is close to the time-split number and far from the random one. Rolling-origin folds (train 1..k, test k+1..k+3, k = 6 to 9) give 0.797, 0.793, 0.785, 0.776, a downward drift. A random split with a 50% test set gives 0.814, so a bigger random test does not help. The prompt's 0.88 versus 0.74 has the same shape.
- Weak: "0.88 uses more test data, so it is more reliable."
- Strong: "0.74 is the honest number. In production the model never sees the months it scores. I would add rolling folds and report the decay."

**Code:**
```python
# Q9 random split vs time split on a drifting churn problem (illustrative simulation)
import numpy as np
from scipy.stats import rankdata

rng = np.random.default_rng(13)
def sig(x): return 1 / (1 + np.exp(-x))
def auc(y, s):
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
def fit(A, y, iters=25):
    b = np.zeros(A.shape[1])
    for _ in range(iters):
        p = sig(A @ b); g = A.T @ (p - y); H = (A * (p * (1 - p))[:, None]).T @ A + 1e-6 * np.eye(len(b))
        b -= np.linalg.solve(H, g)
    return b

per_month = 6_000
def month_data(m):
    """Month m = 1..15. The effect of each feature drifts slowly."""
    X = rng.normal(size=(per_month, 4))
    t = (m - 1) / 14
    coef = np.array([1.6 - 1.4 * t, 0.2 + 1.4 * t, 0.8, 0.0])        # driver 1 fades, driver 2 grows
    y = (rng.random(per_month) < sig(-1.6 + X @ coef)).astype(float)
    return np.full(per_month, m), X, y

parts = [month_data(m) for m in range(1, 16)]
M = np.concatenate([p[0] for p in parts]); X = np.vstack([p[1] for p in parts]); y = np.concatenate([p[2] for p in parts])
A = np.c_[np.ones(len(y)), X]

hist = M <= 12; future = M >= 13                                      # months 13-15 play the role of 'after launch'
Ah, yh, Mh = A[hist], y[hist], M[hist]

# (a) random split of the 12 months, 25% test
idx = rng.permutation(len(yh)); cut = int(0.75 * len(yh))
b_rand = fit(Ah[idx[:cut]], yh[idx[:cut]])
a_rand = auc(yh[idx[cut:]], Ah[idx[cut:]] @ b_rand)
# (b) time split: train months 1-9, test months 10-12
tr = Mh <= 9; te = Mh >= 10
b_time = fit(Ah[tr], yh[tr]); a_time = auc(yh[te], Ah[te] @ b_time)
print(f"random split AUC={a_rand:.3f}   time split (train 1-9, test 10-12) AUC={a_time:.3f}")
# (c) what really happens after launch: train on all 12 months, score months 13-15
b_all = fit(Ah, yh); a_fut = auc(y[future], A[future] @ b_all)
print(f"after launch (train 1-12, score months 13-15) AUC={a_fut:.3f}")
assert a_rand > a_time + 0.015
assert abs(a_fut - a_time) < abs(a_fut - a_rand)       # the time split predicts the future better than the random split

# (d) rolling-origin validation: train on months 1..k, test on k+1..k+3
rows = []
for k in (6, 7, 8, 9):
    t1 = Mh <= k; t2 = (Mh > k) & (Mh <= k + 3)
    rows.append(auc(yh[t2], Ah[t2] @ fit(Ah[t1], yh[t1])))
print("rolling-origin AUCs (train 1..k, test k+1..k+3, k=6..9):", " ".join(f"{a:.3f}" for a in rows), f" mean={np.mean(rows):.3f}")
assert max(rows) < a_rand
# test-set size is not the point: a bigger random test set stays optimistic
idx2 = rng.permutation(len(yh)); cut2 = int(0.5 * len(yh))
a_rand50 = auc(yh[idx2[cut2:]], Ah[idx2[cut2:]] @ fit(Ah[idx2[:cut2]], yh[idx2[:cut2]]))
print(f"random split with a 50% test set: AUC={a_rand50:.3f}")
assert a_rand50 > a_time + 0.015
```

**Output (my run):**
```text
random split AUC=0.813   time split (train 1-9, test 10-12) AUC=0.776
after launch (train 1-12, score months 13-15) AUC=0.770
rolling-origin AUCs (train 1..k, test k+1..k+3, k=6..9): 0.797 0.793 0.785 0.776  mean=0.788
random split with a 50% test set: AUC=0.814
```

**Follow-ups:**
- What if the time split is also lower because of seasonality? Check with the same calendar window last year, or add seasonal features, and say it explicitly.
- Do you ever use a random split? For a stable, non-time-dependent problem with no repeated entities, yes. Not for churn.
- How big a gap between train and test? At least as long as the label delay or the longest look-ahead window of any feature.

**Common mistakes:** Random split on time-ordered data. Thinking more test rows reduce bias. Final test period with immature labels. Tuning on the final test months. Forgetting the entity leak on top of the time leak.

### Q10 ⭐⭐⭐ 🟡 Chargebacks take up to 60 days to arrive, and in the table of the latest 60 days the confirmed-fraud rate is 0.3% while older, fully matured months settle near 1.0%. An engineer wants to retrain weekly on the most recent three months. Explain what this does to the labels, how you would build a training set and an evaluation window, and what you would do about the recent weeks.
**Asked at:** Delayed-label, positive-unlabelled and selection-bias literature (Bekker and Davis PU survey, an arXiv paper on PU survival data, an arXiv paper on PU data under selection bias); no interview page for the exact prompt, so editor-designed from the literature; search snippets only, not opened
**Say this first (1 line):** The recent weeks are not cleaner, they are just unlabelled yet; training on them as they stand teaches the model that many frauds are good, so I would train and evaluate only on matured transactions and treat the last 60 days with a maturity curve.

**Clarifying questions:**
- What is the delay distribution of chargebacks (how many arrive by day 15, 30, 45, 60)? That is the maturity curve and decides the cut-off.
- Are there faster signals (customer disputes, analyst confirmations, card blocks) that could label some recent frauds early? They can fill part of the gap, but they are a biased subset.
- Does the product need to react to new fraud patterns within weeks? If yes, recent data matters and we need a way to use it.
- Is the 1.0% rate stable over months? If the true rate moves, matured months lag reality.
- Are chargeback labels the only truth, or are some frauds never charged back? That is a permanent false-negative floor.

**Approach:**
1. Name the problem: delayed labels make recent negatives "not yet known", not "good". A "no chargeback yet" row is censored. In my run the last-90-day window hides 45% of its true frauds as "good".
2. Build the training set with a label cut-off: only transactions old enough that their label has matured (age of 60 days or more), or build each training snapshot "as of" its date, using only labels that were known then. See Book 1 Part 3 Q34 (labels arrive late: how does this affect training and evaluation, and how do you split the data).
3. Build the evaluation window the same way: a fully matured time window, strictly after the training window in transaction time, for example transactions aged 60 to 90 days. Keep a gap so no label that was learned in training leaks into evaluation.
4. For the last 60 days, do not use them as negatives. Options: monitor them with a maturity-adjusted rate (observed rate divided by the share of labels expected by that age), use fast proxy labels with caution, or give immature rows a lower weight or exclude them. Use the maturity curve for monitoring (Book 6 Part 2 Q4, labels that arrive 45 to 60 days after the transaction).
5. Retrain weekly if you wish, but weekly means "re-fit on the same matured rows plus the newly matured week", not "include the last three months as they stand". Check that new data arrives with the same feature definitions.

**Metrics:**
- Label maturity at age a = share of eventual fraud labels already seen for transactions aged a days (from the delay curve).
- Observed fraud rate by age band = confirmed frauds / transactions in the band.
- Maturity-adjusted rate = observed rate / average maturity of the rows.
- Share of true frauds hidden as "good" in the training window = (true frauds - labelled positives) / true frauds (only known in a simulation or from the delay curve).
- Guardrails: mean predicted probability versus observed rate on matured data, AUC on a matured test window.

**Risks:**
- Training on immature rows lowers predicted probabilities and fills the positive class with noisy negatives.
- Monitoring the recent rate as "improving fraud" (it is label delay).
- Fast proxy labels cover only certain fraud types, so using only them skews the training set.
- Matured-only training reacts to new fraud patterns about 60 days late.

**What the interviewer scores:**
- Strong: recognises censoring and quantifies the maturity curve. Weak: "recent data is more relevant, so use it".
- Strong: label cut-off for training and a matured, later evaluation window. Weak: random split of the latest three months.
- Strong: gives a plan for the recent weeks (adjusted monitoring, proxy labels). Weak: ignores them or drops them silently.
- Strong: notes the trade-off with reaction speed. Weak: no trade-off.

**Example:** (illustrative simulation, my run) Daily 2,000 transactions for 210 days, fraud labels arrive after a late-heavy delay of up to 60 days. True fraud rate is about 0.94%. Observed rate in the last 60 days is 0.271% (matured older rows: 0.943%). By age band the observed rate is 0.003% (0-15 days), 0.113% (15-30), 0.310% (30-45), 0.657% (45-60) and 0.983% (60-90). In the last-90-day window 1,666 are true frauds but only 915 are labelled, so 751 (45%) sit in the data as "good". The average maturity of the last-60-day rows is 0.29, so 0.271% / 0.29 gives a maturity-adjusted rate of 0.919%, close to 0.943%. Model A trained on the last 90 days as labelled predicts a mean of 0.0051 against an observed 0.0095 on a matured test window (AUC 0.815). Model B trained on matured rows aged 60-150 days predicts 0.0095 (AUC 0.816). So the ranking is similar here, but the probabilities from A are about half of the truth, which breaks thresholds and expected-loss use.
- Weak: "Retrain weekly on the last three months, as the data is fresher."
- Strong: "The last 60 days are censored, so I train on matured rows, evaluate on a later matured window, and monitor the recent weeks with a maturity-adjusted rate."

**Code:**
```python
# Q10 chargebacks arrive up to 60 days late: recent weeks look cleaner than they are (illustrative simulation)
import numpy as np
from scipy.stats import rankdata

rng = np.random.default_rng(10)
def sig(x): return 1 / (1 + np.exp(-x))
def auc(y, s):
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
def fit(A, y, iters=25):
    b = np.zeros(A.shape[1])
    for _ in range(iters):
        p = sig(A @ b); g = A.T @ (p - y); H = (A * (p * (1 - p))[:, None]).T @ A + 1e-6 * np.eye(len(b))
        b -= np.linalg.solve(H, g)
    return b

DAYS, PER_DAY, MAXD = 210, 2_000, 60
day = np.repeat(np.arange(DAYS), PER_DAY); n = len(day)            # day 0 oldest, day 209 = today
X = rng.normal(size=(n, 3))
true_fraud = rng.random(n) < sig(-5.45 + X @ np.array([1.0, 0.7, 0.4]))
true_fraud = true_fraud.astype(int)
# Chargeback delay in days: confirmed fraud shows up by age a with probability (a/60)^2.3 for a <= 60 (late-heavy, invented)
delay = MAXD * rng.random(n) ** (1 / 2.3)
age = DAYS - 1 - day
label_seen = (true_fraud == 1) & (delay <= age)                     # fraud confirmed so far
y_obs = label_seen.astype(int)

recent = age < 60; older = age >= 60
print(f"true fraud rate, last 60 days={true_fraud[recent].mean():.3%}; older={true_fraud[older].mean():.3%}")
print(f"observed rate:  last 60 days={y_obs[recent].mean():.3%}; older (fully matured)={y_obs[older].mean():.3%}")
assert abs(y_obs[older].mean() - true_fraud[older].mean()) < 1e-12     # nothing is pending after 60 days
assert 0.0024 < y_obs[recent].mean() < 0.0036 and 0.009 < y_obs[older].mean() < 0.0112

# Labelled-as-clean frauds inside a 'last three months' training window
win = age < 90
missed = (true_fraud[win] == 1) & (y_obs[win] == 0)
print(f"last-90-day window: true frauds={true_fraud[win].sum()}, labelled positive={y_obs[win].sum()}, hidden as 'good'={missed.sum()} ({missed.sum()/true_fraud[win].sum():.0%} of frauds)")
assert missed.sum() / true_fraud[win].sum() > 0.4

# Maturity curve by age band and a maturity-adjusted estimate of the recent rate
bands = [(0, 15), (15, 30), (30, 45), (45, 60), (60, 90)]
print("age band (days) | observed rate | share of final labels seen")
for lo, hi in bands:
    m = (age >= lo) & (age < hi)
    print(f"  {lo:2d}-{hi:2d}          | {y_obs[m].mean():.3%}        | {min(y_obs[m].mean() / true_fraud[older].mean(), 1):.0%}")
mat = np.clip((age[recent] / MAXD) ** 2.3, 0, 1).mean()             # average share of labels already in for the last 60 days
adj = y_obs[recent].mean() / mat
print(f"average maturity of last-60-day rows={mat:.2f}; maturity-adjusted rate={adj:.3%} (vs matured {y_obs[older].mean():.3%})")
assert abs(adj - y_obs[older].mean()) < 0.0015

# Train two models: (A) last 90 days as labelled today, (B) only rows aged 60-150 days (fully matured)
A = np.c_[np.ones(n), X]
old_win = (age >= 60) & (age < 150)
test = (age >= 150)                                                  # older, fully matured, evaluation window
bA = fit(A[win], y_obs[win]); bB = fit(A[old_win], y_obs[old_win])
for name, b in (("A: last 90 days, labels as they are", bA), ("B: matured rows aged 60-150 days   ", bB)):
    p = sig(A[test] @ b)
    print(f"{name}: matured-test AUC={auc(y_obs[test], p):.3f}; mean predicted={p.mean():.4f} vs observed {y_obs[test].mean():.4f}")
pA = sig(A[test] @ bA); pB = sig(A[test] @ bB)
assert pA.mean() < 0.6 * y_obs[test].mean() and abs(pB.mean() - y_obs[test].mean()) < 0.002
```

**Output (my run):**
```text
true fraud rate, last 60 days=0.897%; older=0.943%
observed rate:  last 60 days=0.271%; older (fully matured)=0.943%
last-90-day window: true frauds=1666, labelled positive=915, hidden as 'good'=751 (45% of frauds)
age band (days) | observed rate | share of final labels seen
   0-15          | 0.003%        | 0%
  15-30          | 0.113%        | 12%
  30-45          | 0.310%        | 33%
  45-60          | 0.657%        | 70%
  60-90          | 0.983%        | 100%
average maturity of last-60-day rows=0.29; maturity-adjusted rate=0.919% (vs matured 0.943%)
A: last 90 days, labels as they are: matured-test AUC=0.815; mean predicted=0.0051 vs observed 0.0095
B: matured rows aged 60-150 days   : matured-test AUC=0.816; mean predicted=0.0095 vs observed 0.0095
```

**Follow-ups:**
- How do you react to a new fraud pattern faster? Use fast proxy labels (disputes, analyst reviews) as extra signals and as a separate fast model or rules layer, and keep the matured model as the calibrated base.
- Can you use the immature rows at all? Yes, as unlabelled data (positive-unlabelled style), with a lower weight, or as features for drift monitoring. Not as clean negatives.
- Does a PU method help? It can, if you know the label delay curve. Treat it as a second step, after the cut-off fix (Book 1 Part 3 Q46, positive-unlabeled learning).

**Common mistakes:** Treating "no chargeback yet" as good. Evaluating on the latest weeks. Reading a falling recent fraud rate as a real improvement. Retraining on immature rows and then using the probabilities for decisions. Not leaving a gap between training and evaluation windows.

### Q11 ⭐⭐⭐ 🟡 In a payments table, 0.2% of rows have an amount above 1,000,000 rupees while the median amount is 800 rupees. Some of these are genuine corporate payments and some are entry errors with extra zeros. Explain how you would tell outliers from errors, what you would do with each group and whether you would clip, drop or keep them.
**Asked at:** Data-cleaning question banks (an Educative data-science interview data-cleaning lesson, a TechPrep '82 Data Cleaning Interview Questions' page, StrataScratch 'data cleaning traps', a DataCamp cleaning checklist) covering outliers versus errors and unit mismatches; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** I do not treat "big" as "wrong": I test each large amount against independent evidence (the customer's own history, the settlement ledger, the merchant type), fix or flag the ones that fail, and keep the genuine ones as real data with a flag, because clipping would erase the very corporate payments the business cares about.

**Clarifying questions:**
- Is there a second source of the amount (bank settlement ledger, invoice, card network record)? Why: an independent amount is the cleanest way to prove an entry error.
- Who makes these payments: retail users, corporates, or both, and do corporates have a customer type flag? Why: a 12 lakh payment is normal for one segment and absurd for another.
- What is the model or report for (fraud scoring, spend forecasting, a revenue number)? Why: the cost of keeping or dropping a row depends on the use.
- Does entry validation exist at the source (maximum per channel, confirmation screen)? Why: it decides whether this is a fix-once problem or a recurring one.
- How many rows are in question (here 0.2%, about 200 per 100,000) and can a person review them? Why: a few hundred rows can go to a review queue; a million cannot.

**Approach:**
1. Say what the numbers mean: median 800 rupees and 0.2% of rows above 1,000,000 means the tail is about 1,250 times the median. That alone proves nothing. A genuine corporate payment and an extra-zero typo both sit there.
2. Look for independent evidence per row, in this order: (a) ledger or settled amount disagrees with the recorded amount, (b) amount divided by the customer's own largest earlier payment (a retail customer who always paid under 20,000 and now "pays" 3,000,000 is suspicious, a corporate with earlier 4,000,000 payments is not), (c) the amount is 10, 100 or 1,000 times a plausible price for that merchant or item, (d) channel limits (a UPI-style limit would make some values impossible, check the current limit with the owner).
3. Put each large row in one of three groups: error (evidence says so), genuine (history fits), unknown (no history, no ledger). Unknown goes to a short review queue.
4. Treat each group differently. Errors: repair if the true value is recoverable (ledger value), otherwise set to missing and flag. Genuine: keep unchanged, add an `is_large_corporate` style flag so a model or report can handle them on purpose. Unknown: hold out of training until reviewed; do not guess.
5. Only after that choose a statistical treatment for what is left. For a mean-based report use the repaired data, for a linear model use a log transform or a robust loss, for trees leave the rows alone. Clip (winsorise) only as a documented modelling choice, never as a substitute for finding the errors.
6. Fix the source: add a validation rule (a confirmation step above a limit) and a monthly count of extreme values per channel.

**Metrics:**
- Error rate among large rows = rows confirmed as entry errors / rows above 1,000,000. Here 120 / 200 in the simulation below.
- Auto-rule precision = correctly auto-flagged errors / all auto-flagged rows. Recall = auto-flagged errors / all errors.
- Review-queue size = rows with no evidence either way. Keep it small enough for a person to clear.
- Effect on the headline number: mean amount before and after repair.
- Guardrail: genuine large payments must not be altered (count of genuine rows changed should be 0).

**Risks:**
- Clipping all rows above a percentile changes genuine corporate payments to a fake smaller value, and the corporate segment looks smaller than it is.
- Dropping all large rows biases the sample against corporates, so the model never learns that segment.
- An automatic rule that uses the same field that has the error (for example the amount itself) is circular.
- "Extra zeros" errors can also land below any threshold (a typed 8,000 instead of 800), so a big-value filter finds only some errors. Check the ratio to history at all sizes.
- Fixing values by dividing by 1,000 without proof makes up data. Use the ledger value or set to missing.

**What the interviewer scores:**
- Strong: separates "outlier" (real but extreme) from "error" (recorded wrong) and asks for independent evidence per row.
- Strong: three groups (error, genuine, unknown) with a different action for each, and a review queue instead of a guess.
- Strong: says clip, drop or keep is a modelling decision made after the errors are removed, and names the cost of each.
- Weak: "remove anything beyond 3 standard deviations" or "clip at the 99th percentile" with no check against evidence.
- Weak: no plan to fix the source of the errors.
- Cross-reference: Book 1 Part 2 covers the theory in "How do outliers affect linear regression and what robust options exist (winsorizing, Huber, quantile regression)?". This question is about proving which rows are errors first.

**Example:** (illustrative numbers) 100,000 rows, 200 above 1,000,000. Of these, 80 are genuine corporate payments (customers with earlier payments of 1 to 6 million) and 120 are retail customers whose amount is a real amount times 1,000 (the ledger shows the right figure). Evidence rule: ledger mismatch, or amount at least 100 times the customer's earlier maximum, so 120 rows are auto-flagged as errors and all 120 are real errors; 70 genuine rows pass the history check; 10 genuine first-time corporate rows have no history, so they go to review. Effect on the mean amount: 7,587 before repair, 3,900 after, almost double. Clipping at the 99.9th percentile (2,971,627) leaves a mean of 6,349 (still inflated, because the errors stay in the data, only some of them capped) and truncates the largest genuine payment from 7,034,373 to 2,971,627. Weak answer: "clip at the 99.9th percentile." Strong answer: "I prove the errors first with the ledger and customer history, fix those, keep the genuine large payments with a flag, and only then decide on a transform."

**Code:**
```python
# Q11: outliers vs entry errors in a payments table (illustrative numbers)
import numpy as np
rng = np.random.default_rng(11)
N = 100_000
# 99,800 ordinary retail rows, median about 800 rupees
retail = rng.lognormal(np.log(800), 1.0, 99_800)
# 80 genuine corporate payments (customers with a history of large payments)
corp_prior_max = rng.uniform(1.0e6, 6.0e6, 80)
corp_amt = corp_prior_max * rng.uniform(0.5, 1.5, 80)
corp_amt = np.maximum(corp_amt, 1.05e6)
# 120 entry errors: a retail amount typed with three extra zeros
true_small = rng.uniform(1_100, 5_000, 120)
err_amt = true_small * 1000
err_prior_max = rng.uniform(2_000, 20_000, 120)       # retail customers' own history
# the 10 corporate rows below are first-time large payers: no history to compare with
new_big = rng.choice(80, 10, replace=False)
corp_prior_max[new_big] = 0

amount = np.concatenate([retail, corp_amt, err_amt])
prior_max = np.concatenate([np.full(99_800, 5_000.0), corp_prior_max, err_prior_max])
is_error = np.concatenate([np.zeros(99_800 + 80, bool), np.ones(120, bool)])
settled = np.where(is_error & (np.arange(N) >= 99_880), amount / 1000, amount)  # bank ledger amount

big = amount > 1_000_000
print("rows > 1,000,000:", big.sum(), "share:", f"{big.mean():.3%}", " median:", round(float(np.median(amount))))
assert big.sum() == 200 and abs(np.median(amount) - 800) < 20

# Evidence 1: ledger mismatch.  Evidence 2: amount versus the customer's own largest earlier payment.
mismatch = big & (np.abs(settled - amount) / amount > 0.5)
ratio = np.where(prior_max > 0, amount / np.maximum(prior_max, 1), np.inf)
history_ok = big & (ratio <= 3)                      # in line with own history
auto_error = mismatch | (big & (prior_max > 0) & (ratio >= 100))       # far above own history, or ledger disagrees
review = big & ~auto_error & (prior_max == 0)        # no history and no mismatch: a human looks
keep = big & ~auto_error & ~review
print(f"auto-error {auto_error.sum()}  keep {keep.sum()}  review queue {review.sum()}")
tp = (auto_error & is_error).sum(); fp = (auto_error & ~is_error).sum()
print(f"auto-error rule: caught {tp} of {is_error.sum()} errors, wrongly flagged {fp} genuine")
assert auto_error.sum() == 120 and tp == 120 and fp == 0 and review.sum() == 10 and keep.sum() == 70

# Repair the errors: divide by 1000 (the ledger value) and keep a flag column
fixed = np.where(auto_error, settled, amount)
def mean_log(a): return float(np.mean(np.log1p(a)))
cap = np.quantile(amount, 0.999)
clipped = np.minimum(amount, cap)
print(f"mean amount: raw {amount.mean():,.0f}  fixed {fixed.mean():,.0f}  clipped at p99.9 ({cap:,.0f}) {clipped.mean():,.0f}")
print(f"genuine corporate rows after clip: largest {clipped[~is_error & big].max():,.0f} vs real {amount[~is_error & big].max():,.0f}")
assert 1.9 < amount.mean() / fixed.mean() < 2.0
assert clipped[~is_error & big].max() < amount[~is_error & big].max()
print("log-scale mean: raw", round(mean_log(amount), 3), "fixed", round(mean_log(fixed), 3))
```

**Output (my run):**
```text
rows > 1,000,000: 200 share: 0.200%  median: 801
auto-error 120  keep 70  review queue 10
auto-error rule: caught 120 of 120 errors, wrongly flagged 0 genuine
mean amount: raw 7,587  fixed 3,900  clipped at p99.9 (2,971,627) 6,349
genuine corporate rows after clip: largest 2,971,627 vs real 7,034,373
log-scale mean: raw 6.703 fixed 6.695
```

**Follow-ups:**
- Evidence is missing for most rows, what then? Use the ratio to the customer's own history and merchant norms to score "likely error", send the top of the list to review, and use a robust method (log scale, Huber loss, trees) for the rest. Say clearly that this is a risk judgement, not proof.
- Would you ever clip? Yes, as a model-side step after cleaning, for a method that is sensitive to extremes (a linear model on raw amounts), documented and tested by comparing validation error with and without it.

**Common mistakes:** Using a standard-deviation or percentile rule as proof of error. Treating all extreme rows the same way. Dropping rows silently. Fixing values by guessing the number of zeros. Cleaning once and not fixing the source.

### Q12 ⭐⭐⭐ 🟡 A new partner feed covers 90,000 of 500,000 rows (18%) and reports distance in miles while the rest of the table is in kilometres, and nobody noticed until the delivery-time model's error rose. Explain how you would find the affected rows, how you would repair the data and the model, and which checks would catch this next time.
**Asked at:** Data-cleaning question banks (an Educative data-science interview data-cleaning lesson, a TechPrep '82 Data Cleaning Interview Questions' page, StrataScratch 'data cleaning traps', a DataCamp cleaning checklist) covering outliers versus errors and unit mismatches; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** I find the affected rows by comparing the reported distance with an independent distance (coordinates) per source, convert miles to kilometres only for the proven rows, retrain on the repaired table, and add a per-source unit check so the next feed cannot slip through.

**Clarifying questions:**
- Is there a source or feed column, and when did the partner feed start? Why: if yes, the affected rows are a filter, not a guess; the start date also says which past training data is contaminated.
- Do we have coordinates (pickup and drop) or another distance that does not depend on the partner? Why: an independent measure is how I prove the unit.
- Does the partner feed also differ in other fields (weight, time zone, currency)? Why: a unit bug is rarely alone.
- Did anyone retrain on the mixed table, and is the model already live? Why: it decides between a data fix only and a retrain plus rollback.
- Can the partner confirm the unit in writing (a data contract)? Why: I fix the data on evidence, and the confirmation closes the case.

**Approach:**
1. Size it. 90,000 of 500,000 rows is 18%. Cut the model error by source and by date: if the error rise starts when the feed starts and sits in the partner rows, the unit is the first suspect.
2. Prove it with a ratio. For every row compute reported distance divided by a reference distance (straight-line from coordinates, which does not depend on the feed). Take the median per source. For kilometres the median ratio sits near some stable value (here 1.30, the road detour); for miles it sits at 0.621 times that. A ratio between sources close to 0.6214 (1 mile = 1.609344 km) is the signature.
3. Find the rows. If a feed column exists, filter on it. If not, use a row screen on the ratio plus the date the shift started, then check the screened set against the partner's id list.
4. Repair data: multiply the partner distances by 1.609344, store both `distance_raw` and `distance_km`, record the source unit as a column, and re-run the ratio check. The KS distance between partner and other distance distributions should fall to near zero.
5. Repair the model: retrain on the fixed table and compare on a holdout split by source (partner rows and other rows). Do not just compare overall error.
6. Look back: which retrains, reports and promises used the broken field? If the model is live and the error is large, roll back to the last model trained before the feed and then redeploy the retrained one.
7. Prevent: a data contract with unit names, an automated per-source unit check (median ratio against a band of 0.85 to 1.15), and a volume and distribution check on every new feed before it is joined.

**Metrics:**
- Share affected = partner rows / all rows = 90,000 / 500,000 = 18%.
- Unit ratio for a source = median(reported / reference distance) for that source, divided by the same median for trusted sources. Alert when outside 0.85 to 1.15.
- MAE (minutes) = mean of |actual minus predicted delivery time|, reported overall and by source.
- Guardrails: the kilometre rows must not change (rows modified outside the partner set = 0); the repaired distributions match (KS statistic near 0).

**Risks:**
- Converting by a filter on distance size (say, "everything below 3") also converts genuine short trips.
- Partner feeds can change units later (a silent switch back), so a one-time fix is not enough.
- A global model with mixed units still looks fine overall: the other 82% of rows hide the damage. Always cut by source.
- Rounding: partner distances may be rounded to 0.1 mile (0.16 km), which loses precision; note this limit.
- Refitting before the repair would teach the model the partner's rows are "short trips that take long".

**What the interviewer scores:**
- Strong: uses an independent reference to prove the unit, not just a hunch, and slices the error by source.
- Strong: repairs data first, then model, and says what evidence shows the repair worked.
- Strong: puts the prevention at the contract and the pipeline (per-source check, unit column).
- Weak: retrain and hope, or a manual one-off conversion with no check.
- Weak: cannot say how to detect affected rows when there is no feed column.
- Cross-reference: Book 6 Part 2 has a production-side version, "An upstream team renamed a column and changed its type, and a default of 0 is now silently filled in where the model expects order_value in rupees". Here the object is the data table.

**Example:** (illustrative numbers) 500,000 rows, 90,000 from the partner (18%). In the simulation the partner median ratio reported/straight-line is 0.808 and the others' is 1.300; 0.808 / 1.300 = 0.621, which is 1 mile in km (0.6214). Partner distances after dividing by 0.621371 match the others (KS 0.311 before, 0.005 after). A line fitted for delivery minutes on the broken table has MAE 8.76 on partner rows versus 3.18 after the fix, and the overall MAE falls from 4.46 to 3.20. Weak answer: "Retrain with more data." Strong answer: "I prove the unit with the coordinate ratio, convert only the partner rows, check the two distributions match, and add a unit check per feed."

**Code:**
```python
# Q12: partner feed in miles inside a kilometre table (illustrative numbers)
import numpy as np
from scipy import stats
rng = np.random.default_rng(12)
N, NP = 500_000, 90_000
MI = 0.621371
km = rng.lognormal(np.log(5.0), 0.6, N)
partner = np.zeros(N, bool); partner[rng.choice(N, NP, replace=False)] = True
print("partner share:", f"{partner.mean():.0%}"); assert partner.sum() == NP and partner.mean() == 0.18
straight = km / rng.uniform(1.15, 1.45, N)            # straight-line distance from coordinates
reported = np.where(partner, km * MI, km)             # what the table says
minutes = 8 + 4.5 * km + rng.normal(0, 4, N)          # delivery time truth

# Step 1: find affected rows: ratio of reported distance to coordinate distance, by source
ratio = reported / straight
r_p, r_o = np.median(ratio[partner]), np.median(ratio[~partner])
print(f"median reported/straight: partner {r_p:.3f}  others {r_o:.3f}  ratio {r_p / r_o:.3f}")
assert abs(r_p / r_o - MI) < 0.01
# a row-level screen with no feed label: ratio below 0.95 flags most miles rows
flag = ratio < 1.0
print(f"row screen (ratio<1.0): catches {(flag & partner).sum() / NP:.1%} of partner rows, false alarms {(flag & ~partner).sum() / (~partner).sum():.1%} of others")

# Step 2: repair the data and verify the repair
fixed = np.where(partner, reported / MI, reported)
ks = stats.ks_2samp(fixed[partner], fixed[~partner]).statistic
ks_raw = stats.ks_2samp(reported[partner], reported[~partner]).statistic
print(f"KS partner vs others: raw {ks_raw:.3f}  after fix {ks:.3f}")
assert ks_raw > 0.3 and ks < 0.02

# Step 3: repair the model: fit a line on the broken table versus the fixed table
idx = rng.permutation(N); tr, te = idx[:400_000], idx[400_000:]
def fit(d): return np.linalg.lstsq(np.c_[np.ones(len(tr)), d[tr]], minutes[tr], rcond=None)[0]
def mae(d, w, m): return float(np.mean(np.abs(minutes[m] - (w[0] + w[1] * d[m]))))
tep = te[partner[te]]; teo = te[~partner[te]]
w_bad, w_ok = fit(reported), fit(fixed)
print(f"MAE minutes on partner rows: trained on broken {mae(reported, w_bad, tep):.2f} | fixed data {mae(fixed, w_ok, tep):.2f}")
print(f"MAE minutes on other rows:   trained on broken {mae(reported, w_bad, teo):.2f} | fixed data {mae(fixed, w_ok, teo):.2f}")
print(f"MAE overall (test):          broken {mae(reported, w_bad, te):.2f} | fixed {mae(fixed, w_ok, te):.2f}")
assert mae(fixed, w_ok, tep) < mae(reported, w_bad, tep)
print("slope per km: broken", round(w_bad[1], 2), "fixed", round(w_ok[1], 2)); assert abs(w_ok[1] - 4.5) < 0.1

# Step 4: the check that would have caught it: daily per-source median ratio against a band
def unit_check(r, src_mask, band=(0.85, 1.15), ref=None):
    m = np.median(r[src_mask]) / ref
    return round(float(m), 3), bool(not (band[0] <= m <= band[1]))
print("check partner :", unit_check(ratio, partner, ref=r_o))
print("check others  :", unit_check(ratio, ~partner, ref=r_o))
assert unit_check(ratio, partner, ref=r_o)[1] and not unit_check(ratio, ~partner, ref=r_o)[1]
```

**Output (my run):**
```text
partner share: 18%
median reported/straight: partner 0.808  others 1.300  ratio 0.621
row screen (ratio<1.0): catches 100.0% of partner rows, false alarms 0.0% of others
KS partner vs others: raw 0.311  after fix 0.005
MAE minutes on partner rows: trained on broken 8.76 | fixed data 3.18
MAE minutes on other rows:   trained on broken 3.52 | fixed data 3.20
MAE overall (test):          broken 4.46 | fixed 3.20
slope per km: broken 4.47 fixed 4.5
check partner : (0.621, True)
check others  : (1.0, False)
```

The row screen separates the sources perfectly here because the simulated detour factor is bounded between 1.15 and 1.45; real data overlaps more, so use the screen to build a candidate list, not as final proof.

**Follow-ups:**
- The partner will not confirm the unit. Use the independent ratio and a sample of trips with known real distances (a few hundred checked on a map); a consistent 0.62 ratio is strong evidence, and I would still record the assumption.
- The model must stay live while the data is fixed. Add the unit conversion in the serving feature step using the source id, so partner rows are converted at request time too, and confirm that online and offline distance distributions match.

**Common mistakes:** Judging by overall error only. Converting without a proof step. Repairing the data but not the stored features and past training sets. Ignoring serving-time conversion. No automated check afterwards.

### Q13 ⭐⭐⭐ 🔴 You trained a fraud model after keeping all 10,000 fraud rows and a random 10% of the 990,000 legitimate rows (99,000 rows, so 109,000 in all and a training fraud share of about 9.2%). A transaction gets a score of 0.50, and finance wants to use the scores as true probabilities for expected-loss calculations. Explain what the 0.50 means, how you would correct it to the 1% base rate, and how you would check the result.
**Asked at:** Imbalanced-data and fraud-evaluation guides (techinterview.org 'Handling Imbalanced Datasets in Machine Learning', Dataford fraud-evaluation prompts such as 'how do you evaluate a fraud detection model on imbalanced data', a KDnuggets piece on SMOTE misuse, a Coresignal 'class imbalance interview trap' post); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** A 0.50 from a model trained on a 10%-sampled legit set is a score on the sampled mix, so at the true 1% base rate it means about 9.1%, using p = 0.1 x 0.5 / (0.1 x 0.5 + 0.5); I check it with a calibration table on a full-population sample.

**Clarifying questions:**
- Was the 10% of legitimate rows a uniform random sample, and was it drawn before any other filtering? Why: the correction assumes sampling depends on the label only.
- Is the 1% base rate the current rate in the traffic the model will score (and by segment)? Why: the correction uses the true prior, and a drifting prior moves the answer.
- What will finance do with the number (expected loss, reserve, a threshold)? Why: it sets how accurate the probabilities must be.
- Do I have a recent, full-rate (not undersampled) validation set with matured labels? Why: that is the only honest place to check calibration.
- Any class weights on top of the sampling? Why: weights and sampling both shift the scores and must not be corrected twice.

**Approach:**
1. Do the arithmetic from the prompt: 10,000 fraud + 10% x 990,000 legit (that is 99,000) gives a training set of 109,000 rows and fraud is 10,000 / 109,000 = 9.17%. The true base rate is 10,000 / 1,000,000 = 1%.
2. Say what 0.50 means: on a training-like mix (9.2% fraud), a transaction with score 0.50 has equal odds of fraud and legit (odds 1.0). The sampling kept all fraud but only a tenth of legit, so legit is under-represented ten-fold.
3. Correct the odds. Sampling rate for legit beta = 0.1. Corrected odds = beta x raw odds = 0.1 x 1 = 0.1, so corrected probability = 0.1 / 1.1 = 0.0909. As a formula: p = beta p_s / (beta p_s + (1 - p_s)). Equivalent: subtract ln(1/beta) = 2.303 from the logit.
4. Check it. Score a full-rate validation sample, bin by corrected score, and compare mean predicted versus actual fraud rate per bin (a reliability table), plus the mean of corrected scores versus the base rate. If still off, fit a small calibration step (Platt or isotonic) on the full-rate validation data, never on the undersampled data.
5. Tell finance about limits: bins with few frauds are noisy, and the correction fixes the prior shift only, not a model that is bad in other ways.
6. Decide the threshold on the corrected scale (so "block above 5% fraud probability" means what it says).
7. Cross-reference: Book 1 Part 3 asks "Does class weighting, SMOTE or undersampling break probability calibration? How do you correct p...". This question applies it with checkable numbers.

**Metrics:**
- Training fraud share = fraud rows / training rows = 10,000 / 109,000 = 9.17%.
- Corrected probability p = beta p_s / (beta p_s + 1 - p_s), beta = legit sampling rate = 0.1.
- Calibration check: per band, mean corrected score and actual fraud rate (fraud rows / rows) on full-rate data; overall, mean corrected score versus base rate.
- Brier score or log-loss on the full-rate validation set, before and after correction.
- Guardrail: ranking metrics (AUC, PR-AUC) do not change with the correction because it is a monotone transform; if they change, something else is wrong.

**Risks:**
- Correcting twice (class weights and the formula) or not at all.
- Using the correction with the wrong beta (for example 0.01 instead of 0.1) turns a calibration fix into a new error.
- A tree ensemble may not be well calibrated even before sampling, so the formula alone may leave residual bias; check the table.
- The base rate shifts by segment and over time; a single prior is a simplification.
- Using the undersampled validation set to judge calibration will always look fine and tell you nothing.

**What the interviewer scores:**
- Strong: gets 109,000 and 9.17% right, explains the odds shift in one sentence, and gives 0.0909.
- Strong: validates on a full-rate sample with a reliability table instead of trusting the formula.
- Strong: knows ranking metrics do not change and that the threshold must be set on the corrected scale.
- Weak: "just use the score as it is" or "apply SMOTE-style rebalancing to fix it".
- Weak: corrects with the wrong direction (raising instead of lowering).

**Example:** (illustrative numbers) 10,000 fraud and 990,000 legit; keep all fraud and 10% of legit. Raw score 0.50 maps to 0.0909. In the simulation below (one feature, true model known, 1.005% fraud) the mean raw score on the full population is 6.309%, far above 1%, while the mean corrected score is 1.004%. For raw scores near 0.50 the corrected value is 0.090 and the actual fraud rate is 0.087. Weak answer: "A score of 0.50 means 50% fraud." Strong answer: "0.50 is the odds on the sampled mix; at the true prior the odds are ten times smaller, about 9%, and I confirm that on full-rate data."

**Code:**
```python
# Q13: undersampling and probability correction (illustrative numbers)
import numpy as np
rng = np.random.default_rng(13)
# arithmetic from the prompt
fraud, legit, beta = 10_000, 990_000, 0.10
kept = fraud + beta * legit
print(f"training rows {kept:,.0f}, training fraud share {fraud / kept:.2%}, true base rate {fraud / (fraud + legit):.2%}")
assert kept == 109_000 and round(fraud / kept, 3) == 0.092
def correct(ps, beta): return beta * ps / (beta * ps + (1 - ps))
p = correct(0.50, beta); print("score 0.50 ->", round(p, 4)); assert round(p, 4) == 0.0909
print("odds view: 0.50 is odds 1.0; times beta 0.1 gives odds 0.1; prob", round(0.1 / 1.1, 4))
# base-rate shift check: mean raw score level versus the 1% truth

# simulation: one feature, true model known, population with a 1% fraud rate
def sig(z): return 1 / (1 + np.exp(-z))
n = 1_000_000
x = rng.normal(size=n)
lo, hi = -10.0, 0.0
for _ in range(60):
    mid = (lo + hi) / 2
    if sig(mid + 2 * x).mean() > 0.01: hi = mid
    else: lo = mid
b0 = (lo + hi) / 2
y = rng.random(n) < sig(b0 + 2 * x)
print("simulated population fraud rate:", f"{y.mean():.3%}")
keep = y | (rng.random(n) < beta)
xs, ys = x[keep], y[keep].astype(float)
print("training rows:", keep.sum(), " fraud share:", f"{ys.mean():.2%}")
w = np.zeros(2); X = np.c_[np.ones(len(xs)), xs]
for _ in range(25):                                    # Newton / IRLS
    pr = sig(X @ w); g = X.T @ (ys - pr); H = (X * (pr * (1 - pr))[:, None]).T @ X
    w += np.linalg.solve(H, g)
print("fitted intercept", round(w[0], 3), " true intercept", round(b0, 3), " shift", round(w[0] - b0, 3), " ln(1/beta)=", round(np.log(1 / beta), 3))
assert abs((w[0] - b0) - np.log(1 / beta)) < 0.25 and abs(w[1] - 2) < 0.2
raw = sig(w[0] + w[1] * x); cor = correct(raw, beta)
print(f"mean score on the full population: raw {raw.mean():.3%}  corrected {cor.mean():.3%}  truth {y.mean():.3%}")
assert raw.mean() > 0.05 and abs(cor.mean() - y.mean()) < 0.0015
# calibration by raw-score band, full population
edges = [0, 0.1, 0.3, 0.5, 0.7, 0.9, 1.0]
print("band        n        raw_mean  corrected_mean  actual")
for a, b in zip(edges[:-1], edges[1:]):
    m = (raw >= a) & (raw < b + (1e-12 if b == 1 else 0))
    if m.sum() > 200:
        print(f"{a:.1f}-{b:.1f}  {m.sum():9,d}   {raw[m].mean():.3f}     {cor[m].mean():.3f}         {y[m].mean():.3f}")
m = (raw > 0.45) & (raw < 0.55)
print("raw scores near 0.50: corrected", round(cor[m].mean(), 3), " actual fraud rate", round(y[m].mean(), 3))
assert abs(cor[m].mean() - y[m].mean()) < 0.01 and abs(y[m].mean() - 0.0909) < 0.01
```

**Output (my run):**
```text
training rows 109,000, training fraud share 9.17%, true base rate 1.00%
score 0.50 -> 0.0909
odds view: 0.50 is odds 1.0; times beta 0.1 gives odds 0.1; prob 0.0909
simulated population fraud rate: 1.005%
training rows: 109316  fraud share: 9.20%
fitted intercept -4.102  true intercept -6.407  shift 2.305  ln(1/beta)= 2.303
mean score on the full population: raw 6.309%  corrected 1.004%  truth 1.005%
band        n        raw_mean  corrected_mean  actual
0.0-0.1    829,507   0.021     0.002         0.002
0.1-0.3    118,433   0.172     0.021         0.021
0.3-0.5     31,825   0.384     0.060         0.059
0.5-0.7     13,461   0.587     0.128         0.123
0.7-0.9      5,953   0.784     0.279         0.288
0.9-1.0        821   0.936     0.607         0.609
raw scores near 0.50: corrected 0.09  actual fraud rate 0.087
```

**Follow-ups:**
- What if finance wants the probability for a segment with a 3% base rate? Use that segment's prior: convert the model odds back to the training prior, then multiply by the new prior odds over the training prior odds. Check on that segment's labelled data.
- Does the correction change who gets flagged at a fixed top-k? No. It is monotone, so the ranking and any top-k list are unchanged. Only threshold-on-probability rules change.

**Common mistakes:** Reading the raw score as true probability. Applying the correction in the wrong direction. Validating calibration on undersampled data. Forgetting to set the threshold on the corrected scale. Correcting a model that also used class weights without tracking what each step did.

### Q14 ⭐⭐⭐ 🔴 A lender trained a default model only on the 60,000 approved applications from last year's 100,000, because the 40,000 rejected applicants never produced repayment outcomes. The model looks excellent on approved loans, but a new policy now lets in applicants who would previously have been rejected. Explain what bias this creates, what you would do about the rejected group, and how you would validate under the new policy.
**Asked at:** Delayed-label, positive-unlabelled and selection-bias literature (Bekker and Davis PU survey, an arXiv paper on PU survival data, an arXiv paper on PU data under selection bias); no interview page for the exact prompt, so editor-designed from the literature; search snippets only, not opened
**Say this first (1 line):** Training only on approved loans is selection bias: the model has never seen the risk of the people the old policy rejected, so under a looser policy it will underestimate their default, and I fix it with a small randomised exploration group, weighting, and a validation plan on the new band.

**Clarifying questions:**
- How were the 60,000 chosen: a score cut, officer judgement, or rules using fields the model does not see? Why: if the approval rule used only model features the bias is extrapolation; if it used hidden information, the bias is deeper.
- How wide is the new policy: a little looser or a big jump? Why: the further outside old approvals, the less the old data tells us.
- Can the business approve a small random slice of rejected applicants for learning? Why: it is the only direct way to get outcomes for them.
- Are there outcomes for rejected applicants elsewhere (credit bureau data on other loans they took)? Why: it gives a partial label without lending.
- What is the cost of a default versus a lost good customer? Why: it sets how much exploration is worth paying for.

**Approach:**
1. Name the bias: selection bias (sample selection on the outcome-related variable, also called reject inference). The training population is the approved 60,000 of 100,000; the new policy scores 40,000 people the model never saw.
2. Check overlap: compare the feature ranges of approved, rejected and new-policy applicants. Where the new band falls outside what the model trained on, predictions are extrapolation.
3. Get real labels for part of the rejected group. Best: a controlled exploration, approving a small random slice of rejected applicants within a risk budget, and recording the approval probability of each. Fallbacks: bureau performance on other loans (a proxy label), or the lender's own past policy changes.
4. Train with weights. Give each explored row a weight of 1 divided by its probability of being explored, so the sample stands for the whole rejected group, and fit on approved plus explored rows.
5. Avoid the cheap tricks as the main plan. Labelling every reject as "default" or "good" is wrong either way. Augmentation, parcelling and similar reject-inference methods use assumptions that cannot be tested from the approved data, so treat them as sensitivity analyses, not as truth.
6. Validate on the new policy. Backtest by band (approved, newly approved), compare predicted and actual default rates in the explored sample, and launch in steps (approve a small extra band first, watch matured outcomes) with a loss limit.
7. Remember delayed labels: repayment outcomes mature over months, so the first read is early-delinquency, not final default.

**Metrics:**
- Default rate by band = defaults / loans in that band, observed only for approved or explored loans.
- Calibration gap in the new band = mean predicted default minus actual default rate.
- AUC by band, not only overall (the approved-only AUC is computed on a narrow, range-restricted group and is optimistic).
- Exploration cost = expected extra losses on the explored group = explored loans x expected default rate x loss per default. Keep it inside a budget.
- Guardrails: losses per band against a limit, and approval share by band.

**Risks:**
- A model that "looks excellent" on approved loans has only been tested on the easy part of the population.
- Range restriction: AUC on a narrow group is lower than on a wide group, and calibration at the edge of the data can still be badly wrong.
- Unobserved selection: officers may have rejected people because of information not in the data (this is MNAR; no weighting can fix hidden causes).
- Exploration can cost real money and has fairness and legal questions: check with the risk and legal teams.
- Weights of 1 / p with small p are noisy; cap them or use a stabilised version.

**What the interviewer scores:**
- Strong: names selection bias and reject inference, and says the data cannot answer the question on its own.
- Strong: proposes a concrete way to get labels (exploration with recorded probabilities) and weights the results.
- Strong: validates on the new band and rolls out in steps.
- Weak: "use class weights" or "predict the rejected as defaults".
- Weak: trusts the offline AUC computed only on approved loans.

**Example:** (illustrative simulation) 100,000 applicants, the old policy approves the 60,000 lowest-risk ones and rejects 40,000. Default rate: 1.79% among approved, 20.82% among rejected. A logistic model on approved loans only predicts 4.88% for the next 25,000 applicants that the new policy would admit; the actual rate is 6.79%. In the riskiest 5,000 it predicts 22.41% when the actual is 78.84%. Approving a random 1,200 of the 40,000 rejected applicants (3%) and weighting those rows by 40,000 / 1,200 brings the prediction for the riskiest 5,000 to 76.32%, an error of 2.5 percentage points instead of 56.4. Weak answer: "AUC is 0.94 on approved loans, so launch." Strong answer: "The model has not seen these applicants; I get a small randomised sample of outcomes from the rejected group and launch in bands."

**Code:**
```python
# Q14: reject inference / selection bias (illustrative simulation)
import numpy as np
rng = np.random.default_rng(14)
def sig(z): return 1 / (1 + np.exp(-z))
def fit_logit(X, y, it=30):
    w = np.zeros(X.shape[1])
    for _ in range(it):
        p = sig(X @ w); H = (X * (p * (1 - p))[:, None]).T @ X + 1e-6 * np.eye(len(w))
        w += np.linalg.solve(H, X.T @ (y - p))
    return w
def auc(s, y):
    from scipy.stats import rankdata
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)

N = 100_000
risk = rng.normal(size=N)                  # higher = riskier applicant (bureau-style score, standardised)
true_logit = -3.6 + 0.8 * risk + 0.9 * np.maximum(risk, 0) ** 2   # risk climbs faster in the tail
default = rng.random(N) < sig(true_logit)
# old policy: approve the 60,000 lowest-risk applicants (rank cut)
order = np.argsort(risk); approved = np.zeros(N, bool); approved[order[:60_000]] = True
print("approved", approved.sum(), "rejected", (~approved).sum())
assert approved.sum() == 60_000 and (~approved).sum() == 40_000
print(f"default rate: approved {default[approved].mean():.2%}   rejected (unseen by the lender) {default[~approved].mean():.2%}")
X = np.c_[np.ones(N), risk, risk ** 2]   # a flexible-enough logit: intercept, risk, risk squared
w = fit_logit(X[approved], default[approved].astype(float))
pred = sig(X @ w)
print(f"approved-only model: AUC on approved {auc(pred[approved], default[approved].astype(int)):.3f}")
# new policy approves the next 25,000 lowest-risk applicants (ranks 60,000 to 85,000)
band = np.zeros(N, bool); band[order[60_000:85_000]] = True
print(f"new band: predicted default {pred[band].mean():.2%}  actual {default[band].mean():.2%}")
assert default[band].mean() > 1.3 * pred[band].mean()
# worst slice: the riskiest 5,000 of the rejected
tail = np.zeros(N, bool); tail[order[-5_000:]] = True
print(f"riskiest 5,000: predicted {pred[tail].mean():.2%}  actual {default[tail].mean():.2%}")
# fix 1: exploration: approve a random 3% of rejected applicants and observe them (1,200 loans)
rej_idx = np.flatnonzero(~approved)
explore = rng.choice(rej_idx, 1_200, replace=False)
print("exploration sample:", len(explore), "loans =", f"{len(explore) / 40_000:.0%} of rejected")
assert len(explore) == 1_200
# reweight the exploration rows by inverse sampling probability (1 / 0.03) and refit on approved + explored
use = np.r_[np.flatnonzero(approved), explore]
wt = np.r_[np.ones(60_000), np.full(len(explore), 40_000 / 1_200)]
w2 = np.zeros(3)
for _ in range(30):
    p = sig(X[use] @ w2); H = (X[use] * (wt * p * (1 - p))[:, None]).T @ X[use] + 1e-6 * np.eye(3)
    w2 += np.linalg.solve(H, X[use].T @ (wt * (default[use] - p)))
pred2 = sig(X @ w2)
print(f"with weighted exploration: new band predicted {pred2[band].mean():.2%}  actual {default[band].mean():.2%}; riskiest 5,000 predicted {pred2[tail].mean():.2%}")
err_old = abs(pred[tail].mean() - default[tail].mean()); err_new = abs(pred2[tail].mean() - default[tail].mean())
print(f"tail error (percentage points): approved-only {err_old * 100:.1f}  with exploration {err_new * 100:.1f}")
assert err_new < err_old
```

**Output (my run):**
```text
approved 60000 rejected 40000
default rate: approved 1.79%   rejected (unseen by the lender) 20.82%
approved-only model: AUC on approved 0.625
new band: predicted default 4.88%  actual 6.79%
riskiest 5,000: predicted 22.41%  actual 78.84%
exploration sample: 1200 loans = 3% of rejected
with weighted exploration: new band predicted 7.28%  actual 6.79%; riskiest 5,000 predicted 76.32%
tail error (percentage points): approved-only 56.4  with exploration 2.5
```

The "AUC on approved" line (0.625) is low because approved loans are a narrow, low-risk slice, not because the model is bad; that is the range-restriction risk named above. The simulated risk curve is steeper in the tail than a straight-line logit, which is what makes extrapolation fail here; real data may behave differently.

**Follow-ups:**
- Exploration is not allowed. Use bureau data on the rejected applicants' loans elsewhere as proxy labels, run sensitivity analysis under several assumptions about the rejected group's default rate, and launch only a small band with a loss cap.
- Does a simple "reject inference" method fix it? Sometimes it reduces the bias a little, but each method rests on an assumption the approved data cannot test. Use it to bound the answer, and still collect real outcomes.

**Common mistakes:** Reporting offline AUC on approved loans as the launch metric. Treating all rejects as defaults or as good. Not recording selection probabilities for exploration. Using one big launch instead of bands. Forgetting that outcomes arrive late.

### Q15 ⭐⭐⭐ 🔴 A feature's missing values were filled with the mean target value within each city, computed on the whole data set before the split, and offline AUC is 0.93 against 0.71 live. The author says imputation cannot leak because it only uses a single column. Explain the leak, how you would prove it with an experiment, and how imputation should be set up instead.
**Asked at:** Missing-data interview explainers (a PrachHub 'Missing Data, Imputation, And Selection Bias' concept page, ydata.ai 'understanding missing data mechanisms', a Towards Data Science 'Talking About Missing Data' article, a Daily Dose of Data Science post on three types of missing values); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** It leaks, because the city mean of the target uses the label of the very row being filled (and of the test rows), so the filled value contains the answer; I prove it by running the same fill on pure-noise labels and by comparing against a fill computed on training rows only, and the fix is to compute the fill inside each training fold.

**Clarifying questions:**
- How many rows per city, and how many of the missing rows are in small cities? Why: the leak is strongest when a city has few rows, because each row's own label is a large share of its city mean.
- Was the fill computed before the split, on train and test together? Why: the prompt says whole data; that also puts test labels into the training features.
- Is the imputed column missing at random, or is missingness related to the target? Why: it changes what a fair fill is.
- What does the live pipeline use to fill missing values? Why: live rows have no label, so a target-based fill cannot be reproduced at serving time, which alone explains a gap.
- Are other target-based features (target encodings) built the same way? Why: the same bug often repeats across features.

**Approach:**
1. Explain the leak in one sentence: the fill for a row is the mean of y in its city, and that mean includes this row's own y; for a city of 10 rows, 10% of the filled value is the row's own label.
2. Show the second leak: computing the city means on the whole data before the split lets test labels flow into training features.
3. Prove it with a noise experiment. Make the label unrelated to every feature (or shuffle it), fill the way the author did, and measure AUC of the filled value. A feature built without leakage gets about 0.5; a leaking one scores well above that. Repeat after shuffling to be sure it does not depend on one draw.
4. Show the live gap: in production the label is unknown, so a target-based fill cannot run the same way. The model learned a pattern that does not exist live, and AUC falls from 0.93 towards 0.71.
5. Fix: split first. Fit every imputation inside the training fold only. For a target-based fill on training rows use out-of-fold means (smoothed toward the global mean, so small cities do not carry noise); for validation and test rows use the training-fold means. Prefer fills that do not use the target at all (median, a model on other features, plus a missing flag) unless the target-based one earns its place on honest validation.
6. Wrap it in a pipeline so the fill is part of the fitted model and cannot be fitted on all rows by mistake.
7. Cross-reference: Book 1 Part 2 asks "How do you do target encoding without leakage (out-of-fold, smoothing)?" and the same fix applies here.

**Metrics:**
- AUC of the filled value on rows where it was missing: leaky fill versus fill computed on training rows only (noise-label test; honest value is about 0.5).
- Own-label share = 1 / rows in the city (10 rows gives 10%).
- Gap = offline AUC minus live (or time-forward) AUC. Here 0.93 versus 0.71 is 0.22.
- Guardrail: after the fix, offline and honest holdout AUC should agree within a few points.

**Risks:**
- The author's argument "it only uses one column" misses that the column is the target's own summary.
- A noise-label test shows that a leak exists, not how big it is on real data; also run the corrected pipeline and see the real drop.
- Small cities make out-of-fold means noisy; without smoothing the honest fill can hurt.
- Other steps (scaling, selection, encoding) may leak the same way.

**What the interviewer scores:**
- Strong: states the self-inclusion leak and the train-test leak separately, and notes live rows have no label.
- Strong: a concrete proof experiment (noise or shuffled labels) with a number.
- Strong: the fix is fitted inside folds, with out-of-fold or smoothed means, in a pipeline.
- Weak: accepts "single column cannot leak", or just says "do it after the split" without explaining why.

**Example:** (illustrative simulation) 20,000 rows in 2,000 cities (about 10 per city), a label that is pure noise with a 10% rate, and a feature missing in 60% of rows. Among the 3,554 test rows where the feature was missing, the leaky filled value reaches AUC 0.790 on a label with no signal. The fill computed on training rows only gives 0.477, and the out-of-fold fill on training rows gives 0.498. After shuffling the labels five times the leaky AUC stays between 0.779 and 0.809, so it is the fill reading the label, not luck. Weak answer: "Imputation uses one column, so it is safe." Strong answer: "The filled value contains the row's own label; I show an AUC of 0.79 on noise, then fit the fill inside the folds."

**Code:**
```python
# Q15: target-mean imputation computed before the split leaks the label (illustrative simulation)
import numpy as np
from scipy.stats import rankdata
rng = np.random.default_rng(15)
def auc(s, y):
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
N, CITIES = 20_000, 2_000                   # about 10 rows per city
city = rng.integers(0, CITIES, N)
y = (rng.random(N) < 0.10).astype(int)      # label is pure noise: NO real signal in any column
missing = rng.random(N) < 0.60               # feature missing in 60% of rows
test = rng.random(N) < 0.30

def city_target_mean(idx_fit, idx_apply):
    s = np.bincount(city[idx_fit], weights=y[idx_fit], minlength=CITIES)
    c = np.bincount(city[idx_fit], minlength=CITIES)
    g = y[idx_fit].mean()
    m = np.where(c > 0, s / np.maximum(c, 1), g)
    return m[city[idx_apply]]

allrows = np.arange(N)
leaky = city_target_mean(allrows, allrows)                  # whole data, before the split
tr, te = np.flatnonzero(~test), np.flatnonzero(test)
clean = city_target_mean(tr, te)                            # train rows only
m_te = missing[te]
a_leaky = auc(leaky[te][m_te], y[te][m_te])
a_clean = auc(clean[m_te], y[te][m_te])
print(f"test rows with a filled value: {m_te.sum()}")
print(f"AUC of the filled value on a label with NO signal: leaky {a_leaky:.3f}   train-only fill {a_clean:.3f}")
assert a_leaky > 0.58 and abs(a_clean - 0.5) < 0.05
# permutation proof: shuffle the labels, redo the leaky fill; AUC stays high -> the fill is reading y
y_real = y.copy()
aucs = []
for _ in range(5):
    y[:] = rng.permutation(y_real)
    lk = city_target_mean(allrows, allrows)
    aucs.append(auc(lk[te][m_te], y[te][m_te]))
print("leaky AUC after shuffling labels (5 shuffles):", [round(float(a), 3) for a in aucs])
assert min(aucs) > 0.58
# why: a row's own label sits inside its city mean.  Own-label share = 1 / rows in city
n_city = np.bincount(city, minlength=CITIES)
print(f"median rows per city {np.median(n_city):.0f}; own label is {1 / np.median(n_city):.0%} of that city's mean")
# the right setup: fit the fill inside each training fold, with out-of-fold means for training rows
folds = rng.integers(0, 5, len(tr)); oof = np.zeros(len(tr))
for k in range(5):
    fit_idx, app_idx = tr[folds != k], tr[folds == k]
    oof[folds == k] = city_target_mean(fit_idx, app_idx)
a_oof = auc(oof[missing[tr]], y[tr][missing[tr]])
print(f"out-of-fold fill on training rows: AUC {a_oof:.3f}  (honest, close to 0.5)")
assert abs(a_oof - 0.5) < 0.05
```

**Output (my run):**
```text
test rows with a filled value: 3554
AUC of the filled value on a label with NO signal: leaky 0.790   train-only fill 0.477
leaky AUC after shuffling labels (5 shuffles): [0.792, 0.785, 0.794, 0.809, 0.779]
median rows per city 10; own label is 10% of that city's mean
out-of-fold fill on training rows: AUC 0.498  (honest, close to 0.5)
```

**Follow-ups:**
- Is target-based imputation ever fine? Yes, if it is computed out-of-fold, smoothed, and it still beats a plain median plus a missing flag on honest validation. Many teams skip it because it is hard to serve.
- How would you catch this in review? Ask of every feature: "could this be computed at prediction time with no label?" and run a shuffled-label check on the full pipeline.

**Common mistakes:** Fitting any imputer, scaler or encoder on the whole data before the split. Using target means without out-of-fold or smoothing. Trusting a suspiciously high offline AUC. Checking only the final model, not each feature.

### Q16 ⭐⭐⭐ 🔴 After a vendor outage, a model feature that was missing in 5% of training rows was missing in 40% of live rows for two days, and live AUC fell from 0.83 to 0.74. The model uses mean imputation without a missing flag. Explain how you would diagnose this, what you would change in training and serving to make the model robust, and how you would alert on it.
**Asked at:** Missing-data interview explainers (a PrachHub 'Missing Data, Imputation, And Selection Bias' concept page, ydata.ai 'understanding missing data mechanisms', a Towards Data Science 'Talking About Missing Data' article, a Daily Dose of Data Science post on three types of missing values); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** When a feature that is missing in 5% of training rows is missing in 40% of live rows, the model is scoring a population it never trained on, so I confirm it with missingness and score-shift monitoring, expect part of the AUC loss to be unavoidable (the information is gone), and make the model robust by training with realistic random missingness and alerting on the missing rate.

**Clarifying questions:**
- Was the missingness random across users (an outage) or concentrated in a segment? Why: concentrated missingness shifts the population, random missingness mostly removes information.
- In training, was the feature missing at random or tied to the label? Why: if missingness carried label information in training, a missing flag learns that, and the outage breaks it.
- Is there a fallback source or a cached older value for the feature? Why: a stale value may beat a mean fill.
- How important is the feature (importance, ablation drop)? Why: it sets how much AUC loss is the floor.
- Are decisions made on probabilities or on ranks (thresholds, expected loss)? Why: score levels moved even if ranks did not.

**Approach:**
1. Confirm the cause from logs: missing rate by hour for this feature (5% to 40% in two days), then compare model AUC on rows with the feature present versus missing. If AUC on present rows is still 0.83 and the drop sits in the missing rows, the outage explains it.
2. Check the score distribution: mean score, and share above the threshold, by missing versus present. Mean imputation pushes outage rows to the middle, so thresholds fire differently.
3. Separate unavoidable loss from avoidable loss. Unavoidable: the feature's information is not there. Avoidable: calibration and threshold shifts caused by how the model treats missing values.
4. Training changes: add a missing indicator, and train with extra random missingness (for example drop the feature in a random 30% to 40% of training copies) so the model learns to rely on other features when it is absent. For trees, use native missing-value handling. Do not let the missing flag stand for risk in training if outages break that link.
5. Serving changes: send the true missing state to the model (do not silently fill with a stale default), use a fallback source when it exists, and route to a smaller model without the feature if the missing rate stays high.
6. Alerting: monitor the hourly missing rate per feature against its training rate with a binomial limit (about 6.9% at 2,000 requests an hour, below), page when it crosses, and also monitor mean score and share flagged.
7. Test the setup: replay the outage in staging (force 40% missing) before the next one.
8. Cross-reference: Book 6 Part 2 has "After an upstream deploy, the merchant_category feature's null rate jumped from 0.5% to 18% overnight" for the production-incident side.

**Metrics:**
- Missing rate = rows with the feature missing / rows scored, per hour, per feature.
- Alert limit = the 99.99th percentile of Binomial(requests per hour, training rate) divided by requests; at 2,000 requests and 5% it is 138 rows (6.9%).
- AUC (and mean score versus actual rate) at 5% and at 40% missing, for each model variant.
- Guardrail: calibration (mean score versus actual rate) and the share of rows flagged by the threshold.

**Risks:**
- A missing flag trained where the label is linked to missingness can hurt in an outage: in the simulation the flag model over-scores outage rows.
- Over-augmenting makes the model lean less on the feature even when it is present; check AUC at 5% missing too.
- Alerts on the average hide a segment-only outage; slice by source and region.
- Backfilling after the outage and retraining on the outage days can teach the wrong pattern; exclude or flag those days.

**What the interviewer scores:**
- Strong: separates information lost from avoidable damage (calibration, thresholds), and proves the cause with logs.
- Strong: robust training (random missingness) and a serving fallback, not only "impute better".
- Strong: a concrete alert design with a base rate and a false-alarm rate.
- Weak: "retrain on the outage data" or "just use a missing flag".
- Weak: no monitoring plan.

**Example:** (illustrative simulation, not the prompt's AUC values) In training the feature is missing for 5% of rows, 61% positive among missing versus 32.4% among present. Live, the feature goes missing at random for 40% of rows. The mean-imputation model without a flag drops from AUC 0.833 to 0.786. The model with a flag learned from training (coefficient 1.44) is worse, 0.761, and its mean score rises from 0.340 to 0.427 while the real rate is 0.341. The model trained with extra random missingness (flag coefficient 0.5) keeps 0.786 and a mean score of 0.350. So about 0.047 of AUC is information loss for every model, and the flag model adds avoidable damage. Alert design: at 2,000 requests per hour and a 5% baseline, alert above 138 missing requests (6.9%); the outage hour had 819. Weak answer: "Retrain on the new data." Strong answer: "Prove it from the missing rate, accept the information loss, fix the avoidable damage with training that expects missingness, and alert on the rate."

**Code:**
```python
# Q16: feature missingness jumps from 5% to 40% (illustrative simulation)
import numpy as np
from scipy.stats import rankdata, norm
rng = np.random.default_rng(16)
def sig(z): return 1 / (1 + np.exp(-z))
def auc(s, y):
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
def fit(X, y, it=30):
    w = np.zeros(X.shape[1])
    for _ in range(it):
        p = sig(X @ w); H = (X * (p * (1 - p))[:, None]).T @ X + 1e-6 * np.eye(len(w))
        w += np.linalg.solve(H, X.T @ (y - p))
    return w
def make(n, miss_rate, informative=False):
    x1, x2 = rng.normal(size=n), rng.normal(size=n)
    y = (rng.random(n) < sig(-1.0 + 1.0 * x1 + 1.4 * x2)).astype(float)
    if informative:      # training world: the feature is missing more often for positives (about 5% overall)
        miss = rng.random(n) < np.where(y == 1, 0.09, 0.03)
    else:                # outage world: missing at random, whatever the label
        miss = rng.random(n) < miss_rate
    return x1, x2, miss, y
def design(x1, x2, miss, mu2, flag):
    x2f = np.where(miss, mu2, x2)                       # mean imputation
    cols = [np.ones(len(x1)), x1, x2f] + ([miss.astype(float)] if flag else [])
    return np.c_[tuple(cols)]
x1, x2, m, y = make(300_000, 0, informative=True)
print(f"training: missing rate {m.mean():.1%}; positive rate when missing {y[m].mean():.1%} vs present {y[~m].mean():.1%}")
mu2 = x2[~m].mean()
# A: today's setup (mean imputation, no flag)
wA = fit(design(x1, x2, m, mu2, False), y)
# B: add a missing flag, trained on the real 5% (the flag soaks up the label link)
wB = fit(design(x1, x2, m, mu2, True), y)
# C: flag, but training copies also get extra RANDOM missingness (to about 40%), so the flag cannot stand for risk
x1c, x2c, mc, yc = np.r_[x1, x1], np.r_[x2, x2], np.r_[m, m | (rng.random(len(m)) < 0.37)], np.r_[y, y]
wC = fit(design(x1c, x2c, mc, mu2, True), yc)
print("flag coefficient: B", round(float(wB[3]), 2), " C", round(float(wC[3]), 2))
out = {}
for rate in (0.05, 0.40):
    a1, a2, am, ay = make(150_000, rate)
    row = []
    for w, f in ((wA, False), (wB, True), (wC, True)):
        sc = design(a1, a2, am, mu2, f) @ w
        row.append((auc(sc, ay), float(sig(sc).mean())))
    out[rate] = row
    print(f"live missing {rate:.0%} (random): actual rate {ay.mean():.3f} | AUC / mean score  A {row[0][0]:.3f} / {row[0][1]:.3f}   B {row[1][0]:.3f} / {row[1][1]:.3f}   C {row[2][0]:.3f} / {row[2][1]:.3f}")
assert out[0.05][0][0] - out[0.40][0][0] > 0.04          # every model loses AUC: the information really is gone
assert out[0.40][1][0] < out[0.40][2][0] - 0.01           # flag-trained-on-5% (B) is worse than the augmented model (C)
# alert: hourly missing rate against the training rate, exact binomial limit, 2,000 requests an hour
from scipy.stats import binom
n_h, p0 = 2_000, 0.05
limit = binom.ppf(0.9999, n_h, p0)                       # about 1 false alarm in 10,000 normal hours
print(f"alert when more than {int(limit)} of {n_h} hourly requests are missing ({limit / n_h:.2%})")
quiet = rng.binomial(n_h, p0, 24 * 30)
print("false alarms in 30 days (720 normal hours):", int((quiet > limit).sum()))
outage = rng.binomial(n_h, 0.40)
print(f"outage hour: {outage} missing of {n_h} -> alarm {outage > limit}")
assert limit / n_h < 0.07 and outage > limit
```

**Output (my run):**
```text
training: missing rate 5.0%; positive rate when missing 61.0% vs present 32.4%
flag coefficient: B 1.44  C 0.5
live missing 5% (random): actual rate 0.340 | AUC / mean score  A 0.833 / 0.340   B 0.828 / 0.340   C 0.833 / 0.330
live missing 40% (random): actual rate 0.341 | AUC / mean score  A 0.786 / 0.328   B 0.761 / 0.427   C 0.786 / 0.350
alert when more than 138 of 2000 hourly requests are missing (6.90%)
false alarms in 30 days (720 normal hours): 0
outage hour: 819 missing of 2000 -> alarm True
```

**Follow-ups:**
- The outage lasts weeks. Retrain with the new missing rate in the mix only if the new rate is the new normal; otherwise keep the model and route to the fallback, and re-evaluate when the vendor recovers.
- Can the model detect the outage itself? Monitor the input's missing rate and the score distribution; the model's own error is delayed because labels arrive late.

**Common mistakes:** Filling with a stale default silently. Adding a missing flag without checking whether missingness was tied to the label. Alerting only on AUC, which arrives late. Treating all AUC loss as a bug instead of lost information.

### Q17 ⭐⭐ 🟢 A data set of 60,000 rows has 300 positives (0.5%), and a tree ensemble takes two hours to train. A teammate suggests SMOTE, another suggests class weights, and a third suggests undersampling. Explain which you would try first, in what order you would compare them, and what metric you would compare them on.
**Asked at:** Imbalanced-data and fraud-evaluation guides (techinterview.org 'Handling Imbalanced Datasets in Machine Learning', Dataford fraud-evaluation prompts such as 'how do you evaluate a fraud detection model on imbalanced data', a KDnuggets piece on SMOTE misuse, a Coresignal 'class imbalance interview trap' post); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** I would not start with any of them: I would first train a plain model with a proper metric (PR-AUC) and threshold tuning, then test class weights and undersampling because they are cheap, and try SMOTE last because it is the slowest and most error-prone, comparing all on PR-AUC across several seeds.

**Clarifying questions:**
- What decision does the score drive and what are the costs of a miss and a false alarm? Why: it picks the metric and the threshold, which matter more than the resampling.
- Are the 300 positives all from one time period or one source? Why: SMOTE interpolates between positives, and a clustered positive set gives odd synthetic points.
- How noisy are the labels? Why: SMOTE copies noise into synthetic rows.
- Do I need calibrated probabilities? Why: resampling and weights both shift probabilities and need a correction.
- Compute budget: is two hours per run a limit on how many comparisons I can afford? Why: I should compare cheap variants first.

**Approach:**
1. Fix the evaluation before the method: a stratified split (or repeated stratified folds), metric PR-AUC (average precision, whose no-skill value is the base rate, 0.5%), plus recall at the review budget. With 300 positives the metric is noisy, so use repeated folds and report the spread.
2. Baseline: the model with no rebalancing, and a tuned threshold. Rank-based metrics often change little with weights alone.
3. Class weights: nearly free, no extra rows, no leakage risk. A weight near negatives / positives (199 here) is a starting point; lower weights are worth a try.
4. Undersampling: keep all 300 positives and, say, ten negatives per positive (3,000), so the training set is 3,300 rows. This cuts training time sharply. Repeat with several random negative samples (bagging) to lose less information.
5. SMOTE: only if the above leave a gap. Apply it inside each training fold only (never before the split), tune k, and check against weights. It needs numeric, well-scaled features and gets awkward with categoricals.
6. Compare on the same folds and seeds and keep the simplest method inside the noise. If probabilities are needed, correct or recalibrate on full-rate validation data (Book 1 Part 3 "Does class weighting, SMOTE or undersampling break probability calibration?").
7. Cross-reference: Book 1 Part 3 covers the concepts in "Class weights vs resampling (over/under-sampling): trade-offs, and which would you try first?", "PR-AUC: what is its random baseline" and "Where in the pipeline do you apply SMOTE or resampling?".

**Metrics:**
- Average precision (PR-AUC) = mean of the precision at each true positive's rank. No-skill value is the positive rate, 300 / 60,000 = 0.5%.
- Recall at the review budget = true positives in the top k / all positives.
- Spread = standard deviation of the metric over seeds or folds. A difference smaller than that is not a real difference.
- Cost: training rows and wall-clock time. Guardrail: calibration if the probabilities are used.

**Risks:**
- Applying SMOTE or undersampling before the split (leakage and inflated results).
- Comparing methods on ROC-AUC or accuracy, which hide the difference.
- Differences smaller than seed noise being read as wins.
- Resampled models need probability correction.
- With 300 positives, a single holdout split is a lottery.

**What the interviewer scores:**
- Strong: metric and split first, then a cheap-to-expensive order of methods with a reason for each.
- Strong: compares over several seeds and says "no real difference" when that is what the numbers show.
- Strong: mentions time cost (3,300 rows versus 119,400) and probability calibration.
- Weak: "use SMOTE" as the first and only answer.
- Weak: evaluates on accuracy or on a balanced test set.

**Example:** (illustrative simulation, 8 seeds) 60,000 training rows and 300 positives, a test set of 60,000 rows with 300 positives (no-skill average precision about 0.005). Plain logistic model: mean AP 0.0785 (sd 0.0153); class weight 199: 0.0778; undersampling to 1:10: 0.0782; SMOTE to 1:1: 0.0778. The spread between method means is 0.0007, against a seed-to-seed standard deviation of 0.0155, so there is no real difference in this setup. Training rows: 60,000, 60,000, 3,300 and 119,400. If the two-hour run scales linearly with rows (an assumption), undersampling takes about 7 minutes and SMOTE to 1:1 about 4 hours. So the cheap method wins on cost. Weak answer: "SMOTE, it is the standard fix." Strong answer: "Metric first, then weights and undersampling because they are cheap, SMOTE last, compared over seeds."

**Code:**
```python
# Q17: SMOTE vs class weights vs undersampling on 0.5% positives (illustrative simulation)
import numpy as np
rng = np.random.default_rng(17)
def sig(z): return 1 / (1 + np.exp(-z))
def fit(X, y, wt=None, it=25, l2=1.0):
    wt = np.ones(len(y)) if wt is None else wt
    w = np.zeros(X.shape[1])
    for _ in range(it):
        p = sig(X @ w); H = (X * (wt * p * (1 - p))[:, None]).T @ X + l2 * np.eye(len(w))
        w += np.linalg.solve(H, X.T @ (wt * (y - p)) - l2 * w)
    return w
def avg_precision(s, y):
    o = np.argsort(-s); yy = y[o]; tp = np.cumsum(yy)
    return float((tp / np.arange(1, len(yy) + 1))[yy == 1].mean())
D = 10
beta = np.r_[1.2, 0.8, 0.5, np.zeros(D - 3)]
def make(n, pos):
    X = rng.normal(size=(n, D)); X[:pos] += 1.0 * beta  # first rows are positives, shifted
    y = np.zeros(n); y[:pos] = 1
    return X, y
def smote(Xp, n_new, k=5):
    d = ((Xp[:, None, :] - Xp[None, :, :]) ** 2).sum(-1); np.fill_diagonal(d, np.inf)
    nn = np.argsort(d, 1)[:, :k]
    i = rng.integers(0, len(Xp), n_new); j = nn[i, rng.integers(0, k, n_new)]
    t = rng.random((n_new, 1)); return Xp[i] + t * (Xp[j] - Xp[i])
res = {k: [] for k in ("plain", "class weight", "undersample 1:10", "SMOTE to 1:1")}
for seed in range(8):
    Xtr, ytr = make(60_000, 300); Xte, yte = make(60_000, 300)
    A = lambda X: np.c_[np.ones(len(X)), X]
    res["plain"].append(avg_precision(A(Xte) @ fit(A(Xtr), ytr), yte))
    wt = np.where(ytr == 1, 199.0, 1.0)
    res["class weight"].append(avg_precision(A(Xte) @ fit(A(Xtr), ytr, wt), yte))
    neg = np.flatnonzero(ytr == 0); keep = np.r_[np.arange(300), rng.choice(neg, 3_000, replace=False)]
    res["undersample 1:10"].append(avg_precision(A(Xte) @ fit(A(Xtr[keep]), ytr[keep]), yte))
    Xs = np.r_[Xtr, smote(Xtr[:300], 59_400)]; ys = np.r_[ytr, np.ones(59_400)]
    res["SMOTE to 1:1"].append(avg_precision(A(Xte) @ fit(A(Xs), ys), yte))
print("test positive rate 0.50%, so a no-skill average precision is about 0.005")
print(f"{'method':18} {'mean AP':>8} {'sd over 8 seeds':>16} {'train rows':>11}")
rows = {"plain": 60_000, "class weight": 60_000, "undersample 1:10": 3_300, "SMOTE to 1:1": 119_400}
for k, v in res.items(): print(f"{k:18} {np.mean(v):8.4f} {np.std(v, ddof=1):16.4f} {rows[k]:11,d}")
# time arithmetic from the prompt (assume time grows linearly with rows; an assumption, not a measurement)
base_h = 2.0
for k in ("undersample 1:10", "SMOTE to 1:1"):
    print(f"{k}: about {base_h * rows[k] / 60_000 * 60:.0f} minutes if time is linear in rows")
assert round(base_h * 3_300 / 60_000 * 60) == 7 and round(base_h * 119_400 / 60_000) == 4
assert 60_000 * 0.005 == 300
m = {k: np.mean(v) for k, v in res.items()}
assert min(m.values()) > 10 * 0.005
spread = max(m.values()) - min(m.values()); sd = np.mean([np.std(v, ddof=1) for v in res.values()])
print(f'spread of method means {spread:.4f} versus seed-to-seed sd {sd:.4f}')
```

**Output (my run):**
```text
test positive rate 0.50%, so a no-skill average precision is about 0.005
method              mean AP  sd over 8 seeds  train rows
plain                0.0785           0.0153      60,000
class weight         0.0778           0.0153      60,000
undersample 1:10     0.0782           0.0161       3,300
SMOTE to 1:1         0.0778           0.0152     119,400
undersample 1:10: about 7 minutes if time is linear in rows
SMOTE to 1:1: about 239 minutes if time is linear in rows
spread of method means 0.0007 versus seed-to-seed sd 0.0155
```

The simulation uses a logistic model and a simple self-written SMOTE (five nearest positives, random interpolation); with a tree ensemble the numbers will differ, so run the comparison on your own model. The finding "no real difference" belongs to this simulated setup, not to all data.

**Follow-ups:**
- When would SMOTE win? Sometimes with a model that overfits tiny positive sets, such as a deep net or a very flexible tree model, in low dimensions with continuous features; test it, do not assume.
- The comparison is within noise. Pick the cheapest, then spend effort on features, label quality and the threshold.

**Common mistakes:** Resampling before the split. Using accuracy. Comparing on one seed. Treating 1:1 as the target ratio by default. Forgetting to fix probabilities after resampling.

### Q18 ⭐⭐ 🟢 Two annotators labelled 1,000 support tickets as urgent or not and agreed on 820 of them (82% raw agreement), and each marked about 30% of tickets as urgent. The team says 82% agreement is good enough. Explain what chance-adjusted agreement says here, what the disagreements suggest about the guidelines, and how you would form training labels.
**Asked at:** Noisy-label and annotator-disagreement material (Tanno et al., CVPR 2019 on annotator confusion matrices; a Codemia data-labelling course page); research and course pages rather than interview banks, so the scenario is partly editor-designed; search snippets only, not opened
**Say this first (1 line):** 82% raw agreement is not good enough to judge, because with 30% urgent each annotator you would agree 58% of the time by chance alone, so chance-adjusted agreement (Cohen's kappa) is 0.57, only moderate, and the 180 disagreements point to unclear guidelines.

**Clarifying questions:**
- Are "urgent" and "not urgent" defined by written criteria with examples? Why: vague criteria produce disagreement that more annotators cannot fix.
- Were both annotators trained and independent (no discussion)? Why: shared habits inflate agreement.
- Is the 30% urgent rate each annotator's own, or the real rate in the data? Why: kappa depends on prevalence.
- What is the cost of a wrong "urgent" label (missed urgent ticket versus wasted attention)? Why: it sets how much to spend on adjudication.
- Is there an expert or ground truth for a subset? Why: agreement is not accuracy; two annotators can agree and both be wrong.

**Approach:**
1. Rebuild the 2x2 table from the numbers. 1,000 tickets, each marks 300 urgent. Disagreements are 180. Both urgent = (300 + 300 - 180) / 2 = 210, each has 90 tickets the other did not mark, and both said not urgent for 610. Agreement 210 + 610 = 820.
2. Chance agreement: 0.3 x 0.3 + 0.7 x 0.7 = 0.58. Kappa = (0.82 - 0.58) / (1 - 0.58) = 0.571. That is moderate, not "good enough".
3. Look at class-specific agreement: on "urgent" the two agree on 0.70 of their combined urgent marks (2 x 210 / 600); on "not urgent" 0.87. The positive class, which matters, is where they disagree most.
4. Read the 180 disagreements (all of them, or a sample of 60 to 100) and group them: unclear rule, missing context (a ticket needs the customer's history), genuine borderline, or annotator slip. Fix the guidelines with examples and re-annotate a fresh sample to see whether kappa rises.
5. Forming labels: keep the 820 agreed rows; send the 180 disagreements to a third senior reviewer (adjudication); for a high-volume setup, use 3 annotators and majority vote. Keep a flag or soft label for borderline tickets and consider down-weighting them in training.
6. Report agreement in the model card (kappa and the by-class numbers) and use it as a ceiling for model performance: a model cannot be much better than labels that humans disagree on.

**Metrics:**
- Observed agreement p_o = agreements / tickets = 820 / 1,000 = 0.82.
- Chance agreement p_e = sum over classes of (A's share x B's share) = 0.3 x 0.3 + 0.7 x 0.7 = 0.58.
- Cohen's kappa = (p_o - p_e) / (1 - p_e) = 0.571. Add a bootstrap interval (here about 0.52 to 0.63).
- Positive-class agreement = 2 x both-positive / (A positives + B positives) = 0.70.
- Guardrail: kappa after the guideline fix on a fresh sample.

**Risks:**
- Kappa depends on prevalence: with rare classes it can be low even when raw agreement is high (a 5% urgent rate and 92% agreement gives kappa 0.158).
- Agreement is not correctness: both annotators can be wrong in the same way.
- Two annotators only: with disagreement you cannot tell which is right without a third.
- Adjudicating only disagreements ignores cases where both are wrong together.

**What the interviewer scores:**
- Strong: computes chance agreement and kappa correctly from the given numbers, and says "moderate".
- Strong: treats disagreements as information about the guidelines, not noise to average away.
- Strong: concrete label formation (adjudication or majority vote, soft labels) and keeps agreement as a quality ceiling.
- Weak: "82% is fine" or calls kappa a model metric.
- Weak: drops all disagreeing tickets without looking at them (this biases against hard cases).

**Example:** (illustrative numbers) 1,000 tickets, 820 agreements, each annotator marks 300 urgent. Table: both urgent 210, A only 90, B only 90, neither 610. Chance agreement 0.58, kappa 0.571, bootstrap 95% interval about 0.52 to 0.63. The trap in the other direction: with only 5% urgent each and 92% raw agreement, chance is 0.905 and kappa is 0.158. Weak answer: "82% agreement is above 80%, so we are fine." Strong answer: "Chance would give 58%, so kappa is 0.57; the 180 disagreements need a guideline fix and a third reviewer."

**Code:**
```python
# Q18: raw agreement versus chance-adjusted agreement (illustrative)
import numpy as np
rng = np.random.default_rng(18)
n, agree, urgent_a, urgent_b = 1_000, 820, 300, 300
# 2x2 table: both urgent x, A only a_only, B only b_only, neither
x = (urgent_a + urgent_b - (n - agree)) // 2          # both = (300+300-180)/2
a_only, b_only = urgent_a - x, urgent_b - x
neither = n - x - a_only - b_only
print("both urgent", x, " A only", a_only, " B only", b_only, " neither", neither)
assert (x, a_only, b_only, neither) == (210, 90, 90, 610) and x + neither == agree
po = agree / n
pe = (urgent_a / n) * (urgent_b / n) + (1 - urgent_a / n) * (1 - urgent_b / n)
kappa = (po - pe) / (1 - pe)
print(f"observed {po:.3f}  chance {pe:.3f}  kappa {kappa:.3f}")
assert round(pe, 2) == 0.58 and round(kappa, 3) == 0.571
# positive-class agreement: 2*both / (A urgent + B urgent)
pos_agree = 2 * x / (urgent_a + urgent_b); neg_agree = 2 * neither / ((n - urgent_a) + (n - urgent_b))
print(f"agreement on 'urgent' {pos_agree:.2f}, on 'not urgent' {neg_agree:.2f}")
assert round(pos_agree, 2) == 0.70
# bootstrap interval for kappa
cells = np.array([x, a_only, b_only, neither]); labs = np.repeat(np.arange(4), cells)
ks = []
for _ in range(2_000):
    s = rng.choice(labs, n); c = np.bincount(s, minlength=4)
    p_o = (c[0] + c[3]) / n; ua, ub = (c[0] + c[1]) / n, (c[0] + c[2]) / n
    p_e = ua * ub + (1 - ua) * (1 - ub); ks.append((p_o - p_e) / (1 - p_e))
lo, hi = np.percentile(ks, [2.5, 97.5]); print(f"bootstrap 95% interval for kappa: {lo:.2f} to {hi:.2f}")
assert lo < kappa < hi
# the trap: 5% prevalence, 92% agreement
pe2 = 0.05 ** 2 + 0.95 ** 2; k2 = (0.92 - pe2) / (1 - pe2)
print(f"5% urgent each, 92% raw agreement: chance {pe2:.3f}, kappa {k2:.3f}")
assert round(k2, 3) == 0.158
# forming labels: keep the 820 agreed rows, send the 180 disagreements to a third, senior reviewer
print("rows to adjudicate:", n - agree, f"= {(n - agree) / n:.0%} of the sample; extra labels needed: {n - agree}")
# if instead one annotator is picked at random for the 180, expected wrong labels among them is half if one is right
print("expected wrong labels if we pick a random annotator on the disagreements:", (n - agree) // 2)
```

**Output (my run):**
```text
both urgent 210  A only 90  B only 90  neither 610
observed 0.820  chance 0.580  kappa 0.571
agreement on 'urgent' 0.70, on 'not urgent' 0.87
bootstrap 95% interval for kappa: 0.52 to 0.63
5% urgent each, 92% raw agreement: chance 0.905, kappa 0.158
rows to adjudicate: 180 = 18% of the sample; extra labels needed: 180
expected wrong labels if we pick a random annotator on the disagreements: 90
```

**Follow-ups:**
- Who breaks ties? A senior reviewer or domain expert, with a short written reason that goes back into the guidelines. If the cost of a wrong label is low, a third annotator vote can do it.
- Would you use soft labels? Yes if there are many borderline tickets: use the share of annotators saying urgent as a target or as a sample weight, and test whether it helps on a trusted validation set.

**Common mistakes:** Quoting raw agreement alone. Reading kappa without prevalence. Throwing away disagreements. Treating agreement as accuracy. Changing guidelines without re-measuring.

### Q19 ⭐⭐ 🟢 A table of 200,000 rows with 1,000 positives has 4,000 rows with a missing key feature, and 600 of those 4,000 rows are positive, against 400 positives among the other 196,000 rows. A manager says to drop the 4,000 rows because they are only 2% of the data. Explain why that is risky, what the numbers imply about the missingness, and what you would do instead.
**Asked at:** Missing-data interview explainers (a PrachHub 'Missing Data, Imputation, And Selection Bias' concept page, ydata.ai 'understanding missing data mechanisms', a Towards Data Science 'Talking About Missing Data' article, a Daily Dose of Data Science post on three types of missing values); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Dropping those 4,000 rows is risky because the missing group is only 2% of the rows but holds 60% of the positives, with a positive rate of 15% versus 0.2% elsewhere, so the missingness itself is a strong signal and I would keep the rows and add a missing flag.

**Clarifying questions:**
- Why is the feature missing (not collected, not applicable, a failed lookup, a customer who did not give it)? Why: the reason tells me whether missing means "risky" or just "unknown".
- Will live traffic also have this feature missing at about 2%? Why: if yes, the model must be able to score those rows; dropping them from training means it never learns them.
- Is the key feature related to the label for non-missing rows? Why: it tells me whether the feature adds anything beyond the flag.
- Did the missing share change over time? Why: a changing share means a changing process.
- What does the business do with scores on those rows? Why: they may need a separate rule or manual review.

**Approach:**
1. Do the counts: 200,000 rows and 1,000 positives; 4,000 rows missing (2.0%) hold 600 positives (60% of all positives); the other 196,000 rows hold 400 (0.204%).
2. Compare rates: 600 / 4,000 = 15.0% versus 400 / 196,000 = 0.204%, a ratio of 73.5. A chi-square test on the 2x2 table gives a huge statistic (17,250 in the run below), so this is far from chance.
3. Interpret: missingness is not random with respect to the label. It looks like MAR or MNAR (depends on something observed, or on the unobserved value or risk itself). I cannot prove which from the data alone, and either way the flag matters.
4. Show the danger of dropping: the model would train on 400 of 1,000 positives and never see the most positive-heavy group, while live traffic still contains these rows. It would score them like normal rows and miss most of the positives there.
5. Do instead: keep the rows, add `feature_missing` as a feature, fill the value in a simple way (median or model-based, fitted on training folds), or use a model that handles missing values natively. Investigate the cause with the data owner.
6. Check the alternatives on an honest, time-split holdout that also contains missing rows: dropped versus flag plus fill. Report performance separately for missing and present rows.
7. Operations: monitor the missing rate in production and decide, with the business, what happens to rows with a missing key (a rule, manual review, a separate model).

**Metrics:**
- Positive rate by group = positives / rows in the group: 15.0% versus 0.204%.
- Share of positives in the group = 600 / 1,000 = 60%; share of rows = 4,000 / 200,000 = 2%.
- AUC of the missing flag alone = (1 + TPR - FPR) / 2 with TPR = 0.60 and FPR = 3,400 / 199,000 = 0.0171, so 0.791.
- Performance on missing rows and on present rows separately, plus overall PR-AUC.

**Risks:**
- Dropping rows removes most of the signal and creates a mismatch with live traffic.
- The flag can encode a process artefact (for example a fraud team's manual step that fills the field), and then it will not hold at launch. Ask how the value is produced.
- Imputing without a flag throws away the strongest signal.
- If missingness is MNAR, no method recovers the missing value from the data alone; stay humble in claims.

**What the interviewer scores:**
- Strong: computes 15% versus 0.2%, notes 60% of positives, and concludes the missingness is informative.
- Strong: keeps the rows, adds a flag, and evaluates on missing and present groups separately.
- Strong: asks why the value is missing and whether the pattern will hold in production.
- Weak: "it's only 2%, drop it" or "fill with the mean and move on".
- Weak: calls it MCAR without testing.

**Example:** (exact numbers from the prompt) Missing group: 4,000 rows, 600 positives (15.0%). Other rows: 196,000, 400 positives (0.204%). The missing group is 2.0% of rows and 60% of positives. A flag alone has AUC 0.791. If the missing rows were scored like normal rows, the model would expect about 8.2 positives there (4,000 x 0.204%) against 600 real. Weak answer: "Drop them, they are only 2%." Strong answer: "That 2% holds 60% of the positives; I keep them, add a missing flag and find out why they are missing."

**Code:**
```python
# Q19: dropping the 2% of rows with a missing key feature (exact counts from the prompt)
import numpy as np
from scipy.stats import chi2_contingency, rankdata
rows, pos = 200_000, 1_000
mis_n, mis_pos = 4_000, 600
obs_n, obs_pos = rows - mis_n, pos - mis_pos
print("observed rows", obs_n, "observed positives", obs_pos); assert obs_n == 196_000 and obs_pos == 400
r_mis, r_obs = mis_pos / mis_n, obs_pos / obs_n
print(f"positive rate: missing {r_mis:.2%}  present {r_obs:.3%}  ratio {r_mis / r_obs:.1f}x")
assert r_mis == 0.15 and round(r_obs, 5) == 0.00204 and round(r_mis / r_obs, 1) == 73.5
print(f"rows dropped {mis_n / rows:.1%}; positives dropped {mis_pos / pos:.0%}")
assert mis_n / rows == 0.02 and mis_pos / pos == 0.6
tab = np.array([[mis_pos, mis_n - mis_pos], [obs_pos, obs_n - obs_pos]])
chi2, p, _, _ = chi2_contingency(tab, correction=False)
print(f"chi-square {chi2:,.0f}, p-value {p:.1e}")
assert p < 1e-100
# missing flag as a single feature
y = np.r_[np.ones(mis_pos), np.zeros(mis_n - mis_pos), np.ones(obs_pos), np.zeros(obs_n - obs_pos)]
flag = np.r_[np.ones(mis_n), np.zeros(obs_n)]
r = rankdata(flag); n1 = y.sum(); n0 = len(y) - n1
auc = (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
tpr, fpr = mis_pos / pos, (mis_n - mis_pos) / (rows - pos)
print(f"AUC of the missing flag alone {auc:.3f}  (TPR {tpr:.2f}, FPR {fpr:.4f}, (1+TPR-FPR)/2 = {(1 + tpr - fpr) / 2:.3f})")
assert abs(auc - (1 + tpr - fpr) / 2) < 1e-9 and auc > 0.78
# what drop does to training and what happens live: share of live positives in missing rows
print(f"after dropping, training positives {obs_pos} of {pos}; but in live traffic 4,000 per 200,000 rows still arrive with the feature missing")
# If we mean-impute and skip the flag, the model cannot tell those rows apart:
print(f"if scored like normal rows, expected positives in the missing group at the normal rate: {mis_n * r_obs:.1f} versus {mis_pos} real")
assert round(mis_n * r_obs, 1) == 8.2
```

**Output (my run):**
```text
observed rows 196000 observed positives 400
positive rate: missing 15.00%  present 0.204%  ratio 73.5x
rows dropped 2.0%; positives dropped 60%
chi-square 17,250, p-value 0.0e+00
AUC of the missing flag alone 0.791  (TPR 0.60, FPR 0.0171, (1+TPR-FPR)/2 = 0.791)
after dropping, training positives 400 of 1000; but in live traffic 4,000 per 200,000 rows still arrive with the feature missing
if scored like normal rows, expected positives in the missing group at the normal rate: 8.2 versus 600 real
```

The p-value prints as 0.0e+00 because it underflows in floating point; read it as "far smaller than 1e-100".

**Follow-ups:**
- Does a significant difference prove MNAR? No. It shows missingness is not MCAR; separating MAR from MNAR needs outside knowledge (how the field is collected) because the data cannot test it.
- What if the flag is an artefact that will disappear? Test with a time split and ask the data owner; if it will disappear, you need other features, and the launch estimate must not rely on the flag.

**Common mistakes:** Dropping rows because they are few. Imputing without a flag. Declaring MCAR. Not checking the live missing rate. Reporting one overall metric that hides the missing group.

### Q20 ⭐⭐ 🟢 In a 300,000-row table, 12,000 rows (4%) hold -999 in the age column, and the income column is stored as text with entries such as 'N/A' and 'null' next to real numbers. A quick model is already trained and works acceptably. Explain how you would find and handle these sentinel and encoding problems, and how you would check whether they affect the model.
**Asked at:** Data-cleaning question banks (an Educative data-science interview data-cleaning lesson, a TechPrep '82 Data Cleaning Interview Questions' page, StrataScratch 'data cleaning traps', a DataCamp cleaning checklist) covering outliers versus errors and unit mismatches; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** -999 and 'N/A' are missing-value codes, not data, so I find them by profiling, turn them into real missing values with flags, refit, and compare against the quick model to see what the bugs were costing.

**Clarifying questions:**
- Does the data dictionary say what -999 means (unknown, not asked, refused)? Why: the meaning decides the flag and the handling.
- Are the missing ages and incomes related to the target or to a data source? Why: informative missingness should be kept as a feature.
- Is the same pipeline used at serving time, with the same coded values? Why: the cleaning must be identical online and offline.
- Which model type is in use? Why: a linear model is damaged by -999 as a number; a tree can accidentally treat it as a separate group.
- Are there other sentinel candidates (0, 9999, '1900-01-01', 'unknown')? Why: the same habit shows up in several columns.

**Approach:**
1. Profile every column: min and max, the most frequent values, counts of values that repeat suspiciously, and a type check. A min of -999 in age, or a mean of -1.43 for a column that should be near 40, tells the story.
2. For text-typed numbers, try a numeric parse with errors turned into missing, then list the tokens that failed (value counts). Here the failures are 'N/A', 'null' and empty strings: nothing else should hide there.
3. Handle explicitly: replace sentinels and tokens with proper missing values, add a missing flag per column, and fill (median fitted on training rows) or use a model that handles missing values natively. Keep the raw column for audit.
4. Check whether missingness carries signal: the target rate among rows with missing age versus present.
5. Put the cleaning in one function used both for training and serving, with tests on a few messy rows.
6. Measure the damage: refit, compare AUC (and coefficients) between the quick model and the cleaned one on a holdout. A small difference is still worth the fix because the quick model is fragile; a large one shows hidden bias.
7. Add checks: schema type checks, an allowed range for age, a count of unparsable tokens per run, and an alert when a new token appears.

**Metrics:**
- Sentinel share = rows equal to the sentinel / rows = 12,000 / 300,000 = 4.0%.
- Unparsable share = rows that fail numeric parsing / rows (income, here 6.03% in the simulation).
- Test AUC of quick model versus cleaned model on the same holdout.
- Coefficient on age versus its true value (simulation only), and the event rate in missing versus present rows.
- Guardrail: rows changed by the cleaning that were not sentinels or known tokens = 0.

**Risks:**
- A -999 left in a numeric column drags a mean to -1.43 and ruins scaling, binning and linear fits.
- A tree model can "work" with -999 by splitting it off, so the bug stays hidden until the encoding changes.
- Filling blanks with 0 turns "unknown" into "zero income".
- Sentinels used in training may differ from those in serving.
- Dropping the 4% rows loses a group with a different event rate.

**What the interviewer scores:**
- Strong: finds the problems by profiling (min, mean, tokens) instead of waiting for model error.
- Strong: converts to real missing values, adds flags, fits the fill on training data only.
- Strong: re-trains and compares, and builds checks into the pipeline.
- Weak: "the model works, leave it."
- Weak: deletes the rows or fills with 0 without checking the effect.

**Example:** (illustrative simulation) 300,000 rows. Age has 12,000 entries of -999 (4.0%), so the mean is -1.43 against 40.14 without them. Income as text: 'N/A' 9,024 rows, 'null' 5,983, empty 3,069, in total 6.03% unparsable. The event rate is 21.3% where age is missing versus 7.7% where it is present, so missing age is informative. The quick model (text coerced, blanks as 0, -999 left in) has test AUC 0.608; the cleaned model with flags has 0.645. The age coefficient is -0.0012 in the quick model and -0.0296 in the cleaned one (true value -0.03). Weak answer: "It works acceptably, so I would not touch it." Strong answer: "I convert the codes to real missing values, add flags, refit and show the AUC and coefficient change; then I add checks."

**Code:**
```python
# Q20: -999 sentinels and text-typed income (illustrative simulation)
import numpy as np, pandas as pd
rng = np.random.default_rng(20)
from scipy.stats import rankdata
def sig(z): return 1 / (1 + np.exp(-z))
def auc(s, y):
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
def fit(X, y, it=30):
    w = np.zeros(X.shape[1])
    for _ in range(it):
        p = sig(X @ w); H = (X * (p * (1 - p))[:, None]).T @ X + 1e-6 * np.eye(len(w))
        w += np.linalg.solve(H, X.T @ (y - p))
    return w
N = 300_000
age = np.clip(rng.normal(40, 12, N), 18, 90).round()
inc = rng.lognormal(np.log(50_000), 0.5, N).round()
age_missing = np.zeros(N, bool); age_missing[rng.choice(N, 12_000, replace=False)] = True   # 4%
logit = -2.5 - 0.03 * (age - 40) - 0.6 * (inc / 50_000 - 1) + 1.2 * age_missing
y = (rng.random(N) < sig(logit)).astype(float)
df = pd.DataFrame({"age": np.where(age_missing, -999, age), "income": inc.astype(int).astype(str)})
bad = rng.random(N)
df.loc[bad < 0.03, "income"] = "N/A"; df.loc[(bad >= 0.03) & (bad < 0.05), "income"] = "null"
df.loc[(bad >= 0.05) & (bad < 0.06), "income"] = ""
# 1. find them: look at extreme values and at what refuses to parse
print("age sentinel rows:", int((df.age == -999).sum()), f"= {(df.age == -999).mean():.1%}")
assert (df.age == -999).sum() == 12_000
print("age min / mean with sentinel:", df.age.min(), round(df.age.mean(), 2), " mean without:", round(df.age[df.age != -999].mean(), 2))
parsed = pd.to_numeric(df.income, errors="coerce")
tokens = df.income[parsed.isna()].replace("", "<empty>").value_counts()
print("income tokens that failed to parse:\n" + tokens.to_string())
assert set(tokens.index) == {"N/A", "null", "<empty>"} and tokens.sum() == parsed.isna().sum()
print(f"income unparsable: {parsed.isna().mean():.2%}")
# 2. handle: explicit NaN + missing flags + median fill (fit on training rows only)
tr = rng.random(N) < 0.7; te = ~tr
age_c = df.age.where(df.age != -999)
inc_c = parsed
def design(clean):
    if clean:
        a_med, i_med = age_c[tr].median(), inc_c[tr].median()
        return np.c_[np.ones(N), age_c.fillna(a_med), inc_c.fillna(i_med) / 1e4, age_c.isna(), inc_c.isna()]
    i_fill = inc_c.fillna(0)                          # the 'quick model': text coerced, blanks to 0, -999 left in
    return np.c_[np.ones(N), df.age, i_fill / 1e4]
res = {}
for name, flag in (("quick (-999 left in)", False), ("cleaned + flags", True)):
    X = design(flag); w = fit(X[tr], y[tr]); res[name] = auc(X[te] @ w, y[te])
    print(f"{name:22} test AUC {res[name]:.3f}")
assert res["cleaned + flags"] > res["quick (-999 left in)"]
# 3. does it matter?  Compare coefficients on age
Xq = design(False); Xc = design(True)
print("age coefficient quick:", round(fit(Xq[tr], y[tr])[1], 4), " cleaned:", round(fit(Xc[tr], y[tr])[1], 4), " (truth -0.03)")
print(f"event rate: age missing {y[age_missing].mean():.1%} vs present {y[~age_missing].mean():.1%}")
assert abs(fit(Xc[tr], y[tr])[1] + 0.03) < 0.005
```

**Output (my run):**
```text
age sentinel rows: 12000 = 4.0%
age min / mean with sentinel: -999.0 -1.43  mean without: 40.14
income tokens that failed to parse:
income
N/A        9024
null       5983
<empty>    3069
income unparsable: 6.03%
quick (-999 left in)   test AUC 0.608
cleaned + flags        test AUC 0.645
age coefficient quick: -0.0012  cleaned: -0.0296  (truth -0.03)
event rate: age missing 21.3% vs present 7.7%
```

**Follow-ups:**
- Tree model, so the sentinel "works"? It still matters: the tree cannot tell -999 from a genuinely low value if the sentinel changes, scaling and linear baselines break, and a flag is clearer. Convert anyway.
- How do you stop a new sentinel next month? A schema contract with allowed ranges and a nightly check for unparsable tokens and values at the range edge, with an alert.

**Common mistakes:** Using the mean or median with the sentinel still in the column. Coercing text to numbers and filling with 0. Not adding a flag. Fitting the fill on all rows. Cleaning in training code but not in serving.

### Q21 ⭐⭐ 🟢 A temperature sensor in a plant shows readings of 850 degrees Celsius for about a minute on 3 of 1,200 machines (0.25%), while normal readings run between 20 and 90. A teammate wants to winsorise them. Explain how you would decide between error and real event, what you would do in each case and what you would record for the downstream owners.
**Asked at:** Data-cleaning question banks (an Educative data-science interview data-cleaning lesson, a TechPrep '82 Data Cleaning Interview Questions' page, StrataScratch 'data cleaning traps', a DataCamp cleaning checklist) covering outliers versus errors and unit mismatches; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** I would not winsorise yet; 850 on a 20 to 90 sensor is either a broken reading or a real emergency, and clipping it to 90 would hide both, so I first test which one it is, then keep the raw value, flag it and tell the owners.

**Clarifying questions:**
- What is the sensor type and its valid range (thermocouple, RTD, gateway scaling)? 850 can be a fault code, a saturation value, or a unit or scaling bug.
- Did any other signal on the same machine move (motor current, pressure, a second temperature probe, alarms)? A real heat event moves other things; a bad sensor does not.
- Is the reading a smooth ramp or an instant jump and an instant return? Physical temperature has inertia; a jump of 790 C in one 10-second step is not physical.
- Did the three machines share a gateway, firmware, time or network segment? A common cause points to the data path, not to the machines.
- Who owns the data and the alarm system, and is there a maintenance or incident log for those minutes? They hold the ground truth.
- What does the downstream model do with this signal (predict failures, control, report)? It decides how costly a wrong call is in each direction.

**Approach:**
1. Do not touch the data yet. Keep the raw value and add a flag column.
2. Test physical plausibility: the maximum rate of change the process can produce, whether the value is exactly constant (850.0 for six readings looks like a fault or sentinel), and the sensor's stated range.
3. Test corroboration: a second sensor, motor current, pressure, alarm log, the operator's note. Disagreement between sensors on the same machine points to a sensor error.
4. Test the pattern: how many machines, which gateway, which minute. Three machines at the same minute and one gateway is a data-path fault.
5. Decide per case. Error: set the value to missing for modelling (not to 90), keep the raw value in an audit column, and do not use it for features. Real event: keep it, do not clip; it is the most important row in the table. Unclear: keep it, flag it, escalate to the plant owner and do not train on that window until answered.
6. Record: raw value, flag, reason code, rule and version used, who decided, affected machines and time range, the treatment, and a note to downstream owners (for example "hourly max is invalid for these machines on this date").
7. Fix upstream: ask the sensor or gateway owner for a fault code instead of a numeric value, and add a range and rate-of-change check to the pipeline.

**Metrics:**
- Share of rows flagged: flagged readings divided by all readings; here 18 of 432,000 in my simulation (0.004%), and 3 of 1,200 machines (0.25%).
- Detector quality against a hand-checked set: precision = flagged readings that are truly errors divided by flagged readings; recall = true errors flagged divided by all true errors. Missing a real event is the costly mistake, so I also track "real events wrongly marked as errors".
- Guardrails: no raw value overwritten, every flag has a reason code, and the alert owner is told within the agreed window.

**Risks:**
- Winsorising at a percentile changes good data. In my run, clipping at the 99th percentile also altered 1.00% of good rows and the hidden spike became a normal-looking 77.4.
- Treating a real overheating event as noise would remove the one event a failure model most needs.
- Dropping rows breaks time continuity for rolling features.
- A fixed cap such as 90 hides alarms from monitoring users who read the same table.
- Single-source evidence: two sensors that fail together (same gateway) can agree on a wrong value.

**What the interviewer scores:**
- Strong: separates "error" from "extreme but real" with evidence (plausibility, corroboration, pattern). Weak: picks a statistical rule (z-score, IQR) as the only test.
- Strong: keeps the raw value and flags it. Weak: overwrites or drops it silently.
- Strong: treats the two cases differently and says what each downstream consumer needs to know. Weak: one treatment for both.
- Strong: asks for an upstream fix (fault codes, range checks). Weak: cleans it in a notebook only.
- Strong: notes that percentile winsorising touches good rows. Weak: "just winsorise at 99%".

**Example:** (illustrative numbers) 1,200 machines, one reading every 10 seconds for one hour (360 per machine, 432,000 rows). Three machines show 850.0 for six readings (about a minute): 18 bad rows, 3 of 1,200 machines = 0.25%. The jump from about 60 to 850 within one step is 79 C per second, against an assumed physical maximum of 5 C per second. With no change in motor current, the triage says "error". The same spike with motor current up 40% says "unclear: escalate", and a smooth ten-minute ramp with motor current up 40% says "real event".
- Weak: "Winsorise at the 99th percentile and move on."
- Strong: "It is physically impossible within one step and nothing else moved, so I mark it as a probable sensor or gateway error, set it to missing for modelling, keep the raw value with a reason code and tell the plant owner. If the current had moved too, I would treat it as real and alert."

**Code:**
```python
# Q21 sensor spike: error or real event? (illustrative numbers)
import numpy as np
rng = np.random.default_rng(21)

machines, hours = 1200, 1
step_s = 10                                   # one reading every 10 s
n = hours * 3600 // step_s                    # 360 readings per machine
base = rng.normal(60, 8, size=(machines, 1)) + rng.normal(0, 1.0, size=(machines, n))
base = np.clip(base, 20, 90)
spike_machines = [101, 640, 1033]
k = 6                                         # about a minute = 6 readings
for m in spike_machines:
    base[m, 100:100 + k] = 850.0
assert len(spike_machines) / machines == 0.0025          # 0.25% of machines
bad = (base > 90).sum()
print("spike rows:", bad, "of", base.size, f"= {bad/base.size:.5%} of rows")
assert bad == 18

# 1) Percentile winsorising: clip at the 99th percentile of all readings
p99 = np.percentile(base, 99)
clipped = np.minimum(base, p99)
changed_good = ((base != clipped) & (base <= 90)).sum()
print(f"p99 = {p99:.1f} C; winsorising also alters {changed_good} GOOD rows ({changed_good/base.size:.2%})")
assert changed_good > 3000
# 850 does become ~p99, so the spike is hidden and the evidence is gone
assert clipped[101, 100] == p99

# 2) Effect of the spike on a 1-hour mean and max feature for a spiked machine
m = 101
print(f"hourly mean raw {base[m].mean():.1f}, clipped {clipped[m].mean():.1f}; hourly max raw {base[m].max():.0f}")
assert base[m].max() == 850

# 3) Triage rule: a physical-plausibility check, not a statistical one
MAX_SLEW = 5.0        # C per second the process can physically change (illustrative)
def triage(series, other_sensor_delta):
    """series: 10 s readings around the event; other_sensor_delta: change on a second sensor (e.g. motor current %)."""
    jump = np.abs(np.diff(series)).max() / step_s
    impossible_slew = jump > MAX_SLEW
    corroborated = abs(other_sensor_delta) > 10
    if impossible_slew and not corroborated:
        return "error (likely sensor/gateway)"
    if corroborated and not impossible_slew:
        return "real event"
    return "unclear: escalate to plant owner"
s = base[101, 95:115]
print("jump rate", round(np.abs(np.diff(s)).max() / step_s, 1), "C/s")
print("no corroboration  ->", triage(s, 0.5))
print("motor current +40% ->", triage(s, 40))
assert triage(s, 0.5).startswith("error")
assert triage(s, 40).startswith("unclear")
# a real overheating event ramps up smoothly and other sensors move with it
ramp = np.concatenate([np.linspace(60, 850, 60), np.full(10, 850.0)])  # 60 readings of 10 s: ~10 min ramp
print("ramp, current +40% ->", triage(ramp, 40))
assert triage(ramp, 40) == "real event"
```

**Output (my run):**
```text
spike rows: 18 of 432000 = 0.00417% of rows
p99 = 77.4 C; winsorising also alters 4302 GOOD rows (1.00%)
hourly mean raw 70.2, clipped 57.3; hourly max raw 850
jump rate 79.3 C/s
no corroboration  -> error (likely sensor/gateway)
motor current +40% -> unclear: escalate to plant owner
ramp, current +40% -> real event
```

**Follow-ups:**
- *What if it is a real event?* Keep and never clip. Tag the window as an incident so training, evaluation and reporting handle it deliberately (for example, include it as a labelled failure example). See Book 1 Part 5 Q24 (statistical outlier detection: z-score, IQR, MAD, when each works and fails) for the detector side.
- *What if you cannot tell?* Keep the raw value, flag as "unclear", exclude that window from training features until the owner answers, and say in the report that this is a decision, not a fact.
- *How do you stop it recurring?* A range and rate-of-change check at ingestion, fault codes instead of numbers, and a per-gateway flagged-rate alert.

**Common mistakes:**
- Winsorising, clipping or dropping before finding out what the value is.
- Using a z-score or IQR as proof of error. A statistic says "unusual", not "wrong".
- Overwriting the raw value, so nobody can undo the call.
- Telling nobody downstream, so a dashboard keeps showing 850.
- Setting the bad value to the median and leaving no flag.

### Q22 ⭐⭐ 🟡 A defect-detection image model has 300 defective images among 100,000 (0.3%), and a teammate wants to replace cross-entropy with focal loss. Another says that class weights are simpler. Explain when focal loss helps, what its parameters do, how you would compare it with the alternatives, and what calibration concerns you would raise.
**Asked at:** Imbalanced-data and fraud-evaluation guides (techinterview.org 'Handling Imbalanced Datasets in Machine Learning', Dataford fraud-evaluation prompts such as 'how do you evaluate a fraud detection model on imbalanced data', a KDnuggets piece on SMOTE misuse, a Coresignal 'class imbalance interview trap' post); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Focal loss down-weights easy examples so the rare hard ones drive the gradient; it can help, but class weights or sampling are simpler, neither is a free fix, and both change the probabilities, so I would compare all three on PR-AUC and recalibrate if the scores must be probabilities.

**Clarifying questions:**
- Is the problem that the model ignores defects, or that it cannot see them (labels, resolution, lighting)? Loss changes do not fix bad data or blur.
- Are the 300 defects one class of defect or several? Rare sub-types need different handling from a single rare class.
- How are defects used: an inspector reviews top flags, or the line is stopped automatically? It sets the metric (precision at a review budget, or recall at a fixed false-alarm rate).
- Do the scores need to be probabilities? If yes, any imbalance trick needs recalibration.
- Is there a clean, untouched validation set with the real 0.3% rate? Without it no comparison is honest.
- How many near-duplicate defect images are there (the same part photographed many times)? Splits must be by part or batch.

**Approach:**
1. Baseline first: plain cross-entropy with a proper split (by part or batch) and PR-AUC, recall at a fixed review budget. Many "imbalance problems" are partly a data or threshold problem.
2. Class weights or balanced mini-batches: cheap, no new hyper-parameter beyond the weight. Try it second.
3. Focal loss: FL = -alpha_t (1 - p_t)^gamma log(p_t), where p_t is the probability given to the true class. With gamma = 2, an easy example at p_t = 0.99 has its loss multiplied by 0.0001, a hard one at p_t = 0.10 by 0.81. Gamma controls how hard easy examples are pushed down; alpha is a class weight inside the same formula.
4. Tune gamma (try 0, 1, 2) and alpha on validation, with several seeds. Report the spread; with 300 positives the differences are often inside the noise.
5. Add the other levers: augmentation of defects, hard-negative mining, a better backbone, more labelled defects. These usually beat the loss choice.
6. Calibration: after weights or focal loss the scores are not probabilities. Recalibrate on a validation set with the real rate (Platt, isotonic, or a simple prior correction) if anything downstream reads them as probabilities.
7. Choose the threshold from the cost of a missed defect versus a false stop, on the validation set, and confirm on the test set once.

**Metrics:**
- PR-AUC (average precision) with the no-skill baseline equal to the positive rate, here 0.3% (300 / 100,000).
- Recall at a fixed precision, or precision at a fixed review budget (for example, the top 1% of images).
- Calibration: mean predicted probability versus observed rate, and a reliability curve or Brier score.
- Guardrails: stability across seeds (standard deviation of PR-AUC), per-defect-type recall.

**Risks:**
- Focal loss with a large gamma can focus on label noise: mislabelled images are the "hardest" examples.
- Probabilities become inflated; a threshold tuned on them will not transfer.
- Tuning on a validation set with only about 60 positives picks noise.
- Weights and focal loss can lower accuracy on the majority while lifting recall; check the false-alarm cost.

**What the interviewer scores:**
- Strong: can write the focal formula, explains gamma and alpha in plain words. Weak: "it handles imbalance".
- Strong: compares against a plain baseline and class weights with the same metric and seeds. Weak: adopts focal loss because it is fashionable.
- Strong: raises calibration and label noise. Weak: reports accuracy.
- Strong: says the loss is one lever among data levers. Weak: only loss.

**Example:** (illustrative numbers) A single easy negative at p_t = 0.99 has cross-entropy loss 0.0101; with focal loss, gamma = 2, it is 0.0000010. In a batch population of 99,700 easy negatives and 300 hard positives (p_t = 0.10), the easy negatives supply 59.2% of the cross-entropy loss but only 0.02% of the focal loss. In my small linear stand-in (not an image model), 70,000 training rows, 30,000 test rows with 86 positives, all three loss choices rank about the same (AP 0.329, 0.324, 0.329 versus a no-skill 0.0029), but the weighted and the focal models predict an average probability of 0.048 and 0.047 against a true rate of 0.0029, while plain cross-entropy stays at 0.0029.
- Weak: "Focal loss is the standard for imbalance, so switch."
- Strong: "Run plain, weighted and focal on the same split and seeds, compare PR-AUC and recall at the review budget, and recalibrate whichever wins."

**Code:**
```python
# Q22 focal loss vs class weights vs plain cross-entropy (illustrative; a linear model stands in for the image model)
import numpy as np
from scipy.optimize import minimize
rng = np.random.default_rng(22)

# 1) What focal loss does to one example (gamma = 2)
gamma = 2.0
def ce(pt): return -np.log(pt)
def fl(pt, g=gamma): return -(1 - pt) ** g * np.log(pt)
easy_neg, hard_pos = 0.99, 0.10             # p_t = probability given to the true class
print(f"CE  easy negative {ce(easy_neg):.4f}, hard positive {ce(hard_pos):.4f}")
print(f"FL  easy negative {fl(easy_neg):.7f}, hard positive {fl(hard_pos):.4f}")
print(f"focal multiplier: easy negative {(1-easy_neg)**gamma:.4f}, hard positive {(1-hard_pos)**gamma:.2f}")
assert abs((1 - easy_neg) ** gamma - 1e-4) < 1e-12
assert abs((1 - hard_pos) ** gamma - 0.81) < 1e-12
# total loss contributed by 99,700 easy negatives versus 300 hard positives
neg_share_ce = 99_700 * ce(easy_neg) / (99_700 * ce(easy_neg) + 300 * ce(hard_pos))
neg_share_fl = 99_700 * fl(easy_neg) / (99_700 * fl(easy_neg) + 300 * fl(hard_pos))
print(f"share of total loss from the 99,700 easy negatives: CE {neg_share_ce:.1%}, FL {neg_share_fl:.2%}")
assert neg_share_ce > 0.55 and neg_share_fl < 0.01

# 2) Small experiment: 100,000 rows, 300 positives (0.3%), 5 features
n, npos = 100_000, 300
y = np.zeros(n, int); y[:npos] = 1
X = rng.normal(size=(n, 5)); X[y == 1] += 1.2
perm = rng.permutation(n); X, y = X[perm], y[perm]
tr = np.arange(n) < 70_000
Xtr, ytr, Xte, yte = X[tr], y[tr], X[~tr], y[~tr]
Xb = lambda A: np.hstack([A, np.ones((len(A), 1))])
sig = lambda z: 1 / (1 + np.exp(-np.clip(z, -30, 30)))

def make_obj(kind):
    def obj(w):
        z = Xb(Xtr) @ w; p = sig(z)
        if kind == "ce":
            wt = np.ones(len(ytr))
            L = -(ytr * np.log(p + 1e-12) + (1 - ytr) * np.log(1 - p + 1e-12))
            g = (p - ytr)
        elif kind == "weighted":
            wt = np.where(ytr == 1, 50.0, 1.0)
            L = -(ytr * np.log(p + 1e-12) + (1 - ytr) * np.log(1 - p + 1e-12)) * wt
            g = (p - ytr) * wt
        else:  # focal
            pt = np.where(ytr == 1, p, 1 - p); pt = np.clip(pt, 1e-12, 1 - 1e-12)
            L = -(1 - pt) ** gamma * np.log(pt)
            dL_dpt = gamma * (1 - pt) ** (gamma - 1) * np.log(pt) - (1 - pt) ** gamma / pt
            g = dL_dpt * pt * (1 - pt) * np.where(ytr == 1, 1, -1)
        return L.mean(), (Xb(Xtr).T @ g) / len(ytr)
    return obj

def ap(y, s):
    o = np.argsort(-s); yy = y[o]
    tp = np.cumsum(yy); prec = tp / np.arange(1, len(yy) + 1)
    return (prec * yy).sum() / yy.sum()

print(f"test rows {len(yte)}, positives {yte.sum()}, no-skill AP = base rate = {yte.mean():.4f}")
res = {}
for kind in ["ce", "weighted", "focal"]:
    w = minimize(make_obj(kind), np.zeros(6), jac=True, method="L-BFGS-B").x
    p = sig(Xb(Xte) @ w)
    res[kind] = (ap(yte, p), p.mean())
    print(f"{kind:9s} AP {res[kind][0]:.3f}   mean predicted prob {p.mean():.4f}   (true rate {yte.mean():.4f})")
# calibration claims
assert abs(res["ce"][1] - yte.mean()) < 0.001            # plain CE keeps probabilities near the base rate
assert res["weighted"][1] > 5 * yte.mean()               # weights inflate probabilities
assert res["focal"][1] > 2 * yte.mean() or res["focal"][1] < yte.mean() / 2   # focal distorts them too (direction printed above)
assert all(v[0] > 5 * yte.mean() for v in res.values())  # all rank far better than no-skill
```

**Output (my run):**
```text
CE  easy negative 0.0101, hard positive 2.3026
FL  easy negative 0.0000010, hard positive 1.8651
focal multiplier: easy negative 0.0001, hard positive 0.81
share of total loss from the 99,700 easy negatives: CE 59.2%, FL 0.02%
test rows 30000, positives 86, no-skill AP = base rate = 0.0029
ce        AP 0.329   mean predicted prob 0.0029   (true rate 0.0029)
weighted  AP 0.324   mean predicted prob 0.0479   (true rate 0.0029)
focal     AP 0.329   mean predicted prob 0.0470   (true rate 0.0029)
```

**Follow-ups:**
- *What does gamma do?* gamma = 0 is ordinary (alpha-weighted) cross-entropy; higher gamma shrinks the loss of well-classified examples faster. Typical tuning range is small (0 to 3).
- *How do you restore probabilities?* Fit isotonic or Platt scaling on a validation set with the true rate, or apply the prior correction in Book 1 Part 3 Q23 (class weighting, SMOTE and undersampling versus calibration). Book 6 Part 3 Q6 covers the class-weight case.
- *When would you skip all of this?* If PR-AUC is fine and a threshold on the plain model meets the review budget, extra machinery adds risk, not value.

**Common mistakes:**
- Reading a small PR-AUC difference between three losses on 300 positives as a real win.
- Using the focal-loss scores as probabilities.
- Ignoring mislabelled defects, which focal loss amplifies.
- Splitting by image instead of by part or batch, so near-identical shots land on both sides.

### Q23 ⭐⭐ 🟡 A screening test for a rare disease is applied to 20,000 patients with a prevalence of 0.5% (100 cases), and your model has sensitivity 90% and specificity 95%. Doctors say that 95% specificity sounds reliable. Explain what share of the positive flags would be true cases, how you would present that, and what you would change in the workflow.
**Asked at:** Imbalanced-data and fraud-evaluation guides (techinterview.org 'Handling Imbalanced Datasets in Machine Learning', Dataford fraud-evaluation prompts such as 'how do you evaluate a fraud detection model on imbalanced data', a KDnuggets piece on SMOTE misuse, a Coresignal 'class imbalance interview trap' post); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** With a prevalence of 0.5%, only about 8% of positive flags are true cases (90 of 1,085), because specificity 95% still produces 995 false alarms among 19,900 healthy patients; so the flag must trigger a confirmatory step, not a diagnosis.

**Clarifying questions:**
- Is 0.5% the prevalence in the people who will be screened, or in a different study population? PPV moves strongly with prevalence.
- What happens after a flag (a second test, a specialist visit, a treatment)? It sets the cost of a false alarm.
- What does a missed case cost compared with a false alarm (delayed treatment, anxiety, an invasive follow-up)? It sets the target sensitivity and specificity.
- Is a cheap and independent second test available? Independence is what makes two-stage testing work.
- Were sensitivity and specificity measured on a population like the screening one, or on a sick-versus-healthy sample that is easier to separate?

**Approach:**
1. Build the 2 by 2 table from the numbers: 100 cases, 19,900 healthy. TP = 90 (sensitivity), FN = 10, FP = 995 (5% of healthy), TN = 18,905.
2. Positive predictive value = TP / (TP + FP) = 90 / 1,085 = 8.3%. Negative predictive value = TN / (TN + FN) = 18,905 / 18,915 = 99.95%.
3. Say it in natural frequencies: "Out of 1,085 flagged people, about 90 are sick and about 995 are fine; about 11 false alarms per true case."
4. Show how PPV moves with prevalence for the same test, so doctors see it is a property of the population as well as the test.
5. Change the workflow: treat the flag as "needs confirmation", add a second test for flagged patients, and give patients wording that matches 8%, not 95%.
6. Check which error matters more and, if needed, move the threshold on a calibrated score, comparing options by the cost of FP and FN.

**Metrics:**
- Sensitivity = TP / (TP + FN) = 90 / 100 = 90%.
- Specificity = TN / (TN + FP) = 18,905 / 19,900 = 95%.
- PPV (precision) = TP / (TP + FP) = 90 / 1,085 = 8.3%.
- NPV = TN / (TN + FN) = 99.95%.
- Workload: flagged per 100,000 screened, and false alarms per true case found.
- Guardrail: a prevalence check on the live population; if it drifts, PPV drifts.

**Risks:**
- Reading specificity as "95% of positives are right". That is the reverse conditional probability.
- Sensitivity and specificity measured on an easy case-control sample overstate real performance.
- Two tests are rarely perfectly independent; the second-stage gain is optimistic when the same patients are hard for both.
- Anxiety, cost and harm from follow-ups of false positives.

**What the interviewer scores:**
- Strong: gets 8.3% quickly and explains with counts. Weak: says "95% accurate".
- Strong: ties PPV to prevalence and shows another prevalence. Weak: treats PPV as fixed.
- Strong: proposes a workflow change (confirmatory test, wording), not just a number. Weak: only calculates.
- Strong: states the independence assumption for a second test. Weak: multiplies without comment.

**Example:** (illustrative numbers) 20,000 patients: 100 cases and 19,900 healthy. The model flags 90 true cases and 995 healthy people, so 1,085 flags and PPV 8.3%. A second independent test with the same sensitivity and specificity, given only to flagged patients, leaves 81 true cases and 49.75 false alarms, so PPV rises to 62.0% while 81 of the 100 cases are still caught (assuming independence). The same test at 10% prevalence would have PPV 66.7%. To reach PPV 50% at 0.5% prevalence you would need specificity of about 99.55%.
- Weak: "95% specificity means 95% of flags are right."
- Strong: "Only about 1 flag in 12 is a real case here; I would use it to select people for a second test, and I would tell patients 'screening positive, needs confirmation'."

**Code:**
```python
# Q23 rare-disease screening: positive predictive value (illustrative)
N, prev, sens, spec = 20_000, 0.005, 0.90, 0.95
cases = round(N * prev); healthy = N - cases
tp = round(cases * sens); fn = cases - tp
fp = round(healthy * (1 - spec)); tn = healthy - fp
print(f"cases {cases}, healthy {healthy}")
print(f"TP {tp}, FN {fn}, FP {fp}, TN {tn}")
ppv = tp / (tp + fp); npv = tn / (tn + fn)
print(f"flagged {tp+fp}; PPV {ppv:.3%}; NPV {npv:.3%}; false alarms per true case {fp/tp:.1f}")
assert (cases, healthy, tp, fn, fp, tn) == (100, 19_900, 90, 10, 995, 18_905)
assert abs(ppv - 90 / 1085) < 1e-12 and round(ppv, 3) == 0.083
assert round(fp / tp, 1) == 11.1

# PPV changes with prevalence (same test)
print("prevalence -> PPV")
for pv in [0.001, 0.005, 0.02, 0.10, 0.30]:
    p = pv * sens / (pv * sens + (1 - pv) * (1 - spec))
    print(f"  {pv:6.1%} -> {p:.1%}")
assert abs(0.10 * sens / (0.10 * sens + 0.90 * 0.05) - 0.667) < 0.001

# Two-stage workflow: only flagged patients get a second, independent test with the same sens/spec
tp2 = tp * sens; fp2 = fp * (1 - spec)
ppv2 = tp2 / (tp2 + fp2)
print(f"after a second independent test: TP {tp2:.1f}, FP {fp2:.2f}, PPV {ppv2:.1%}, cases still caught {tp2:.0f} of {cases}")
assert abs(ppv2 - 81 / 130.75) < 1e-12 and round(tp2, 1) == 81.0
# Specificity needed for PPV 50% at this prevalence
# PPV=0.5 -> FP = TP = 90 -> 90/19900 false positive rate
need_spec = 1 - 90 / healthy
print(f"specificity needed for PPV 50%: {need_spec:.4f}")
assert round(need_spec, 4) == 0.9955
```

**Output (my run):**
```text
cases 100, healthy 19900
TP 90, FN 10, FP 995, TN 18905
flagged 1085; PPV 8.295%; NPV 99.947%; false alarms per true case 11.1
prevalence -> PPV
    0.1% -> 1.8%
    0.5% -> 8.3%
    2.0% -> 26.9%
   10.0% -> 66.7%
   30.0% -> 88.5%
after a second independent test: TP 81.0, FP 49.75, PPV 62.0%, cases still caught 81 of 100
specificity needed for PPV 50%: 0.9955
```

**Follow-ups:**
- *Why does PPV change with prevalence?* Because the number of false alarms scales with the healthy group, which is large when the disease is rare. Book 1 Part 3 Q30 (precision depends on class prevalence; Bayes) works the same idea through Bayes' rule.
- *Would you raise the threshold?* It lifts specificity and PPV but lowers sensitivity, so a missed case rises. I would decide using the cost of each error, on a calibrated score.
- *How do you check the 0.5%?* Confirm in the target screening population; a referral clinic has a higher rate than general screening.

**Common mistakes:**
- Confusing P(positive flag | disease) with P(disease | positive flag).
- Quoting accuracy: with 0.5% prevalence, flagging nobody is 99.5% accurate.
- Using test performance from a balanced research sample for the real population.
- Multiplying two tests' probabilities as if independent without saying so.

### Q24 ⭐⭐ 🟡 An LLM labelled 100,000 support tickets, and a human audit of 500 of them found that the LLM agreed with the humans on 440 (88%), with 45 of its 60 errors in the refund class. The team wants to train a classifier directly on the 100,000 labels. Explain whether and how you would use them, how you would size the audit, and how you would avoid fooling yourself in evaluation.
**Asked at:** AI-era LLM-labelling, weak-supervision and synthetic-data material (an arXiv 2026 abuse-detection paper using LLM annotators, an arXiv survey on LLM-driven synthetic data, an arXiv paper on weak data and model collapse, a Codemia labelling course page); emerging practitioner and research theme, not a confirmed interview staple; search snippets only, not opened
**Say this first (1 line):** I would not train on the 100,000 LLM labels as if they were truth; an 88% match with humans and 45 of 60 errors in one class means the labels are biased, so I would use them as noisy labels, fix or down-weight the refund class with human labels, and evaluate only on a human-labelled test set.

**Clarifying questions:**
- How was the 500 chosen: random, or stratified? A random 500 tells overall agreement but little about rare classes.
- "45 of its 60 errors in the refund class": is that tickets that truly are refund, or tickets the LLM called refund? The first means missed refunds; the second means false refunds. The fix differs.
- How many of the 500 were refund tickets? The error rate inside the class needs that denominator. I assume 100 for the numbers below (illustrative).
- Were the human labels themselves consistent (two annotators, agreement score)? A human error rate caps what the audit can tell us.
- What will the classifier decide (routing, an automatic reply, a refund approval)? It sets how costly refund mistakes are.
- Was the LLM prompted with the same label guidelines the humans use? A guideline mismatch looks like LLM error but is a definition gap.

**Approach:**
1. Treat the 100,000 labels as noisy, not as ground truth. Report agreement overall (88%, 95% interval about 84.9% to 90.6%) and per class.
2. Look at the error structure: 45 of 60 errors (75%) sit in one class. With 100 true refund tickets in the audit that is 55 correct (55%, interval about 45% to 64%) versus 385 of 400 (96.25%) elsewhere. So noise is class-dependent, not random.
3. Spend human effort where it pays: audit more of the refund class and of low-confidence LLM labels; relabel by humans; use a prompt or guideline fix and re-run the LLM on that class; check the rest with a small random audit.
4. Train on LLM labels plus a human-corrected subset; humans win when they disagree; down-weight or drop uncertain LLM labels. A model trained on the LLM labels alone will copy the LLM's mistakes, with the refund class hurt most.
5. Evaluate only against human labels on a held-out set that no LLM label and no tuning touched. Never measure against the LLM's own labels.
6. Size the audit by the quantity you need: for refund accuracy within plus or minus 5 points at 95% confidence you need about 385 refund tickets; at a 20% refund share a random audit would need about 1,925 tickets, so audit refund-heavy strata instead.
7. Keep re-auditing a fresh slice monthly; LLM labelling quality drifts when prompts or models change.

**Metrics:**
- Agreement = tickets where LLM and human agree / audited tickets = 440 / 500 = 88%, with a Wilson 95% interval.
- Per-class agreement (accuracy of LLM labels within each true class), and a confusion matrix showing where refund tickets go.
- Final classifier: macro-F1 and per-class recall on the human test set, with intervals.
- Guardrail: the human test set is drawn independently of the LLM labelling and the LLM never sees it.

**Risks:**
- Evaluating the trained model against LLM labels: a perfect copycat gets 100% there and about 88% against humans.
- Class-dependent noise biases the classifier towards the LLM's blind spots even if overall noise looks tolerable.
- A 500-ticket audit is wide for small classes.
- Humans are not perfect either; adjudicate disagreements.
- Leaking audit tickets into training and then into evaluation.

**What the interviewer scores:**
- Strong: notices the error is concentrated in a class and says why overall 88% hides it. Weak: "88% is good, use all."
- Strong: separates training labels (noisy allowed) from the evaluation labels (human only). Weak: evaluates against LLM labels.
- Strong: sizes the audit from the precision needed per class with a number. Weak: "audit more".
- Strong: proposes a cheap fix loop (prompt change, targeted relabel). Weak: only "get more humans".

**Example:** (illustrative numbers) Audit 500: 440 agree, 60 disagree, 45 of the 60 in refund. If 100 audited tickets are truly refund, the LLM is right on 55 of them (55%) and on 385 of the other 400 (96.25%). A classifier that copies the LLM perfectly agrees with the LLM labels 100% of the time and with humans only 88%. To estimate refund accuracy to plus or minus 5 points you need 385 refund tickets; a random audit at a 20% refund share would need 1,925 tickets.
- Weak: "88% agreement, so train on all 100,000 and evaluate on a held-out 10% of them."
- Strong: "Train on LLM labels with human corrections in the weak class, and evaluate on a separate human-labelled test set with per-class intervals."

**Code:**
```python
# Q24 LLM-labelled tickets: audit sizing and honest evaluation (illustrative; refund share is an assumption)
import math
def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h

audit, agree = 500, 440
err = audit - agree
lo, hi = wilson(agree, audit)
print(f"overall agreement {agree/audit:.1%}, 95% Wilson CI {lo:.1%} to {hi:.1%}; errors {err}")
assert err == 60 and abs(agree / audit - 0.88) < 1e-12 and 0.84 < lo < 0.85 and 0.90 < hi < 0.91

# Assume (illustrative) 100 of the 500 audited tickets truly belong to the refund class
refund_n, refund_err = 100, 45
oth_n, oth_err = audit - refund_n, err - refund_err
print(f"refund: {refund_n-refund_err}/{refund_n} correct = {(refund_n-refund_err)/refund_n:.0%}; others: {oth_n-oth_err}/{oth_n} = {(oth_n-oth_err)/oth_n:.2%}")
rl, rh = wilson(refund_n - refund_err, refund_n)
print(f"refund accuracy 95% CI {rl:.1%} to {rh:.1%}")
assert (oth_n, oth_err) == (400, 15) and abs(refund_err / err - 0.75) < 1e-12
assert (refund_n - refund_err) / refund_n == 0.55

# Audit size for +-5 percentage points on the refund accuracy (worst case p = 0.5)
need_refund_rows = math.ceil(1.96 ** 2 * 0.25 / 0.05 ** 2)
share = refund_n / audit
print(f"refund rows needed {need_refund_rows}; random audit size at {share:.0%} refund share: {math.ceil(need_refund_rows/share):,}")
assert need_refund_rows == 385 and math.ceil(385 / 0.2) == 1925

# A perfect copycat of the LLM labels copies its errors, so against the same humans it scores the LLM's own agreement
copycat_vs_llm, copycat_vs_human = 1.0, agree / audit
print(f"perfect copycat: {copycat_vs_llm:.0%} against LLM labels, {copycat_vs_human:.0%} against human labels")
assert copycat_vs_human == 0.88
```

**Output (my run):**
```text
overall agreement 88.0%, 95% Wilson CI 84.9% to 90.6%; errors 60
refund: 55/100 correct = 55%; others: 385/400 = 96.25%
refund accuracy 95% CI 45.2% to 64.4%
refund rows needed 385; random audit size at 20% refund share: 1,925
perfect copycat: 100% against LLM labels, 88% against human labels
```

**Follow-ups:**
- *Could you use LLM confidence?* Yes as one signal, but check that confidence is calibrated against the audit before filtering on it. Book 1 Part 3 Q40 (evaluating an LLM labeller or judge: metrics, imbalance, agreement, calibration) covers the evaluation side.
- *How big should the human test set be?* Pick the smallest class that matters, decide the interval width you need, and size from that; for 385 refund tickets I get about plus or minus 5 points.
- *What if humans disagree with each other?* Measure human-human agreement; the audit cannot be more accurate than that.

**Common mistakes:**
- Evaluating on LLM labels.
- Reading 88% overall as 88% in every class.
- Auditing at random only, leaving the rare class with too few rows.
- Re-using audit tickets as both training and test data.

### Q25 ⭐⭐ 🟡 A test set of 5,000 documents shows 300 exact matches with training (6%), but a MinHash near-duplicate check flags 1,550 (31%) of the test documents. The model's reported accuracy is 92%. Explain what this does to the reported number, how you would re-evaluate, and how you would stop it recurring.
**Asked at:** Duplicate and leakage guides (a DEV Community post on a train-versus-test dedup gain vanishing, a Voxel51 near-duplicate glossary page, DataEval and Arize leakage pages); commonly reported as a leakage theme in public guides; search snippets only, not opened
**Say this first (1 line):** The 92% is inflated, because 31% of the test documents have a near twin in the training data and the model may simply remember it; I would score the model again on the 3,450 clean documents, report both numbers, and put near-duplicate removal before the split.

**Clarifying questions:**
- What did the MinHash check use (shingle size, similarity threshold)? A loose threshold flags documents that are only similar, not copies.
- Are the near-duplicates the same label as their training twin? Same text with a different label is a different problem (label noise).
- Will production see near-copies of training documents (templates, re-posts)? If yes, part of the 92% is real; if production is genuinely new text, it is not.
- Are the 300 exact matches inside the 1,550 near-duplicates? I assume so (exact match is the limit of near-duplicate).
- Where does the data come from (web crawl, tickets, forms)? It tells me how much template reuse to expect.
- What is accuracy on the flagged subset versus the clean subset? That is the key decomposition.

**Approach:**
1. Confirm the finding: compute the similarity of each test document to its closest training document, and look at a sample of flagged pairs by eye at several thresholds (0.7, 0.8, 0.9).
2. Decompose the reported number. Accuracy = (flagged share x flagged accuracy) + (clean share x clean accuracy). With 4,600 correct out of 5,000 and 98% right on the 1,550 flagged documents (1,519 correct), the clean 3,450 documents have 3,081 correct = 89.3%.
3. Re-evaluate on the deduplicated test set (clean 3,450) with a confidence interval (about plus or minus 1.0 point here), and report the original number as "includes near-duplicates".
4. Decide which number represents production: if live traffic has few near-copies of training documents, quote the clean number; if it has many, quote both and say why.
5. Fix the pipeline: dedupe before splitting; assign near-duplicate clusters (connected components of the MinHash pairs) to the same side of the split; also dedupe the training set so the model does not memorise.
6. Add a gate: a leakage check (share of test documents with a near-neighbour in train above a threshold) that fails the evaluation job.
7. Keep a fresh "never seen" test set going forward (newest documents).

**Metrics:**
- Near-duplicate rate = test documents with a train neighbour above the Jaccard threshold / test documents = 1,550 / 5,000 = 31%.
- Exact-match rate = 300 / 5,000 = 6%.
- Accuracy on clean documents = correct clean / clean documents (3,081 / 3,450 in my example), with a 95% interval.
- Sensitivity table: clean accuracy for the flagged-subset accuracy at 95%, 98%, 100% (90.7%, 89.3%, 88.4% in my run).
- Guardrail: threshold sensitivity; rerun at 0.7, 0.8 and 0.9.

**Risks:**
- Exact-hash dedup misses edited copies; my demo shows a two-word edit breaks the hash but MinHash still scores about 0.95.
- Removing near-duplicates only from the test set changes the test mix; some "twin" documents may genuinely be the production distribution.
- A too-low threshold removes legitimately different documents of the same template and distorts the test set.
- Dedup leaves the training set leaking into later folds if it is done per fold, not globally.

**What the interviewer scores:**
- Strong: decomposes the 92% into flagged and clean parts and recomputes. Weak: "remove duplicates and rerun".
- Strong: knows exact hashing misses near-copies and can describe MinHash and shingles. Weak: only exact match.
- Strong: weighs whether production resembles the duplicates. Weak: assumes always inflated.
- Strong: prevents recurrence by cluster-level splits and a gate. Weak: a one-off fix.

**Example:** (illustrative numbers) 5,000 test documents; 300 exact matches (6%); 1,550 near-duplicate flags (31%); reported accuracy 92% = 4,600 correct. If the model is right on 98% of the flagged documents (1,519), it is right on 3,081 of the 3,450 clean documents, 89.3% (plus or minus 1.0). If the flagged accuracy were only 95%, the clean accuracy would be 90.7%; at 100% it would be 88.4%. A two-word edit changes an exact hash completely, while the MinHash estimate of the Jaccard similarity is 0.949 against a true 0.941.
- Weak: "92% accuracy, ship it."
- Strong: "Re-score on the 3,450 documents with no near twin, report about 89% with an interval, and split by near-duplicate cluster from now on."

**Code:**
```python
# Q25 near-duplicate leakage: MinHash demo and re-evaluation (illustrative numbers)
import hashlib, random
import numpy as np

# 1) The reported accuracy decomposed (invented split of correct answers)
N, exact, near, acc = 5000, 300, 1550, 0.92
print(f"exact {exact/N:.0%}, near-dup {near/N:.0%}, clean docs {N-near}")
assert exact / N == 0.06 and near / N == 0.31 and N - near == 3450
correct = round(N * acc)                     # 4600 correct
acc_near = 0.98                              # assume the model is right on 98% of the near-dups
correct_near = round(near * acc_near)        # 1519
acc_clean = (correct - correct_near) / (N - near)
print(f"correct overall {correct}; near-dup correct {correct_near}; accuracy on clean docs {acc_clean:.1%}")
assert correct == 4600 and correct_near == 1519 and round(acc_clean, 3) == 0.893
# sensitivity: if near-dups are only right 95% of the time
for a in (0.95, 0.98, 1.00):
    print(f"  near-dup accuracy {a:.0%} -> clean accuracy {(correct - near*a)/(N-near):.1%}")

# 2) Exact hashing misses a one-word edit; MinHash does not
def shingles(text, k=3):
    w = text.split(); return {" ".join(w[i:i+k]) for i in range(len(w) - k + 1)}
def jaccard(a, b): return len(a & b) / len(a | b)
rng = random.Random(25)
vocab = [f"w{i}" for i in range(500)]
base = [rng.choice(vocab) for _ in range(200)]
edited = base.copy(); edited[50] = "changed"; edited[120] = "edit"
d1, d2 = " ".join(base), " ".join(edited)
print("exact hash equal:", hashlib.md5(d1.encode()).hexdigest() == hashlib.md5(d2.encode()).hexdigest())
assert hashlib.md5(d1.encode()).hexdigest() != hashlib.md5(d2.encode()).hexdigest()
s1, s2 = shingles(d1), shingles(d2)
true_j = jaccard(s1, s2)
M = 256
P = 2**61 - 1
a = [rng.randrange(1, P) for _ in range(M)]; b = [rng.randrange(0, P) for _ in range(M)]
def sig(S):
    hs = [int(hashlib.md5(x.encode()).hexdigest()[:15], 16) for x in S]
    return np.array([min((ai * h + bi) % P for h in hs) for ai, bi in zip(a, b)])
est = float((sig(s1) == sig(s2)).mean())
print(f"true Jaccard {true_j:.3f}, MinHash estimate ({M} hashes) {est:.3f}")
assert true_j > 0.9 and abs(est - true_j) < 0.08
# an unrelated document
other = " ".join(rng.choice(vocab) for _ in range(200))
est_o = float((sig(s1) == sig(shingles(other))).mean())
print(f"unrelated doc: MinHash estimate {est_o:.3f}")
assert est_o < 0.1

# 3) Uncertainty on the clean-subset accuracy
n = N - near; k = correct - correct_near
p = k / n; half = 1.96 * (p * (1 - p) / n) ** 0.5
print(f"clean accuracy {p:.1%} +- {half:.1%} (95%)")
assert half < 0.011
```

**Output (my run):**
```text
exact 6%, near-dup 31%, clean docs 3450
correct overall 4600; near-dup correct 1519; accuracy on clean docs 89.3%
  near-dup accuracy 95% -> clean accuracy 90.7%
  near-dup accuracy 98% -> clean accuracy 89.3%
  near-dup accuracy 100% -> clean accuracy 88.4%
exact hash equal: False
true Jaccard 0.941, MinHash estimate (256 hashes) 0.949
unrelated doc: MinHash estimate 0.000
clean accuracy 89.3% +- 1.0% (95%)
```

**Follow-ups:**
- *How does MinHash work?* Each document is a set of shingles; for each of many hash functions keep the smallest hash value; the chance that two sets share the same minimum equals their Jaccard similarity, so the share of matching minimums estimates it. Banding (LSH) finds candidate pairs without comparing all pairs.
- *How would you split when documents cluster?* Group by cluster id and use a group split. Book 1 Part 1 Q21 (splitting time-series, grouped or duplicated data and why random k-fold leaks) covers the general principle.
- *Is leakage always bad?* Not if production truly sees near-copies; then report both numbers and say so.

**Common mistakes:**
- Deduplicating with exact hashes only.
- Deleting duplicates from the test set but leaving them in training.
- Reporting one number without saying what the flagged subset does to it.
- Choosing the similarity threshold after seeing which one gives the nicest score.

### Q26 ⭐⭐ 🟡 An app sent a satisfaction survey to 250,000 users and 10,000 replied (a 4% response rate), with a mean score of 4.4 out of 5 among responders. The team wants to train a model to predict satisfaction for all users from these responses. Explain what bias the sample probably has, how you would test for it and what you would do to correct or limit it.
**Asked at:** Delayed-label, positive-unlabelled and selection-bias literature (Bekker and Davis PU survey, an arXiv paper on PU survival data, an arXiv paper on PU data under selection bias); no interview page for the exact prompt, so editor-designed from the literature; search snippets only, not opened
**Say this first (1 line):** A 4% response rate with a mean of 4.4 almost certainly overstates satisfaction, because the people who answer differ from those who do not; I would test that with what I know about both groups, weight if the gap is explained by observed traits, and otherwise limit the claim or run a small follow-up sample.

**Clarifying questions:**
- How were the 250,000 chosen and how was the survey delivered (in-app prompt, email, after a support contact)? The delivery channel shapes who answers.
- What do I know about all 250,000 users (tenure, usage, plan, device, support history)? That is what I can compare and weight on.
- What will the model predict and who will act on it? If it ranks users for outreach, bias matters differently from an average for a dashboard.
- Is there any other satisfaction signal for non-responders (ratings, churn, support tickets)? It lets me check the survey against behaviour.
- Can we contact a random sample of non-responders with an incentive? That is the cleanest bias test.

**Approach:**
1. Name the bias: nonresponse (selection) bias; the responders are a self-selected 4%.
2. Compare responders with the full 250,000 on every observed trait (usage, tenure, plan, region). Large differences mean the sample is not representative on those traits.
3. Model the chance of responding from those traits; if responders are more engaged, weight each response by 1 / response probability (inverse probability weighting), trimming extreme weights.
4. Weighting fixes only differences that the observed traits explain (missing at random given the traits). If people answer because they are especially happy or angry (missing not at random), weighting cannot fix it.
5. Test the remaining gap: contact a random sample of non-responders (for example 600) with an incentive and compare. Combine: overall mean = response rate x responder mean + (1 - response rate) x follow-up mean.
6. If nothing more can be done, give bounds: with 10,000 responders at 4.4 and the other 240,000 anywhere between 1 and 5, the population mean lies between 1.136 and 4.976, which is too wide to use alone, so say it is not identified without assumptions.
7. For the model: train on responders but evaluate against the follow-up sample; report performance by segment; do not present predictions for rarely-responding segments as reliable.

**Metrics:**
- Response rate = responders / invited = 10,000 / 250,000 = 4%; by segment too.
- Standardised difference of each trait between responders and all invited users.
- Weighted mean satisfaction versus raw mean, with effective sample size ((sum of weights) squared / sum of squared weights), since large weights shrink the usable sample.
- Guardrail: follow-up sample result and its interval.

**Risks:**
- Weights built on traits that do not drive response give false comfort.
- Very low response segments produce huge weights.
- A model that predicts the happy responders' behaviour will over-predict satisfaction for everyone.
- Incentivised follow-up responders are not identical to normal responders.

**What the interviewer scores:**
- Strong: names nonresponse bias, separates MAR from MNAR, says what weighting can and cannot do. Weak: "increase the sample".
- Strong: gives a test (compare traits, follow-up sample), not only a name. Weak: opinion only.
- Strong: notes that a bigger count of responses does not remove bias. Weak: "10,000 is plenty".
- Strong: limits claims and states bounds. Weak: reports 4.4 as the app's score.

**Example:** (illustrative simulation) 250,000 users with a hidden true mean of 3.58. Case A: the chance to respond depends on engagement only; 10,217 respond (4.1%) with a mean of 3.86, and weighting by engagement decile gives 3.57. Case B: the chance to respond also depends on satisfaction; 9,580 respond (3.8%) with a mean of 4.31, and the same weighting only gets to 4.13. A random follow-up of 600 non-responders gives an estimate of 3.60. These are simulation numbers, not the prompt's data.
- Weak: "Average score is 4.4, so users are very happy; train on it."
- Strong: "Responders are probably the engaged and the extreme; I would weight on observed traits, check with a random follow-up of non-responders, and report a range."

**Code:**
```python
# Q26 survey nonresponse bias (illustrative simulation tuned to 250,000 users and about 4% response)
import numpy as np
rng = np.random.default_rng(26)
N = 250_000
eng = rng.normal(size=N)                                   # engagement (observable: sessions per week)
sat_true = np.clip(np.round(3.6 + 0.35 * eng + rng.normal(0, 0.9, N)), 1, 5)

def run(label, logit):
    p = 1 / (1 + np.exp(-logit))
    resp = rng.random(N) < p
    return resp

# Case A (MAR): response depends on engagement only
respA = run("A", -3.6 + 1.0 * eng)
# Case B (MNAR): response also depends on satisfaction itself
respB = run("B", -6.55 + 0.8 * eng + 0.75 * sat_true)
for name, resp in [("A response depends on engagement", respA), ("B response also depends on satisfaction", respB)]:
    print(f"{name}: responders {resp.sum():,} ({resp.mean():.1%}), responder mean {sat_true[resp].mean():.2f}, population mean {sat_true.mean():.2f}")

# IPW using only the observable (engagement decile) -> estimate response propensity per bin
def ipw_mean(resp):
    bins = np.digitize(eng, np.quantile(eng, np.linspace(0.1, 0.9, 9)))
    num = den = 0.0
    for b in range(10):
        m = bins == b
        rate = resp[m].mean()
        r = m & resp
        num += (sat_true[r] / rate).sum(); den += (r.sum() / rate)
    return num / den
for name, resp in [("A", respA), ("B", respB)]:
    print(f"case {name}: naive {sat_true[resp].mean():.2f}, engagement-weighted {ipw_mean(resp):.2f}, truth {sat_true.mean():.2f}")
assert abs(ipw_mean(respA) - sat_true.mean()) < 0.05          # MAR: weighting works
assert abs(ipw_mean(respB) - sat_true.mean()) > 0.15           # MNAR: weighting on engagement is not enough
assert sat_true[respA].mean() - sat_true.mean() > 0.2

# Worst-case bounds with the prompt's own numbers: 10,000 responders at 4.4, 240,000 silent users in [1, 5]
lo = (10_000 * 4.4 + 240_000 * 1) / 250_000
hi = (10_000 * 4.4 + 240_000 * 5) / 250_000
print(f"bounds on the population mean without any assumption: {lo:.3f} to {hi:.3f}")
assert (round(lo, 3), round(hi, 3)) == (1.136, 4.976)
# Follow-up sample: 600 randomly chosen non-responders contacted with an incentive
follow = rng.choice(np.where(~respB)[0], 600, replace=False)
rr = respB.mean(); est = rr * sat_true[respB].mean() + (1 - rr) * sat_true[follow].mean()
print(f"double sampling estimate {est:.2f} vs truth {sat_true.mean():.2f}")
assert abs(est - sat_true.mean()) < 0.12
```

**Output (my run):**
```text
A response depends on engagement: responders 10,217 (4.1%), responder mean 3.86, population mean 3.58
B response also depends on satisfaction: responders 9,580 (3.8%), responder mean 4.31, population mean 3.58
case A: naive 3.86, engagement-weighted 3.57, truth 3.58
case B: naive 4.31, engagement-weighted 4.13, truth 3.58
bounds on the population mean without any assumption: 1.136 to 4.976
double sampling estimate 3.60 vs truth 3.58
```

**Follow-ups:**
- *Can you test MNAR from the data?* Not from the responders alone; you need outside information such as a follow-up sample or a behavioural outcome.
- *What about the model?* It can still rank users by relative satisfaction if the bias is roughly uniform, but not estimate the level; check by segment against the follow-up sample.
- *Is the survey useless?* No; it is good for relative comparisons across time within a stable channel and for text feedback, if you say what it represents.

**Common mistakes:**
- Treating the responder mean as the user mean.
- Weighting without checking that the weights are not extreme.
- Believing that more responses from the same channel remove the bias.
- Training a satisfaction model and quoting its mean as a population number.

### Q27 ⭐⭐ 🟡 A credit model trained on 100,000 rows contains only 3,000 rural applicants (3%) but rural applicants are 8% of launch traffic, and the AUC is 0.84 overall but 0.71 for rural applicants. Explain how you would confirm and quantify the gap, what data or modelling steps you would try, and how you would decide whether to launch.
**Asked at:** Splitting and leakage guides (an arXiv paper on panel-data misuse of ML, a LetsDataScience 'science of data splitting' post, a Towards Data Science 'seven common causes of data leakage' article, an APXML recommender-splitting lesson); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** An overall AUC of 0.84 hides a rural AUC of 0.71 on only 3,000 rows, so I would first check that the gap is real with an interval, then try to get more and better rural data, and decide on launch by rural performance against the current process, not by the overall number.

**Clarifying questions:**
- How many rural defaults are in the 3,000 rows? AUC noise depends on the number of positives, not rows. I assume about 6% (186) for the numbers below (illustrative).
- How is "rural" defined and is it available at decision time? It must be a stable, auditable definition.
- Is the lower AUC a weak signal or a different relationship (different features matter)? The remedy differs.
- What do the rural and urban data come from (same sources, same bureau coverage)? Thin credit files in rural areas make features sparse.
- Is there a fairness or regulatory review for geography, which can proxy for protected attributes? That limits what I may change.
- What is the current process for rural applicants and what does a wrong decision cost? A launch rule needs a comparator.

**Approach:**
1. Confirm and quantify: AUC by group with a bootstrap interval, and the interval of the gap. Also calibration by group (does a score of 0.05 mean 5% default in both?), not AUC only.
2. Re-weight to the launch mix: the overall figure is dominated by urban. At 8% rural versus 3%, the overall AUC moves (0.844 to 0.837 in my simulation), small, but the rural risk is bigger than the average suggests.
3. Diagnose: compare feature coverage and distributions; check missingness; fit a rural-only model on the data to see whether a different feature set helps; check for label differences (approved-only data skews rural).
4. Data fixes: collect or buy more rural outcomes, upweight rural rows in training, add features that are informative there, use the shared model plus a rural adjustment (hierarchical or an interaction) rather than a separate tiny model.
5. Model fixes: group-aware calibration, per-group thresholds if policy allows, and a simpler regularised model for the small group.
6. Launch decision: compare rural performance against the incumbent, not against urban. A staged rollout with monitoring on rural default rates, approval rates and calibration, and a pre-agreed rollback trigger.
7. Document: record the known gap, who accepted it and the review date.

**Metrics:**
- AUC per segment = probability that a random default scores above a random non-default in that segment.
- Gap interval from bootstrap; Hanley-McNeil standard error as a sanity check (about 0.022 with 186 defaults).
- Calibration per segment: mean predicted default rate versus observed.
- Business: approval rate and default rate of rural approvals under the new model versus the incumbent.
- Guardrail: urban AUC does not fall.

**Risks:**
- Chasing a gap that is partly noise (few rural defaults).
- Fitting a separate rural model on 3,000 rows that overfits.
- Per-group thresholds can be a legal or fairness problem; geography can proxy for protected traits.
- Approved-only training data hides rejected rural applicants (selection bias).
- Average metrics hide group harm.

**What the interviewer scores:**
- Strong: checks that the gap exceeds noise (an interval) and looks at calibration. Weak: reports AUC alone.
- Strong: re-weights to the launch mix and thinks about positives, not rows. Weak: ignores group counts.
- Strong: offers data and modelling levers with trade-offs. Weak: "collect more data".
- Strong: ties launch to an incumbent comparison and a rollback rule. Weak: blocks or ships based on 0.84.

**Example:** (illustrative simulation) 97,000 urban and 3,000 rural rows. Overall AUC 0.844, urban 0.849, rural 0.716 with 186 rural defaults. Bootstrap 95% interval for the rural AUC is 0.679 to 0.757, and for the gap 0.092 to 0.172, so the gap is real. Resampled to the 8% launch mix, the overall AUC is 0.837. To pin the rural AUC down to a standard error of about 0.01 you would need around 900 rural defaults, roughly 15,000 rural applicants at a 6% rate.
- Weak: "AUC is 0.84, we are fine; rural is a small group."
- Strong: "Rural is 0.71 with an interval of 0.68 to 0.76, 8% of launch traffic. I will check calibration, get more rural data, and launch gated against the incumbent rule for rural."

**Code:**
```python
# Q27 rural subgroup gap in a credit model (illustrative simulation)
import numpy as np
from scipy.stats import rankdata
rng = np.random.default_rng(27)

def auc(y, s):
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)

def make(n, rate, d):
    y = (rng.random(n) < rate).astype(int)
    s = rng.normal(size=n) + d * y            # score = signal + noise; AUC = Phi(d/sqrt2)
    return y, s
# 97,000 urban rows (default rate 5%), 3,000 rural rows (default rate 6%, weaker signal)
yu, su = make(97_000, 0.05, 1.45)
yr, sr = make(3_000, 0.06, 0.62)
y = np.concatenate([yu, yr]); s = np.concatenate([su, sr]); rural = np.r_[np.zeros(97_000, bool), np.ones(3_000, bool)]
a_all, a_u, a_r = auc(y, s), auc(yu, su), auc(yr, sr)
print(f"AUC overall {a_all:.3f}, urban {a_u:.3f}, rural {a_r:.3f}; rural defaults {yr.sum()}")
assert 0.80 < a_all < 0.86 and 0.68 < a_r < 0.75 and a_u - a_r > 0.1

# Bootstrap CI for the rural AUC, and for the gap
B = 400; gaps = []; rurals = []
for _ in range(B):
    i = rng.integers(0, 3_000, 3_000); j = rng.integers(0, 97_000, 97_000)
    ar = auc(yr[i], sr[i]); rurals.append(ar); gaps.append(auc(yu[j], su[j]) - ar)
print(f"rural AUC 95% CI {np.percentile(rurals,2.5):.3f} to {np.percentile(rurals,97.5):.3f}; gap CI {np.percentile(gaps,2.5):.3f} to {np.percentile(gaps,97.5):.3f}")
assert np.percentile(gaps, 2.5) > 0.05                      # the gap is real, not noise

# Re-weight to the launch mix (8% rural) by resampling rows
n_launch = 100_000
iu = rng.integers(0, 97_000, int(n_launch * 0.92)); ir = rng.integers(0, 3_000, int(n_launch * 0.08))
yl = np.concatenate([yu[iu], yr[ir]]); sl = np.concatenate([su[iu], sr[ir]])
print(f"overall AUC at training mix (3% rural) {a_all:.3f}; at launch mix (8% rural) {auc(yl, sl):.3f}")
assert auc(yl, sl) < a_all

# What a rural-only AUC of 0.71 on this many defaults means: Hanley-McNeil standard error
def hm_se(A, n1, n0):
    Q1 = A / (2 - A); Q2 = 2 * A * A / (1 + A)
    return np.sqrt((A*(1-A) + (n1-1)*(Q1-A*A) + (n0-1)*(Q2-A*A)) / (n1 * n0))
print(f"Hanley-McNeil SE for rural AUC with {yr.sum()} defaults: {hm_se(a_r, yr.sum(), len(yr)-yr.sum()):.3f}")
print(f"defaults needed in rural for SE about 0.01: {int(next(n for n in range(100,5000,25) if hm_se(0.71, n, 16*n) < 0.01))}")
assert 0.015 < hm_se(a_r, yr.sum(), len(yr) - yr.sum()) < 0.03
assert next(n for n in range(100, 5000, 25) if hm_se(0.71, n, 16 * n) < 0.01) == 900 and 900 / 0.06 == 15_000
```

**Output (my run):**
```text
AUC overall 0.844, urban 0.849, rural 0.716; rural defaults 186
rural AUC 95% CI 0.679 to 0.757; gap CI 0.092 to 0.172
overall AUC at training mix (3% rural) 0.844; at launch mix (8% rural) 0.837
Hanley-McNeil SE for rural AUC with 186 defaults: 0.022
defaults needed in rural for SE about 0.01: 900
```

**Follow-ups:**
- *Can you just oversample rural?* It can help the model pay attention, but duplicated rows add no new information and distort the probabilities; prefer weights plus recalibration. See Book 1 Part 3 Q10 for where resampling belongs in a pipeline.
- *What about fairness?* Report error rates by group and take the question to the model-risk and compliance owners; do not set per-group rules alone.
- *What if rural is truly harder?* Then the aim is calibrated, honest scores plus a manual-review path, not equal AUC.

**Common mistakes:**
- Quoting overall AUC as the launch metric.
- Ignoring the number of positives in the small group.
- Building a rural-only model from 3,000 rows and calling it fixed.
- Forgetting calibration: equal AUC can still mean wrong risk levels.

### Q28 ⭐⭐ 🟡 A model with 400 labelled rows and 40 positives (10%) gives five-fold CV AUCs between 0.62 and 0.91, and the manager asks if the model is ready. Each fold holds 80 rows with 8 positives. Explain how you would quantify the uncertainty, which procedure you would use to choose a model, and what you would tell the manager.
**Asked at:** Small-data overfitting prompts (Dataford pages such as 'how do you handle overfitting in a model trained on small clinical datasets' and a high-dimensional few-samples prompt); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** No, I would not call it ready; with 8 positives per fold a five-fold AUC range of 0.62 to 0.91 is what pure noise produces, so I would report an interval for the pooled AUC, choose models with repeated or nested cross-validation, and tell the manager what extra data would settle it.

**Clarifying questions:**
- What decision will the model drive and what is the simplest alternative (a rule, a logistic model)? "Ready" means better than the alternative, not an AUC value.
- Are the 400 rows independent (one per customer) or grouped (several per customer or site)? Grouped rows need grouped folds, or the AUC is inflated.
- How many models and hyper-parameters were tried on these 400 rows? Selection on the same folds inflates the score.
- Can we get more labelled rows, and at what cost and time? That decides between "wait" and "ship with a guardrail".
- What error would hurt most (a missed positive or a false alarm)? It gives the metric beyond AUC.

**Approach:**
1. Explain the spread: each fold has 8 positives and 72 negatives, so each fold AUC rests on 8 x 72 = 576 positive-negative pairs, and one positive moving from above every negative to below every negative shifts the fold AUC by 1/8 = 0.125.
2. Quantify uncertainty: pooled out-of-fold AUC over all 400 rows, with a bootstrap confidence interval (resampling rows, or patients if grouped).
3. Repeated stratified cross-validation (for example 5-fold, repeated 10 times) smooths the split noise, but it does not remove the noise of having only 40 positives; say so.
4. Select models with nested cross-validation (inner loop picks, outer loop scores) or a very small search space; keep the final model simple and regularised.
5. Compare with a baseline (a simple model or the current rule) using the same folds and a paired comparison; a model must beat the baseline by more than the noise.
6. Be honest in the answer: "The best guess is an AUC near 0.76 and the plausible range is about 0.65 to 0.85; that is not enough to promise a gain."
7. Suggest what would help: more positives, a pilot or shadow run, or a decision rule that is robust to this uncertainty.

**Metrics:**
- AUC = probability a random positive is scored above a random negative.
- Pooled out-of-fold AUC with a 95% bootstrap interval; fold range as a diagnostic only.
- The standard error of the pooled AUC depends mainly on the positive count: about 0.04 for 40 positives at an AUC near 0.76 (standard deviation 0.039 across simulated datasets).
- Secondary: precision at a review budget, calibration slope and intercept.
- Guardrail: no model-selection step touches the outer test folds.

**Risks:**
- Choosing the best of many models using the same five folds inflates the result.
- Repeating the CV many times looks like more data but is not.
- Row-level folds on grouped data leak.
- Reporting the best fold or the mean without an interval.
- Preprocessing (scaling, feature selection) fitted before the splits.

**What the interviewer scores:**
- Strong: connects the fold spread to the 8 positives and says what it implies. Weak: "the model is unstable".
- Strong: gives an interval for pooled AUC and knows repeating CV does not shrink it. Weak: "run more folds".
- Strong: separates selection from estimation (nested CV). Weak: tunes on the CV score and reports it.
- Strong: gives the manager a plain verdict and next step. Weak: a technical lecture.

**Example:** (illustrative simulation) Scores drawn so the true AUC is 0.76; 400 rows, 40 positives. Over 2,000 simulated datasets the five fold AUCs spread by a median of 0.20 (max minus min), and a spread of 0.29 or more, as in the prompt, appears in 13.6% of datasets. The pooled AUC has a standard deviation of 0.039 across datasets. On one dataset, 50 repeats of 5-fold CV change the mean-of-folds AUC by only 0.0045, but the bootstrap 95% interval for the pooled AUC is 0.71 to 0.85 (width 0.14). So repeats make the number steadier without making it more certain.
- Weak: "Mean CV AUC is 0.76, ship it."
- Strong: "About 0.76 with an interval of roughly 0.71 to 0.85, from only 40 positives. I would run a shadow period or get more labels before committing."

**Code:**
```python
# Q28 400 rows, 40 positives: how noisy is 5-fold AUC? (illustrative; fixed scores isolate the evaluation noise)
import numpy as np
from scipy.stats import rankdata, norm
rng = np.random.default_rng(28)
def auc(y, s):
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
d = 1.0                              # binormal shift: AUC = Phi(d/sqrt(2))
true_auc = norm.cdf(d / np.sqrt(2))
print(f"true AUC of the scoring rule: {true_auc:.3f}")

def one_dataset():
    y = np.r_[np.ones(40, int), np.zeros(360, int)]
    s = rng.normal(size=400) + d * y
    return y, s
def stratified_folds(y):
    pos = rng.permutation(np.where(y == 1)[0]); neg = rng.permutation(np.where(y == 0)[0])
    return [np.r_[pos[k::5], neg[k::5]] for k in range(5)]

# Part 1: spread of the 5 fold AUCs on one dataset, repeated over many datasets
ranges = []; pooled = []
for _ in range(2000):
    y, s = one_dataset()
    f = [auc(y[i], s[i]) for i in stratified_folds(y)]
    ranges.append(max(f) - min(f)); pooled.append(auc(y, s))
ranges = np.array(ranges); pooled = np.array(pooled)
print(f"fold size 80 with 8 positives; median (max-min) of 5 fold AUCs {np.median(ranges):.2f}; share of datasets with a spread >= 0.29: {np.mean(ranges >= 0.29):.1%}")
print(f"pooled AUC over all 400 rows: mean {pooled.mean():.3f}, sd across datasets {pooled.std():.3f}")
assert np.median(ranges) > 0.18
assert 0.03 < pooled.std() < 0.05
# Part 2: repeating the CV many times removes split noise but not the noise of having 400 rows
y, s = one_dataset()
rep = [np.mean([auc(y[i], s[i]) for i in stratified_folds(y)]) for _ in range(50)]
print(f"one dataset, 50 repeats of 5-fold: mean-of-folds AUC varies only {np.std(rep):.4f}; pooled AUC {auc(y,s):.3f}")
# Part 3: bootstrap CI for the pooled AUC on that dataset
bs = []
for _ in range(2000):
    i = rng.integers(0, 400, 400)
    if y[i].sum() in (0, 400): continue
    bs.append(auc(y[i], s[i]))
lo, hi = np.percentile(bs, [2.5, 97.5])
print(f"bootstrap 95% CI for the pooled AUC: {lo:.2f} to {hi:.2f} (width {hi-lo:.2f})")
assert hi - lo > 0.1
assert np.std(rep) < 0.02

assert 8 * 72 == 576 and 1 / 8 == 0.125
```

**Output (my run):**
```text
true AUC of the scoring rule: 0.760
fold size 80 with 8 positives; median (max-min) of 5 fold AUCs 0.20; share of datasets with a spread >= 0.29: 13.6%
pooled AUC over all 400 rows: mean 0.761, sd across datasets 0.039
one dataset, 50 repeats of 5-fold: mean-of-folds AUC varies only 0.0045; pooled AUC 0.787
bootstrap 95% CI for the pooled AUC: 0.71 to 0.85 (width 0.14)
```

**Follow-ups:**
- *Why does repeated CV not fix it?* It reuses the same 400 rows; the sampling noise from having 40 positives stays.
- *Which model type?* A regularised linear model or a shallow tree; with 40 positives, complex models mostly fit noise. Book 1 Part 1 Q5 (cross-validation: k, how it works, when it fails) and Q23 (nested cross-validation) cover the mechanics.
- *How do you compare two models?* A paired bootstrap of the AUC difference on the same rows; see Book 1 Part 3 Q35 (comparing classifiers statistically).

**Common mistakes:**
- Reading the best fold as the model's ability.
- Tuning on the folds and then quoting the same folds' score.
- Treating "mean +- sd of five folds" as a confidence interval.
- Telling a manager "ready" or "not ready" without giving a range.

### Q29 ⭐⭐ 🟡 Only the 20,000 of 1,000,000 transactions (2%) flagged by old rules were reviewed by investigators, and 1,500 of them (7.5%) were confirmed as fraud, while the other 980,000 are treated as legitimate in the training table. The team wants to train a new model on this table. Explain what is wrong with the labels, how this is a positive-unlabelled problem, and how you would get an honest evaluation.
**Asked at:** Delayed-label, positive-unlabelled and selection-bias literature (Bekker and Davis PU survey, an arXiv paper on PU survival data, an arXiv paper on PU data under selection bias); no interview page for the exact prompt, so editor-designed from the literature; search snippets only, not opened
**Say this first (1 line):** The label "not fraud" on the 980,000 unreviewed rows really means "never looked at"; only rule-flagged rows ever get a label, so a model trained on this table learns to copy the old rules, and I need a small random audit to get honest labels and honest evaluation.

**Clarifying questions:**
- How exactly does the rule set choose what gets reviewed (a score cut-off, many rules, random sampling too)? If rows outside the rules never get reviewed, those frauds are invisible.
- Is any random or exploratory sample reviewed (even 0.1%)? It is the only unbiased label source.
- How are customer complaints and chargebacks used? They label some unreviewed fraud late and give a second, independent source.
- What is the review capacity per month? It limits how many new labels we can buy.
- Do fraud patterns change as the rules change (adversaries avoid the rules)? Then old labels go stale.
- What will the new model be used for: replace the rules, or find what the rules miss? The second needs labels beyond the rules.

**Approach:**
1. Say what the label is: positive = reviewed and confirmed (1,500 of 20,000 reviewed, 7.5%); everything else is unlabelled, mostly negative but not known to be. This is a positive-unlabelled (PU) setting, and the labelling is selected by the old rules, not at random.
2. Estimate what is hidden with a random audit of the unreviewed rows. Illustrative result: 9 frauds in 3,000 audited rows (0.30%, 95% interval about 0.10% to 0.50%) implies about 2,940 hidden frauds among the 980,000, so the old rules caught only about 33.8% of all fraud (1,500 of 4,440).
3. Do not use the standard PU shortcut blindly: methods that assume positives are labelled at random (a constant labelling chance) fail here because the chance of being labelled is 0 outside the rules.
4. Build training labels from the reviewed rows plus the audit sample, weighting audit rows by 1 / sampling probability (here 980,000 / 3,000 = about 327 each). Add later chargebacks and complaints as extra positive labels.
5. Keep a standing small random review (for example 0.1% of traffic) so there is always an unbiased slice for training and testing.
6. Evaluate on the random audit sample, not on the reviewed rows: report recall at the review budget and precision from audited rows, with intervals. Compare the new model with the old rules on the same audit.
7. Roll out as challenger on unreviewed traffic, sending a sample of its high scorers to review, to learn from what it finds.

**Metrics:**
- Precision of old rules = confirmed / reviewed = 1,500 / 20,000 = 7.5%.
- Estimated recall of old rules = confirmed / (confirmed + estimated hidden frauds) = 1,500 / 4,440 = 33.8% (illustrative audit).
- Model recall at a fixed review share (for example the top 2%) on the random audit sample, with a bootstrap interval.
- Guardrail: the audit sample is drawn before scoring and never used for training.

**Risks:**
- A model that learns the rules scores well on reviewed rows and finds nothing new.
- Frauds that look different from the rule's patterns never appear as positives.
- A tiny audit gives wide intervals for a rare rate.
- Feedback loops: the new model's flags determine the next labels.
- Treating unreviewed rows as negative inflates apparent precision and recall of rule-like models.

**What the interviewer scores:**
- Strong: names selection by the old rules, says "negative" means "unlabelled", explains why PU assumptions break. Weak: "class imbalance".
- Strong: asks for a random audit and weights it. Weak: "use anomaly detection and skip labels".
- Strong: evaluates on random rows. Weak: evaluates on reviewed rows.
- Strong: quantifies hidden fraud from an audit. Weak: guesses.

**Example:** (illustrative) 1,000,000 transactions; 20,000 reviewed; 1,500 confirmed (7.5%). A random audit of 3,000 unreviewed rows finds 9 frauds: 0.30%, so about 2,940 hidden frauds, and the old rules' recall is about 33.8%. In my simulation (400,000 rows, rule flags the top 2% on one feature), only 436 of 4,028 true frauds (10.8%) are ever confirmed. A model trained on those labels puts a weight of 3.24 on the rule's own feature versus 0.99 with true labels, and on a random audit of 20,000 rows it catches 24.5% of the frauds in its top 2% versus 36.2% for a model trained on the true labels.
- Weak: "Treat unreviewed as non-fraud, train XGBoost, report AUC on a holdout of the same table."
- Strong: "Positives are only what the rules surfaced. I would buy a small random audit, weight it, and measure recall on that audit, not on the reviewed rows."

**Code:**
```python
# Q29 only rule-flagged transactions were reviewed: positive-unlabelled labels (illustrative simulation)
import numpy as np
from scipy.optimize import minimize
rng = np.random.default_rng(29)

# 1) Arithmetic from the prompt
total, reviewed, confirmed = 1_000_000, 20_000, 1_500
print(f"reviewed share {reviewed/total:.1%}; confirmed precision of the old rules {confirmed/reviewed:.1%}; unreviewed rows {total-reviewed:,}")
assert reviewed / total == 0.02 and confirmed / reviewed == 0.075 and total - reviewed == 980_000
# A random audit of 3,000 unreviewed transactions (illustrative result: 9 frauds)
audit_n, audit_hit = 3_000, 9
r = audit_hit / audit_n
hidden = r * (total - reviewed)
print(f"audit fraud rate in unreviewed {r:.2%} -> about {hidden:,.0f} hidden frauds; recall of the old rules about {confirmed/(confirmed+hidden):.1%}")
assert abs(hidden - 2_940) < 1e-6 and round(confirmed / (confirmed + hidden), 3) == 0.338
print(f"weight per audited row {(total-reviewed)/audit_n:.0f}")
assert round((total - reviewed) / audit_n) == 327
need_n = 1.96 ** 2 * 0.003 * 0.997 / 0.001 ** 2
print(f"audited rows needed for +-0.1 points at a 0.3% rate: {need_n:,.0f}")
assert 11_400 < need_n < 11_600
half = 1.96 * (r * (1 - r) / audit_n) ** 0.5
print(f"audit rate 95% interval about {r-half:.2%} to {r+half:.2%}")

# 2) Simulation: train on 'reviewed-and-confirmed = 1, everything else = 0' versus on the true labels
n = 400_000
x1 = rng.normal(size=n); x2 = rng.normal(size=n); x3 = rng.normal(size=n)
logit = -6.2 + 1.0 * x1 + 1.3 * x2 + 0.9 * x3
fraud = rng.random(n) < 1 / (1 + np.exp(-logit))
flagged = x1 > np.quantile(x1, 0.98)                    # old rule: top 2% on x1 only
observed = fraud & flagged                              # only flagged rows are ever confirmed
print(f"true frauds {fraud.sum()}, confirmed {observed.sum()} ({observed.sum()/fraud.sum():.1%} of all frauds); precision of rule {observed.sum()/flagged.sum():.1%}")
X = np.c_[x1, x2, x3, np.ones(n)]
def fit(y):
    f = lambda w: (np.mean(np.logaddexp(0, X @ w) - y * (X @ w)), X.T @ (1 / (1 + np.exp(-(X @ w))) - y) / n)
    return minimize(f, np.zeros(4), jac=True, method="L-BFGS-B").x
w_naive, w_true = fit(observed.astype(float)), fit(fraud.astype(float))
print("coefficients (x1, x2, x3): naive", np.round(w_naive[:3], 2), "| true labels", np.round(w_true[:3], 2))
assert w_naive[0] > 2.5 * w_true[0]          # the naive model leans on the old rule's own feature

# Honest test: a random audit of 20,000 rows labelled with the true outcome; review budget = top 2%
audit = rng.choice(n, 20_000, replace=False)
def recall_at(w, idx, y, share=0.02):
    s = X[idx] @ w; k = int(share * len(idx)); top = np.argsort(-s)[:k]
    return y[idx][top].sum() / y[idx].sum()
print(f"random audit: recall in top 2%: naive model {recall_at(w_naive, audit, fraud):.1%}, true-label model {recall_at(w_true, audit, fraud):.1%}")
# naive evaluation: only judged on observed labels (reviewed rows) looks much better
rev = np.where(flagged)[0]
s_n = X[rev] @ w_naive
print(f"naive evaluation on the reviewed rows only: share of confirmed frauds in naive top 50%: {observed[rev][np.argsort(-s_n)[:len(rev)//2]].sum()/observed[rev].sum():.1%}")
assert recall_at(w_true, audit, fraud) > recall_at(w_naive, audit, fraud) + 0.05
```

**Output (my run):**
```text
reviewed share 2.0%; confirmed precision of the old rules 7.5%; unreviewed rows 980,000
audit fraud rate in unreviewed 0.30% -> about 2,940 hidden frauds; recall of the old rules about 33.8%
weight per audited row 327
audited rows needed for +-0.1 points at a 0.3% rate: 11,490
audit rate 95% interval about 0.10% to 0.50%
true frauds 4028, confirmed 436 (10.8% of all frauds); precision of rule 5.5%
coefficients (x1, x2, x3): naive [3.24 1.21 0.9 ] | true labels [0.99 1.27 0.89]
random audit: recall in top 2%: naive model 24.5%, true-label model 36.2%
naive evaluation on the reviewed rows only: share of confirmed frauds in naive top 50%: 91.1%
```

**Follow-ups:**
- *What does PU theory say?* If positives are labelled completely at random, you can estimate the labelling rate and correct; here the labelling depends on features (the rules), so it does not apply directly. Book 1 Part 3 Q46 (PU learning and noisy labels) gives the textbook case, and Book 6 Part 3 Q14 covers the related reject-inference problem in lending.
- *How big should the audit be?* To estimate a rate near 0.3% within plus or minus 0.1 points at 95% confidence I need about 11,500 audited rows; a stratified audit by model score needs far fewer.
- *Could you use anomaly detection?* It can propose candidates to review, but it still needs reviewed labels for evaluation.

**Common mistakes:**
- Calling the unreviewed rows negatives.
- Evaluating on the reviewed subset.
- Applying the PU "constant labelling rate" correction when selection depends on the rules.
- Never reviewing rows the rules ignore, so the blind spot stays blind.

### Q30 ⭐⭐ 🟡 A nightly pipeline normally loads 5,000,000 rows, yesterday it loaded 3,100,000 (62% of the usual) and the model retrained on it without anyone noticing. You are asked to design data-quality gates. Explain which checks you would block on and which you would only warn on, how you would set thresholds, and what happens when a gate fails.
**Asked at:** Data-quality-gate material (a OneUptime 2026 data-pipeline validation post, a DesignGurus Great Expectations answer, an MLJourney post on quality checks for ML, a Pebblous Great Expectations report); practitioner posts rather than interview banks, so scenario is partly editor-designed; search snippets only, not opened
**Say this first (1 line):** I would put a small set of hard gates in front of training, that block the run when the data is clearly wrong (a 38% row-count drop, a broken schema, null keys), and softer warn-level checks for drift, with thresholds set from history and a defined path for what happens when a gate fails.

**Clarifying questions:**
- Why did 3,100,000 rows arrive instead of 5,000,000: an upstream outage, a late partition, a filter change, or a genuine business drop? It decides whether the right response is wait, backfill or accept.
- How does the usual count vary by weekday, month end and campaigns? Thresholds must use the same-weekday pattern, or they will fire on every Sunday.
- What does the retrained model feed (a live scorer, a report) and how costly is a bad model for a day? It sets how strict the blocking gates are.
- Can the previous model keep serving if tonight's retrain is blocked? A safe fallback makes strict gates cheap.
- Who owns the upstream table and who is on call? A gate with nobody to notify is useless.
- Are there labels in this load, and how late do they arrive? Label-rate checks differ for delayed labels.

**Approach:**
1. Gate placement: run checks after load and before training, on the batch as a whole and per partition; store the result as a record next to the run.
2. Block (the data is wrong or incomplete, so a model on it is not trustworthy):
   - Row count below a limit set from history: compare with the median of the last four same weekdays; block below 90% (yesterday: 62%, ratio about 0.60 in my run).
   - Schema: missing, renamed or retyped columns; wrong partition date; stale data (freshness).
   - Null rate of key and label columns above a hard limit; duplicate primary keys above a limit.
3. Warn (investigate, still run): moderate row-count drop (90% to 97% or above 110%), positive-rate outside its usual band, drift of a top feature (PSI above 0.10), a category appearing or disappearing, null rate rising but under the limit.
4. Set thresholds from history: take 8 to 12 weeks, same weekday, run the gate on each past night, count the false alarms, and choose limits so normal nights pass (in my run: 30 of 30 normal nights passed and the 62% night was blocked). Revisit quarterly.
5. When a gate fails: stop the retrain; keep the last good model serving; quarantine the batch (do not delete); page the data owner with the failing check, value and limit; auto-retry when the partition is fixed; an override needs a named person and a written reason.
6. Record every decision (checks, values, thresholds, pass or fail, who overrode) so the history can tune thresholds later.
7. Test the gates: replay yesterday's bad load as a regression test, and inject synthetic failures regularly.

**Metrics:**
- Row-count ratio = rows tonight / median of last four same-weekday loads; yesterday = 3,100,000 / 5,000,000 = 62% of the usual (against the same-weekday median it was 0.60 in my simulated history).
- Gate false-block rate = blocked normal nights / normal nights (target close to zero), and detection rate = injected faults blocked / injected faults.
- Time from failure to owner notified; share of blocked runs recovered within the agreed window.
- Guardrail: blocking checks are few and each one has an owner.

**Risks:**
- Too many blocking gates teach the team to override them.
- A static threshold ignores weekday and month-end patterns, and fires every Sunday (a normal Sunday at 4,500,000 rows is already z = -1.7 against a plain 30-day mean).
- Count checks do not see wrong content: the right number of rows with shifted labels or units still passes. Those need distribution and label gates.
- A gate that blocks with no fallback can stop a business-critical model.
- Overriding without a record.

**What the interviewer scores:**
- Strong: separates block from warn with a reason for each and uses same-weekday baselines. Weak: one fixed row-count threshold, or "alert on everything".
- Strong: defines the failure path (stop, keep the last model, quarantine, notify, override rule). Weak: "send an alert".
- Strong: sets thresholds from history and measures false alarms. Weak: round numbers.
- Strong: notes that rule-based gates miss label and content problems. Weak: believes row counts are enough.

**Example:** (illustrative history) Normal nights run near 5,000,000 rows with a weekend dip to about 90% to 92%. The gate compares each night with the median of the last four same weekdays; it blocks below 0.90, warns between 0.90 and 0.97, and also above 1.10. On 30 normal nights: 30 pass. Yesterday's night, 3,100,000 rows (62% of the usual), scores 0.60 and is blocked; a 7% short night warns. A z-score on the last 30 nights flags the bad night at -7.2, but it also gives a normal Sunday z = -1.7, which is the seasonality problem.
- Weak: "Alert if the row count looks low."
- Strong: "Block at 90% of the same-weekday median, warn at 97%, check schema, keys and label rate, keep the last good model serving, quarantine the batch and page the owner."

**Code:**
```python
# Q30 data-quality gates for a nightly load (illustrative history)
import numpy as np
rng = np.random.default_rng(30)

print(f"yesterday {3_100_000/5_000_000:.0%} of the usual 5,000,000 rows")
assert 3_100_000 / 5_000_000 == 0.62

# 60 nights of history with a weekday pattern and noise
days = 60
dow = np.arange(days) % 7
weekday_factor = np.array([1.00, 1.02, 1.03, 1.02, 1.00, 0.92, 0.90])
hist = (5_000_000 * weekday_factor[dow] * rng.normal(1, 0.012, days)).astype(int)

def expected(hist, dow_hist, d):
    same = hist[dow_hist == d][-4:]                       # last 4 same-weekday nights
    return np.median(same)

def row_gate(count, d, hist=hist, dow_hist=dow):
    exp = expected(hist, dow_hist, d); ratio = count / exp
    if ratio < 0.90: return "BLOCK", ratio
    if ratio < 0.97 or ratio > 1.10: return "WARN", ratio
    return "PASS", ratio

# False-alarm check: run the gate on each of the last 30 nights using only earlier history
res = {"PASS": 0, "WARN": 0, "BLOCK": 0}
for t in range(30, days):
    g, _ = row_gate(hist[t], dow[t], hist[:t], dow[:t]); res[g] += 1
print("gate on 30 normal nights:", res)
assert res["BLOCK"] == 0 and res["PASS"] >= 28

# Yesterday's bad load: a Wednesday-like night (dow=2) with 3.1M rows
g, ratio = row_gate(3_100_000, 2)
print(f"bad night: {g}, ratio to same-weekday median {ratio:.2f}")
assert g == "BLOCK"
# The usual std-dev style rule on the last 30 nights (no weekday adjustment)
mu, sd = hist[-30:].mean(), hist[-30:].std()
print(f"naive z-score of the bad night: {(3_100_000-mu)/sd:.1f}; but a perfectly normal Sunday (about 4,500,000 rows) already scores z = {(4_500_000-mu)/sd:.1f}")
# A 7% hole on a normal night: warn only
g2, r2 = row_gate(int(0.93 * expected(hist, dow, 3)), 3)
print(f"7% short night: {g2} (ratio {r2:.2f})")
assert g2 == "WARN"

# Other gates as a table-driven check on a batch summary
batch = {"schema_ok": True, "null_rate_key": 0.0004, "dup_key_rate": 0.0, "partition_date_ok": True, "pos_rate": 0.081, "psi_top_feature": 0.14}
rules = [("schema_ok", lambda v: v, "BLOCK"), ("partition_date_ok", lambda v: v, "BLOCK"),
         ("null_rate_key", lambda v: v < 0.001, "BLOCK"), ("dup_key_rate", lambda v: v < 0.001, "BLOCK"),
         ("pos_rate", lambda v: 0.07 <= v <= 0.09, "WARN"), ("psi_top_feature", lambda v: v < 0.10, "WARN")]
out = [(k, sev) for k, f, sev in rules if not f(batch[k])]
print("failed rules:", out)
assert out == [("psi_top_feature", "WARN")]
```

**Output (my run):**
```text
yesterday 62% of the usual 5,000,000 rows
gate on 30 normal nights: {'PASS': 30, 'WARN': 0, 'BLOCK': 0}
bad night: BLOCK, ratio to same-weekday median 0.60
naive z-score of the bad night: -7.2; but a perfectly normal Sunday (about 4,500,000 rows) already scores z = -1.7
7% short night: WARN (ratio 0.93)
failed rules: [('psi_top_feature', 'WARN')]
```

**Follow-ups:**
- *How do you gate label problems?* A label-rate band per batch plus a comparison with the previous batches; see Book 6 Part 3 Q48 for the labelling-vendor drift case.
- *What if the drop is real (a holiday)?* A calendar feature in the expected count, or an override with a reason; the log shows how often that happens.
- *Which tools?* Any of the common validation libraries or plain SQL and Python checks; the design (block versus warn, owner, fallback) matters more than the tool.

**Common mistakes:**
- Fixed thresholds with no weekday adjustment.
- Making everything blocking, then disabling gates after a few false alarms.
- Failing the job without telling anyone or without a fallback model.
- Checking counts and schema but never the label or the distribution.

### Q31 ⭐⭐ 🟡 A customer-level feature called spend_30d was computed with a window that sometimes extends up to 15 days after the prediction date, and the churn model's offline AUC is 0.91 against 0.77 live. The feature team says the window is just a rolling aggregate. Explain how you would prove the leak, how you would rebuild features with point-in-time correctness, and how you would check the rest of the feature set.
**Asked at:** Splitting and leakage guides (an arXiv paper on panel-data misuse of ML, a LetsDataScience 'science of data splitting' post, a Towards Data Science 'seven common causes of data leakage' article, an APXML recommender-splitting lesson); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** A 30-day feature that reads up to 15 days after the prediction date uses the future, so I would prove it by replaying the feature from a snapshot cut at the prediction date, rebuild every feature as-of that date, and audit the rest of the feature set the same way.

**Clarifying questions:**
- What exactly is "the prediction date" and what is the label window? Why: the leak is any feature timestamp later than the prediction timestamp, so I need both clocks defined.
- How was the training table built: a daily snapshot of a feature store, or one big batch query over the full history? Why: batch queries over the full table are where centred windows and "latest value" joins sneak in.
- Is the 0.77 live number measured on the same population and label definition as the 0.91? Why: I must rule out a different cohort or label before blaming the feature.
- Who else uses spend_30d, and are other features built by the same code? Why: the same helper function probably produced other leaks.
- Is there a record of what the live system actually saw on the scoring date? Why: logged serving features are the ground truth to compare the offline table against.

**Approach:**
1. Say what the bug is. The offline spend_30d at prediction date T uses days T-14 to T+15. Live, only days up to T exist. Churners stop spending after they churn, so a window that looks forward sees "no spend" exactly for the customers who are about to churn. The model learns "low future spend means churn", which is the label itself.
2. Prove it with a replay test. Cut the raw events at T so nothing later exists, recompute the feature with the same code, and compare with the stored value. If values change, the feature used data from after T. Count the rows that change.
3. Back it up with two cheap tests. Shift the window back by 15 days: a leak collapses, real signal stays. Compare offline feature values with the logged live values on the same customers and dates.
4. Rebuild with point-in-time correctness. Every feature row gets an `as_of` timestamp. Each source event gets an event time and, if it arrives late, an ingestion time. The join rule is: event_time <= as_of (and ingestion_time <= as_of for late data). In pandas this is `merge_asof` on time, per customer. Windows are trailing only.
5. Audit all features with the same replay: truncate the data at T, recompute every feature, flag any that change. Add a screen for "too good" single-feature AUCs, which are a clue, not a proof.
6. Retrain on the rebuilt table and re-evaluate with a time split. Expect AUC to fall to near the live number. Report the old number as inflated.
7. Make it permanent: a unit test that runs the replay on a sample, a lint rule that bans centred or forward windows, and the same feature code for training and serving.

**Metrics:**
- Replay mismatch rate = rows where recomputed-from-truncated value differs from stored value / all rows. It should be 0 for every feature.
- AUC of the model with leaky vs point-in-time features, on the same time-split test set (the gap is the inflation).
- Train/serve parity: share of live logged feature values equal to the offline recomputation for the same customer and date (target above 99%).
- Guardrail: the live AUC after the fix should land near the rebuilt offline AUC, not near 0.91.

**Risks:**
- The replay only catches leaks the code can express; a label-derived column (like a "closed account" flag) passes a time replay but is still a leak. Review semantics, not only timestamps.
- Late-arriving events: a table keyed on event time can include rows that were not yet in the system at T. Use ingestion time for the as-of join.
- Rebuilding fixes only the feature; a random split of rows from the same customer can still leak (see Book 6 Part 3 Q8 "A model trained on 40,000 rows from 8,000 customers..." and Q9 "A churn model scores AUC 0.88 under a random split...").
- Declaring victory because AUC dropped: the drop is expected, not a finding of quality.

**What the interviewer scores:**
- Strong: names the mechanism (the window includes days after the prediction date, and churners go quiet) and proposes an executable proof (replay on truncated data), not an argument.
- Strong: as-of joins with event and ingestion time, trailing windows only, one code path for training and serving.
- Strong: audits the whole feature set and sets up a permanent test.
- Weak: "the rolling aggregate is fine", "just drop the feature" without proof, or "retrain with more data".
- Cross-reference: Book 1 Part 1 has "What is data leakage? Give 4 real examples (target, preprocessing, temporal, group) and how you would detect it." and Book 1 Part 6 has "How do you build lag and rolling-window features for a GBM (XGBoost/LightGBM) forecaster without leaking future information?".

**Example:** (illustrative numbers) Prediction date T = day 100. Customer A spent Rs 400, 0, 600 in her last three order days and stops buying on day 108 (she churns). Her stored spend_30d covers days 86 to 115, so it contains only the pre-day-108 spend and zero afterwards: it is low. A loyal customer B keeps buying until day 115, so his window is full. At scoring time on day 100 the live feature has no days 101 to 115 at all, so both look alike. Weak answer: "It is a rolling aggregate, it is fine." Strong answer: "Replay it with data cut at day 100. If the value changes for A and B, the window reaches past the prediction date. I would rebuild with an as-of join and re-evaluate."

**Code:**
```python
import numpy as np
from scipy.stats import rankdata

rng = np.random.default_rng(31)
N, D, T = 4000, 160, 100          # customers, days of history, prediction day
H = 15                            # label horizon: churn within the next 15 days

def auc(y, s):
    r = rankdata(s); n1 = int(y.sum()); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)

# daily spend panel: customers order on a day with prob p; churners stop on their churn day
churn = rng.random(N) < 0.15
c_day = np.where(churn, T + rng.integers(1, H + 1, N), 10**6)
p = rng.beta(3, 3, N) * np.where(churn, 0.55, 1.0)       # churners are slightly less active before
active = np.arange(D)[None, :] < c_day[:, None]
spend = rng.random((N, D)) < p[:, None]
spend = spend * rng.gamma(2.0, 250.0, (N, D)) * active
y = churn.astype(int)                                      # label: churned in (T, T+30]

# 1) the leaky feature: window [T-14, T+15] (centred on T); honest feature: window [T-29, T]
leaky = spend[:, T - 14:T + 16].sum(1)
honest = spend[:, T - 29:T + 1].sum(1)
print("spend_30d offline AUC (leaky window)     :", round(auc(y, -leaky), 3))
print("spend_30d point-in-time AUC (trailing)   :", round(auc(y, -honest), 3))

# 2) replay test: recompute the feature from data truncated at the prediction date and compare
def spend_30d_replay(data, t, window_fn):
    visible = data[:, :t + 1]                  # nothing after t exists in the snapshot
    return window_fn(visible, t)
def leaky_window(vis, t):                      # what the team computed; asks for days that do not exist yet
    return vis[:, max(0, t - 14):t + 16].sum(1)
def trailing_window(vis, t):
    return vis[:, t - 29:t + 1].sum(1)
rep_leaky = spend_30d_replay(spend, T, leaky_window)
rep_ok = spend_30d_replay(spend, T, trailing_window)
diff_leaky = np.mean(~np.isclose(rep_leaky, leaky))
diff_ok = np.mean(~np.isclose(rep_ok, honest))
print("share of rows where replay != stored, leaky:", round(diff_leaky, 3), " trailing:", diff_ok)
# rows that changed are exactly those with spend in days T+1..T+15
future_used = spend[:, T + 1:T + 16].sum(1) > 0
assert np.array_equal(~np.isclose(rep_leaky, leaky), future_used)
assert diff_ok == 0.0

# 3) shift test: push the window back by 15 days; a leak vanishes, real signal stays
shifted = spend[:, T - 29 - 15:T + 1 - 15].sum(1)
print("AUC after shifting the window 15 days back:", round(auc(y, -shifted), 3))

# 4) audit the rest of the feature set with the same replay and a suspicious-AUC screen
orders_7d = (spend[:, T - 6:T + 1] > 0).sum(1)                    # trailing, fine
last_order_gap_full = np.array([T - np.max(np.nonzero(r[:T + 1 + 15])[0], initial=0) for r in spend])  # looks 15 days ahead
last_order_gap_ok = np.array([T - np.max(np.nonzero(r[:T + 1])[0], initial=0) for r in spend])
rows = [("spend_30d", leaky, rep_leaky), ("orders_7d", orders_7d, orders_7d),
        ("days_since_last_order", last_order_gap_full, last_order_gap_ok)]
for name, stored, replay in rows:
    flag = np.mean(~np.isclose(stored, replay))
    a = max(auc(y, stored), 1 - auc(y, stored))
    print(f"{name:24s} rows changed by replay: {flag:5.3f}   single-feature AUC as stored: {a:.3f}")

assert 0.82 < auc(y, -leaky) < 0.92 and 0.72 < auc(y, -honest) < 0.82
assert auc(y, -leaky) - auc(y, -honest) > 0.06
assert abs(auc(y, -shifted) - auc(y, -honest)) < 0.03
assert diff_leaky > 0.3
```

**Output (my run):**
```text
spend_30d offline AUC (leaky window)     : 0.861
spend_30d point-in-time AUC (trailing)   : 0.782
share of rows where replay != stored, leaky: 0.948  trailing: 0.0
AUC after shifting the window 15 days back: 0.779
spend_30d                rows changed by replay: 0.948   single-feature AUC as stored: 0.861
orders_7d                rows changed by replay: 0.000   single-feature AUC as stored: 0.727
days_since_last_order    rows changed by replay: 0.948   single-feature AUC as stored: 0.948
```
The text above matches this run: the leaky window gives AUC 0.861 against 0.782 for the trailing window (the real inflation is smaller than the prompt's 0.91 vs 0.77 because the simulation is simple, the direction is the point). The replay changes 94.8% of the leaky feature's rows and 0% of the trailing feature's, and exactly the rows with spend in days T+1 to T+15 (asserted). Shifting the window 15 days back gives 0.779, which is back to the honest level. In the audit, orders_7d is clean, and days_since_last_order, which looked 15 days ahead, changes in 94.8% of rows and has a suspicious single-feature AUC of 0.948.

**Follow-ups:**
- Replay says some rows are unchanged. Is that fine? Those rows had no spend after T, so the leak did not touch them, but the code is still wrong; fix the code, not just the rows.
- How do you stop it happening again? Add the replay test to CI, keep a feature store with as-of retrieval, and log serving features so training and serving can be compared.
- The team insists the feature is "only" 15 days ahead and "only sometimes". Does the size matter? No. Any future information can inflate offline AUC, and "sometimes" means the leak is concentrated in the customers near the label event, which are the ones the model is judged on.

**Common mistakes:** Arguing from the feature's name instead of replaying it. Fixing one feature and not auditing the others. Using event time for late-arriving data. Using a random split after the fix. Treating the lower AUC as a regression instead of the true number.

### Q32 ⭐⭐ 🟡 A team has three heuristic labelling rules for spam that cover 20%, 35% and 50% of posts and often disagree where they overlap, and it has only 300 hand-labelled posts. They want to combine the rules into training labels. Explain how you would combine them, how you would estimate the accuracy of each rule, and what role the 300 hand labels should play.
**Asked at:** AI-era LLM-labelling, weak-supervision and synthetic-data material (an arXiv 2026 abuse-detection paper using LLM annotators, an arXiv survey on LLM-driven synthetic data, an arXiv paper on weak data and model collapse, a Codemia labelling course page); emerging practitioner and research theme, not a confirmed interview staple; search snippets only, not opened
**Say this first (1 line):** I would treat each rule as a noisy voter, learn how accurate each one is from how the rules agree and disagree on the posts they share, combine them with accuracy-based weights (a label model), and use the 300 hand labels to check the result, not to fit it.

**Clarifying questions:**
- What do the rules look like (keyword lists, link counts, account age)? Why: rules built from the same signal make correlated mistakes, and the combination method assumes they do not.
- Does a rule vote on both classes or only fire for spam? Why: a one-sided rule (abstain unless spam) needs a different model of its errors.
- Were the 300 hand labels sampled at random from all posts, or picked where the rules fired or disagreed? Why: a biased hand set gives biased accuracy estimates.
- How common is spam, and is the cost of a false positive (blocking a real post) higher than a miss? Why: it sets the threshold on the final probability.
- Will the final model be a classifier trained on these labels and served on posts the rules never cover? Why: that is the real goal, and it changes how I judge success.

**Approach:**
1. Write each rule as a labelling function: it returns spam, not spam, or abstain. Build a post-by-rule matrix of votes.
2. Check coverage, overlap and conflict. Coverage 20%, 35%, 50% gives a union of about 73% if rules fire independently (1 minus 0.8 x 0.65 x 0.5). Posts no rule covers get no weak label.
3. Estimate each rule's accuracy without labels. For rules that make independent errors, the product of two rules' signed accuracies equals their average agreement: with votes as plus or minus 1, E[l_i l_j] = m_i m_j where m = 2 x accuracy - 1. Three rules give three equations and three unknowns, so each m_i is solvable. Do it on the posts where the pair both vote.
4. Combine with a label model, not a vote count: weight each rule by the log-odds of its accuracy, sum the signed votes, and turn the total into a probability. Ties and uncovered posts abstain.
5. Use the 300 hand labels as a validation set: measure the label model's accuracy and per-rule accuracy with confidence intervals, check the independence assumption (do the rules' errors correlate?), and tune the final threshold. Do not train on them only, and do not reuse them as the final test set if you tuned on them.
6. Train a normal classifier on the weak labels (use the probabilities as soft labels) so it can generalise to posts no rule covers. Judge it on a separate hand-labelled test set, not on weak labels.
7. Keep improving where it pays: label more posts where the rules conflict, and add rules for uncovered posts.

**Metrics:**
- Per-rule coverage = posts it votes on / all posts; overlap and conflict rates = posts with two or more votes (conflict: votes differ) / all posts.
- Estimated accuracy per rule, with the pair-agreement estimate compared against the hand-label estimate and its 95% interval.
- Label-model accuracy on hand labels, on the decided posts; also report the share decided (coverage).
- Final classifier: precision, recall and PR-AUC on a clean hand-labelled test set; guardrail: false-positive rate on real posts.

**Risks:**
- Correlated rules (two rules reading the same keyword): the agreement method over-counts their evidence and the weights are wrong.
- Coverage that depends on the label: a rule that only fires on obvious spam has accuracy estimates that do not transfer to hard posts.
- 300 labels spread over three rules: rule 1 fires on only about 60-75 of them, so its measured accuracy is wide (see the Code block, 0.89 to 0.99 for one rule).
- Teaching the classifier to copy the rules instead of learning the content.
- Using the same 300 posts to estimate accuracies, tune, and report the final number.

**What the interviewer scores:**
- Strong: models abstain, overlap and conflict, and explains that disagreement is the information that reveals accuracy.
- Strong: gives the pair-agreement (triplet) logic or an EM-style label model, and states the independence assumption and how to test it.
- Strong: uses the hand labels for validation and error analysis, with intervals, and keeps a separate clean test set.
- Weak: "take the majority vote" with no accuracy estimate, or "train on the 300 hand labels and ignore the rules".
- Cross-reference: Book 1 Part 3 has "You use an LLM as a classifier or judge to label data. How do you evaluate it (metrics, imbalance, agreement with humans, calibration)?" for the measuring side.

**Example:** (illustrative numbers) 1,000 posts. Rules 1 and 2 both vote on 70 posts and agree on 48 (68.6%). With votes as plus or minus 1, average product = 2 x 0.686 - 1 = 0.371, so m1 x m2 = 0.371. Suppose the other pairs give m1 x m3 = 0.22 and m2 x m3 = 0.15 (invented). Then m1 squared = 0.371 x 0.22 / 0.15 = 0.544, so m1 = 0.74 and accuracy 1 = (1 + 0.74) / 2 = 0.87. Weak answer: "majority vote of the three rules." Strong answer: "estimate each rule's accuracy from the overlap, weight by log-odds, validate on the 300 hand labels, train a classifier on the soft labels."

**Code:**
```python
import numpy as np
from scipy.stats import beta

rng = np.random.default_rng(32)
N = 20000
y = (rng.random(N) < 0.25).astype(int)            # 1 = spam, invented prevalence 25%
cover = [0.20, 0.35, 0.50]
acc = [0.90, 0.75, 0.65]                          # true accuracy of each rule where it fires (hidden from the model)
L = np.full((N, 3), -1)                           # -1 = abstain
for j in range(3):
    fires = rng.random(N) < cover[j]
    right = rng.random(N) < acc[j]
    L[:, j] = np.where(fires, np.where(right, y, 1 - y), -1)

print("coverage per rule:", [round(float((L[:, j] >= 0).mean()), 3) for j in range(3)])
union = (L >= 0).any(1)
print("posts with at least one vote:", round(float(union.mean()), 3))
assert abs(union.mean() - (1 - 0.8 * 0.65 * 0.5)) < 0.01

# agreement on overlaps (no labels needed)
def agree(i, j):
    both = (L[:, i] >= 0) & (L[:, j] >= 0)
    return both.sum(), (L[both, i] == L[both, j]).mean()
for i, j in [(0, 1), (0, 2), (1, 2)]:
    n, a = agree(i, j)
    print(f"rules {i+1},{j+1}: overlap n={n}, agree={a:.3f}")

# triplet method: with conditionally independent rules, m_i = 2*acc_i - 1 and E[l_i l_j] = m_i m_j (votes as +-1)
def m_ij(i, j):
    both = (L[:, i] >= 0) & (L[:, j] >= 0)
    return np.mean((2 * L[both, i] - 1) * (2 * L[both, j] - 1))
m = [np.sqrt(m_ij(0, 1) * m_ij(0, 2) / m_ij(1, 2)),
     np.sqrt(m_ij(0, 1) * m_ij(1, 2) / m_ij(0, 2)),
     np.sqrt(m_ij(0, 2) * m_ij(1, 2) / m_ij(0, 1))]
est = [(1 + x) / 2 for x in m]
print("estimated accuracy (no labels):", [round(float(a), 3) for a in est], " true:", acc)
assert all(abs(e - a) < 0.05 for e, a in zip(est, acc))

# combine: majority vote versus accuracy-weighted vote (weights = log-odds of estimated accuracy)
w = np.log(np.array(est) / (1 - np.array(est)))
score = np.zeros(N)
for j in range(3):
    score += np.where(L[:, j] >= 0, w[j] * (2 * L[:, j] - 1), 0.0)
mv = np.where(L >= 0, 2 * L - 1, 0).sum(1)
wv_lab = np.where(score > 0, 1, 0); mv_lab = np.where(mv > 0, 1, 0)
dec_w = union & (score != 0); dec_m = union & (mv != 0)
print("majority vote: decided", round(float(dec_m.mean()), 3), " accuracy", round(float((mv_lab[dec_m] == y[dec_m]).mean()), 3))
print("weighted vote: decided", round(float(dec_w.mean()), 3), " accuracy", round(float((wv_lab[dec_w] == y[dec_w]).mean()), 3))
accw = (wv_lab[dec_w] == y[dec_w]).mean(); accm = (mv_lab[dec_m] == y[dec_m]).mean()
common = dec_m & dec_w
am = (mv_lab[common] == y[common]).mean(); aw = (wv_lab[common] == y[common]).mean()
print("same posts both decide:", round(float(common.mean()), 3), " majority", round(float(am), 3), " weighted", round(float(aw), 3))
assert aw > am
conflict = ((L == 1).sum(1) > 0) & ((L == 0).sum(1) > 0) & dec_w
print("posts where rules vote both ways:", int(conflict.sum()), " weighted vote accuracy there:", round(float((wv_lab[conflict] == y[conflict]).mean()), 3))
assert (wv_lab[conflict] == y[conflict]).mean() > 0.6

# the 300 hand labels: how well can they measure each rule alone?
hand = rng.choice(N, 300, replace=False)
for j in range(3):
    f = hand[L[hand, j] >= 0]
    k = int((L[f, j] == y[f]).sum()); n = len(f)
    lo, hi = beta.ppf(0.025, k, n - k + 1), beta.ppf(0.975, k + 1, n - k)
    print(f"rule {j+1}: hand-labelled posts where it fires n={n}, accuracy {k/n:.2f}, 95% CI {lo:.2f}-{hi:.2f}")
# the width on rule 1 (about 60 posts) is wide: that is why the hand set validates, it does not fit the weights
n1 = int((L[hand, 0] >= 0).sum())
assert 40 <= n1 <= 80
```

**Output (my run):**
```text
coverage per rule: [0.192, 0.347, 0.495]
posts with at least one vote: 0.734
rules 1,2: overlap n=1346, agree=0.686
rules 1,3: overlap n=1854, agree=0.611
rules 2,3: overlap n=3469, agree=0.577
estimated accuracy (no labels): [0.864, 0.755, 0.652]  true: [0.9, 0.75, 0.65]
majority vote: decided 0.641  accuracy 0.761
weighted vote: decided 0.734  accuracy 0.753
same posts both decide: 0.641  majority 0.761  weighted 0.763
posts where rules vote both ways: 2232  weighted vote accuracy there: 0.707
rule 1: hand-labelled posts where it fires n=74, accuracy 0.96, 95% CI 0.89-0.99
rule 2: hand-labelled posts where it fires n=86, accuracy 0.79, 95% CI 0.69-0.87
rule 3: hand-labelled posts where it fires n=161, accuracy 0.62, 95% CI 0.54-0.70
```
The text above matches this run: coverage is 19%, 35% and 50% with 73.4% of posts voted on by at least one rule. Pair agreement on overlaps (68.6%, 61.1%, 57.7%) yields accuracy estimates of 0.864, 0.755 and 0.652 against true values of 0.90, 0.75 and 0.65, so the estimate is close but not exact (rule 1 is estimated from about 1,300 overlap posts). Weighted voting decides 73.4% of posts at 75.3% accuracy, while majority vote decides only 64.1% (ties abstain) at 76.1%; on the 64.1% both decide the two are nearly equal (76.1% vs 76.3%). So in this simulation the main gain from weights is coverage and sensible tie-breaking, not accuracy. On posts where rules vote both ways the weighted vote gets 70.7%. The 300 hand labels give wide intervals for each rule (rule 1: 74 posts, 0.89 to 0.99), which is why they validate rather than fit.

**Follow-ups:**
- What if two rules are copies of each other? Their agreement is inflated, the estimator trusts them too much; detect by checking pairwise error correlation on the hand labels and drop or merge one.
- Why not train on the 300 labels alone? 300 labels give a weak classifier and wide intervals; the rules give far more (noisy) coverage. Use both: rules to train, hand labels to measure.
- Can an LLM be one of the labelling functions? Yes, treat it as a fourth noisy voter and measure its accuracy the same way; do not let it also grade the final model (see Book 6 Part 3 Q43 "A team labelled training data with one LLM and now uses the same LLM as the judge...").

**Common mistakes:** Majority vote with no accuracy estimate. Treating abstain as "not spam". Assuming independence without checking. Spending all 300 labels on training. Reporting accuracy on weak labels as if they were truth.

### Q33 ⭐⭐ 🟡 A team has 800 real fraud cases among 400,000 transactions (0.2%) and plans to generate 50,000 synthetic fraud rows with a generative model to make the data more balanced. Explain the risks, how you would validate that the synthetic rows help rather than hurt, and why the test set must remain real data only.
**Asked at:** AI-era LLM-labelling, weak-supervision and synthetic-data material (an arXiv 2026 abuse-detection paper using LLM annotators, an arXiv survey on LLM-driven synthetic data, an arXiv paper on weak data and model collapse, a Codemia labelling course page); emerging practitioner and research theme, not a confirmed interview staple; search snippets only, not opened
**Say this first (1 line):** Synthetic fraud rows add no new information beyond the 800 real cases, they can copy or distort them, and 50,000 of them would not even balance the data, so I would test them as an ablation inside training folds and judge everything on real, untouched test data.

**Clarifying questions:**
- How is the generator trained (GAN, VAE, diffusion, or an LLM for tabular rows), and on which of the 800 cases? Why: if it saw the cases that later land in the test set, the test is contaminated.
- Is the fraud one pattern or many (card-not-present, account takeover, mule accounts)? Why: a generator tends to average modes and can blur the rare ones.
- What does the model do with the score: rank for review, or block at a threshold? Why: the cost of false alarms decides whether a shifted score distribution matters.
- Is the 0.2% rate stable over time, and are labels delayed? Why: it affects how many real cases I can put in a time-split test set.
- Why balance at all? Why: class weights, a cost-sensitive threshold or a plain model with PR-AUC may already do the job without inventing data.

**Approach:**
1. Do the arithmetic first. 800 + 50,000 = 50,800 fraud rows against 399,200 legitimate ones is 11.3% fraud, not balanced. A 50/50 set would need 398,400 synthetic rows, about 498 copies per real case. Whatever the plan is, the ratio is set by the generator, not by information.
2. Name the risks. (a) No new information: the generator can only reshuffle what it saw in 800 rows, so the model is trained on the generator's guess about fraud. (b) Memorisation: copies or near-copies of real rows. (c) Mode collapse or smoothing: a smooth generator fills the gaps between modes with fake fraud. (d) Shifted scores and calibration: with a fraud share of 11% in training, probabilities are far above the true 0.2%. (e) Leakage into evaluation if synthetic rows are derived from the test cases.
3. Split first, by time or group. Hold out a real test set (and keep its fraud cases out of the generator). Fit the generator only on training-fold fraud.
4. Run an ablation on real data: baseline (no synthetic), class weights, undersampling, and +synthetic at several amounts (for example 0, 2,000, 10,000, 50,000). Same model, same folds, many seeds.
5. Check the synthetic rows themselves: distance to the nearest real training row (privacy and memorisation), per-feature and joint distribution versus real, and a classifier two-sample test (can a model tell synthetic from real?).
6. Report PR-AUC, recall at a fixed review budget, and precision at that budget, each with an interval, on the real test only. Fix the threshold on real validation data; correct the calibration if scores are used as probabilities.
7. Decide. Keep synthetic data only if the gain on real test data is larger than the seed-to-seed spread, and say so with the interval.

**Metrics:**
- PR-AUC (average precision) on the real test set; the baseline value is the fraud rate, about 0.002.
- Recall at a fixed alert budget = frauds caught in the top K scores / all frauds in the test set; precision at K = frauds caught / K.
- Memorisation check = share of synthetic rows closer to a real training row than a small distance threshold; leak check = the same distance to real test frauds.
- Guardrails: calibration (mean predicted rate vs observed rate on real data), alert volume, and per-segment recall.

**Risks:**
- Evaluating on a test set that contains real frauds the generator saw: scores jump (see the Code block).
- Evaluating on a mix of real and synthetic rows: the model is rewarded for recognising the generator.
- Judging one run: with a few hundred test frauds the PR-AUC moves by several points from seed to seed.
- Fixing the wrong problem: if the issue is a poor threshold, more data of the same kind does not help.
- Fraud adapts; a generator trained on last year's pattern teaches last year's pattern.

**What the interviewer scores:**
- Strong: spots that the arithmetic does not balance and says why 800 real cases cap the information.
- Strong: puts the generator inside the training fold, ablates against class weights and undersampling, and reports intervals.
- Strong: keeps the test set 100% real, time-ordered, and untouched by the generator.
- Weak: "more data is always good", or reporting accuracy or ROC-AUC on a mixed set.
- Cross-reference: Book 6 Part 3 Q2 "A colleague balanced a table of 10,000 rows (500 positives, 5%) to 50/50 with SMOTE and only then split it into train and test..." covers the split-order version of the same mistake, and Book 1 Part 3 has "How do you handle class imbalance? Walk through the options and how you choose between them."

**Example:** (illustrative numbers) 400,000 transactions, 800 fraud. Adding 50,000 synthetic fraud rows: 800 + 50,000 = 50,800 fraud of 450,000 rows = 11.3%. Each real fraud is repeated or imitated about 62 times (50,000 / 800). A model trained there scores real fraud at roughly 11% base rate, so a score of 0.3 does not mean 30%. Weak answer: "balance the data with a GAN and test on the balanced set." Strong answer: "the generator is an ablation inside training folds; I would compare it with class weights, test only on real held-out time, and report PR-AUC with an interval."

**Code:**
```python
import numpy as np

# --- the arithmetic in the prompt
real_fraud, total = 800, 400_000
synth = 50_000
legit = total - real_fraud
print("fraud share before:", round(real_fraud / total, 4))
print("fraud share after adding 50,000:", round((real_fraud + synth) / (legit + real_fraud + synth), 4))
need = legit - real_fraud
print("synthetic rows needed for 50/50:", need)
assert round((real_fraud + synth) / (total + synth), 3) == round(50_800 / 450_000, 3)
assert need == 398_400

rng = np.random.default_rng(33)
d = 4
def make(n, nf):
    X = rng.normal(size=(n, d)); y = np.zeros(n, int); y[:nf] = 1       # exactly nf frauds
    sign = np.where(rng.random(nf) < 0.5, -1.0, 1.0)                     # two fraud modes: x0 near -2.2 or +2.2
    X[:nf, 0] = sign * 2.2 + rng.normal(scale=0.6, size=nf)
    X[:nf, 1] += 1.0; X[:nf, 2] += 0.8; X[:nf, 3] += 0.6
    p = rng.permutation(n)
    return X[p], y[p]
X, y = make(400_000, 800)
print("simulated fraud cases:", int(y.sum()), "rate", round(float(y.mean()), 4))
idx = rng.permutation(len(y)); tr, te = idx[:280_000], idx[280_000:]
Xtr, ytr, Xte, yte = X[tr], y[tr], X[te], y[te]

def feats(X): return np.hstack([X, X ** 2, np.ones((len(X), 1))])
def fit(F, t, w=None, iters=25, l2=1e-3):
    w = np.ones(len(t)) if w is None else w
    b = np.zeros(F.shape[1])
    for _ in range(iters):
        p = 1 / (1 + np.exp(-F @ b)); g = F.T @ (w * (p - t)) + l2 * b
        H = (F * (w * p * (1 - p))[:, None]).T @ F + l2 * np.eye(len(b))
        b -= np.linalg.solve(H, g)
    return b
def ap(t, s):
    o = np.argsort(-s); t = t[o]; tp = np.cumsum(t)
    return float(np.sum(tp / np.arange(1, len(t) + 1) * t) / t.sum())

# generators fitted ONLY on the 560 real training frauds (the honest way), or on all frauds (the leak)
F_tr = Xtr[ytr == 1]; F_all = X[y == 1]
def gaussian_gen(src, n):
    return rng.multivariate_normal(src.mean(0), np.cov(src.T), n)
def memoriser_gen(src, n, s=0.15):
    return src[rng.integers(0, len(src), n)] + rng.normal(scale=s, size=(n, d))

from scipy.spatial import cKDTree
def run(Xs=None):
    Xa = Xtr if Xs is None else np.vstack([Xtr, Xs]); ya = ytr if Xs is None else np.r_[ytr, np.ones(len(Xs), int)]
    b = fit(feats(Xa), ya)
    lr = ap(yte, feats(Xte) @ b)
    _, nn = cKDTree(Xa).query(Xte, k=15)
    knn = ap(yte, ya[nn].mean(1) + 1e-6 * (feats(Xte) @ b > 0))
    return lr, knn
print("test fraud cases:", int(yte.sum()), "train fraud cases:", int(ytr.sum()))
res = {}
res["real only"] = run()
res["+50k gaussian (one blob)"] = run(gaussian_gen(F_tr, synth))
res["+50k memoriser (train frauds)"] = run(memoriser_gen(F_tr, synth))
res["+50k memoriser fitted on ALL frauds (leak)"] = run(memoriser_gen(F_all, synth))
print(f"{'arm':45s} {'logistic PR-AUC':>16s} {'15-NN PR-AUC':>13s}   (real test, base rate {yte.mean():.4f})")
for k, v in res.items(): print(f"{k:45s} {v[0]:16.3f} {v[1]:13.3f}")
# the leak is visible: the leaky arm beats the honest memoriser only because test frauds were copied
assert res["+50k memoriser fitted on ALL frauds (leak)"][1] > res["+50k memoriser (train frauds)"][1]
# sanity: how many of the 50,000 synthetic rows are within 0.3 of a real test fraud in the leaky arm vs honest
def near_test(Xs):
    T = Xte[yte == 1]; c = 0
    for r in Xs[:2000]: c += (np.sqrt(((T - r) ** 2).sum(1)).min() < 0.3)
    return c / 2000
print("share of synthetic rows within 0.3 of a real TEST fraud: honest", near_test(memoriser_gen(F_tr, synth)), " leaky", near_test(memoriser_gen(F_all, synth)))
assert near_test(memoriser_gen(F_all, synth)) > near_test(memoriser_gen(F_tr, synth))
# one real train fraud is copied about 50,000 / 560 times
print("copies per real training fraud:", round(synth / int(ytr.sum()), 1))
assert 80 < synth / int(ytr.sum()) < 100
gs = gaussian_gen(F_tr, synth)
print("share of real train frauds with |x0|<1:", round(float((np.abs(F_tr[:, 0]) < 1).mean()), 3), "  of gaussian synthetic rows:", round(float((np.abs(gs[:, 0]) < 1).mean()), 3))
assert (np.abs(gs[:, 0]) < 1).mean() > 5 * (np.abs(F_tr[:, 0]) < 1).mean()
```

**Output (my run):**
```text
fraud share before: 0.002
fraud share after adding 50,000: 0.1129
synthetic rows needed for 50/50: 398400
simulated fraud cases: 800 rate 0.002
test fraud cases: 253 train fraud cases: 547
arm                                            logistic PR-AUC  15-NN PR-AUC   (real test, base rate 0.0021)
real only                                                0.128         0.101
+50k gaussian (one blob)                                 0.137         0.097
+50k memoriser (train frauds)                            0.101         0.065
+50k memoriser fitted on ALL frauds (leak)               0.100         0.311
share of synthetic rows within 0.3 of a real TEST fraud: honest 0.0585  leaky 0.2235
copies per real training fraud: 91.4
share of real train frauds with |x0|<1: 0.02   of gaussian synthetic rows: 0.338
```
The text above matches this run: fraud share goes from 0.2% to 11.29% with 50,000 rows, and 398,400 rows would be needed for 50/50. In the simulation (800 frauds in two modes, 547 in train, 253 in test) a generator fitted on training fraud only gave no clear gain: logistic PR-AUC 0.128 (real only) versus 0.137 (single Gaussian) and 0.101 (copy-and-jitter), with the nearest-neighbour model going from 0.101 to 0.097 and 0.065. With one seed, differences of a few points are within noise, so I would not claim the Gaussian helped. The single Gaussian put 33.8% of synthetic rows in the gap between the two real modes (|x0| < 1) against 2.0% of real frauds, which is the fake-region risk. The leak is large: when the copy-and-jitter generator is fitted on all 800 frauds, the nearest-neighbour test PR-AUC jumps to 0.311, because 22.4% of synthetic rows sit within 0.3 of a real test fraud (5.9% in the honest version).

**Follow-ups:**
- Is synthetic data ever useful? It can help when it is built from a domain simulator or known rules that add real information (for example new attack types), or to stress-test systems; a purely learned generator from 800 rows adds little.
- How do you handle the score calibration? Train on the synthetic-augmented data if you must, then recalibrate on real validation data (prior correction, Platt or isotonic) before using scores as probabilities.
- What do you do instead? Class weights or a cost-based threshold, careful stratified or time-based splits, more real labels (active learning on borderline cases), and unsupervised or rule signals as extra features.

**Common mistakes:** Mixing synthetic rows into the test set. Fitting the generator before splitting. Believing 50,000 rows balance 400,000. Reporting accuracy. Using the inflated score as a probability. Judging on one seed.

### Q34 ⭐⭐ 🟡 On a training set of 28,000 rows, a cross-validated model strongly disagrees with the given label (confidence above 0.95) on 700 rows (2.5%), and a reviewer finds that 62 of 100 sampled flagged rows are really mislabelled. Explain how you would estimate the overall label-noise rate, how far you would trust that estimate, and whether you would drop, relabel or down-weight those rows.
**Asked at:** Noisy-label and annotator-disagreement material (Tanno et al., CVPR 2019 on annotator confusion matrices; a Codemia data-labelling course page); research and course pages rather than interview banks, so the scenario is partly editor-designed; search snippets only, not opened
**Say this first (1 line):** The flagged rows only give a floor on the noise rate (about 434 mislabelled rows, 1.6% of the data), because the model flags only the obvious errors, so I would audit a random sample of the unflagged rows too before I quote an overall rate, and I would relabel with human review, not delete blindly.

**Clarifying questions:**
- How were the 100 flagged rows sampled (random among the 700, or the most confident)? Why: a biased review sample biases the 62% precision.
- Is the reviewer reliable (single person, a second opinion on disputed rows)? Why: if the reviewer is noisy, "really mislabelled" is itself uncertain.
- Does the noise look class-dependent or concentrated in some segment? Why: noise that is not random changes both the estimate and the fix.
- What is the model for: ranking, or a decision with a threshold? Why: ranking is fairly robust to light noise; threshold use and calibration are not.
- Is the evaluation set clean? Why: a noisy test set caps the measurable accuracy and hides improvement.

**Approach:**
1. State what is known. 700 of 28,000 rows are flagged (2.5%). The reviewer found 62 of 100 truly mislabelled: precision of the flag is 62%, 95% interval about 52% to 72%.
2. Scale it up: 700 x 0.62 = 434 mislabelled rows among the flagged (interval about 362 to 501), which is 1.55% of 28,000. This is a lower bound on the noise rate, not the rate.
3. Estimate the rest. Draw a random sample of unflagged rows, say 300, and have them reviewed. If 9 are wrong, then 27,300 x 9/300 = 819 more, and the total is about 1,253 rows, 4.5%. Combine both pieces with intervals (stratified estimate: flagged stratum plus unflagged stratum).
4. Know why the unflagged stratum matters. A model that is confident (above 0.95) against a label will find only errors that are far from the decision boundary; mislabelled borderline rows look like ordinary hard examples. In a simulation, flagging at high confidence found only about 14% of the real noise.
5. Trust the estimate only as far as the sample: report intervals, the review protocol and the reviewer agreement, and give the noise rate by class and by segment where the sample size allows.
6. Choose the action by cost. Relabel the flagged rows through human review (best when the label can be checked). Down-weight or drop only when review is too costly, and expect about 38% of flagged rows to be valid hard cases that you would be throwing away.
7. Fix the process: look at where the noise came from (a guideline change, a vendor, a time window) and add a label-quality gate so you do not clean the same problem every quarter.

**Metrics:**
- Flag precision = reviewed-flagged rows that are truly mislabelled / reviewed-flagged rows (62/100).
- Noise rate estimate = (flagged x flag precision + unflagged x unflagged error rate) / all rows, with a 95% interval for each part.
- Flag recall (unknown directly) = flagged mislabelled rows / all mislabelled rows, estimated from the audit.
- Downstream guardrails: accuracy and calibration on a clean, reviewed test set, per-class recall, and the share of rows changed per class.

**Risks:**
- Quoting 2.5% or 1.55% as "the noise rate".
- Dropping the 38% of flagged rows that are valid hard examples; they are often the informative ones and may sit in one class or segment.
- Relabelling with the model's own prediction, which just teaches the model its current mistakes.
- Cleaning the training set while the validation set stays noisy, so you cannot see the benefit.
- Reviewer error: a 100-row review with one disagreeing reviewer can move the number a lot.

**What the interviewer scores:**
- Strong: separates "precision of the flags" from "overall noise rate" and says the flagged set gives a lower bound.
- Strong: proposes a random audit of unflagged rows and reports intervals.
- Strong: chooses relabel-with-review over blind dropping and explains the cost of each.
- Weak: "700 rows are noisy, drop them", or "62% means the data is 62% wrong".
- Cross-reference: Book 6 Part 3 Q38 "An audit of 2,000 random transactions with intensive investigation found 25 frauds..." for noise that is not random, and Book 1 Part 3 has "Positive-unlabeled learning and noisy labels: when negatives are really unlabeled, how does that change metrics and training?".

**Example:** (illustrative numbers) 28,000 rows, 700 flagged. 62 of 100 reviewed are wrong, so 434 of the 700 flagged rows are wrong and 266 are right. If you drop all 700 you lose 266 correct rows. Suppose a random 300 unflagged rows hold 9 errors (3%): that is about 819 more bad rows among 27,300 unflagged rows. The overall rate is (434 + 819) / 28,000 = 4.5%, nearly three times the 1.55% you get from the flagged rows alone. Weak answer: "2.5% are flagged, so noise is 2.5%." Strong answer: "62% precision on flags gives a floor of 1.55%; I would audit unflagged rows to get the real rate."

**Code:**
```python
import numpy as np
from scipy.stats import beta

# --- 1) the arithmetic in the prompt
N, flagged, sampled, bad = 28_000, 700, 100, 62
prec = bad / sampled
lo, hi = beta.ppf(0.025, bad, sampled - bad + 1), beta.ppf(0.975, bad + 1, sampled - bad)
print("flag precision:", prec, " 95% CI", round(lo, 3), "-", round(hi, 3))
est_bad_flagged = flagged * prec
print("mislabelled rows among the 700 flagged:", est_bad_flagged, " (CI", round(flagged * lo), "-", round(flagged * hi), ")")
print("lower bound on noise rate from flagged rows alone:", round(est_bad_flagged / N, 4))
assert est_bad_flagged == 434.0 and round(est_bad_flagged / N, 4) == 0.0155
# unflagged rows must be audited too: invented audit of 300 random unflagged rows, 9 mislabelled
unflagged = N - flagged
u_bad, u_n = 9, 300
total_bad = est_bad_flagged + unflagged * u_bad / u_n
print("with an audit of unflagged rows (9 of 300): total noise rate", round(total_bad / N, 4))
assert round(total_bad / N, 3) == round((434 + 27_300 * 0.03) / 28_000, 3)

# --- 2) simulation: why 'flagged at 0.95' misses most of the noise
rng = np.random.default_rng(34)
n = 28_000
X = rng.normal(size=(n, 3)); w_true = np.array([1.5, -1.0, 0.5])
p = 1 / (1 + np.exp(-(X @ w_true)))
y_true = (rng.random(n) < p).astype(int)
flip = np.where(y_true == 1, rng.random(n) < 0.08, rng.random(n) < 0.03)      # asymmetric noise
y_obs = np.where(flip, 1 - y_true, y_true)
print("true noise rate:", round(float(flip.mean()), 4))

def fit(F, t, iters=20, l2=1e-3):
    b = np.zeros(F.shape[1]); w = np.ones(len(t))
    for _ in range(iters):
        q = 1 / (1 + np.exp(-F @ b)); g = F.T @ (w * (q - t)) + l2 * b
        H = (F * (w * q * (1 - q))[:, None]).T @ F + l2 * np.eye(len(b)); b -= np.linalg.solve(H, g)
    return b
F = np.hstack([X, np.ones((n, 1))])
fold = rng.permutation(n) % 5
prob = np.zeros(n)
for k in range(5):                                         # cross-validated probabilities: row never in its own fit
    b = fit(F[fold != k], y_obs[fold != k]); prob[fold == k] = 1 / (1 + np.exp(-F[fold == k] @ b))
conf_other = np.where(y_obs == 1, 1 - prob, prob)          # model's confidence in the OTHER class
flag = conf_other > 0.9
tp = int((flag & flip).sum())
print("flagged:", int(flag.sum()), " flag precision:", round(tp / flag.sum(), 3), " flag recall of the noisy rows:", round(tp / flip.sum(), 3))
assert tp / flip.sum() < 0.2          # most noisy rows are not flagged

# --- 3) drop vs relabel vs down-weight, scored on clean labels of a fresh test set
Xt = rng.normal(size=(20_000, 3)); yt = (rng.random(20_000) < 1 / (1 + np.exp(-(Xt @ w_true)))).astype(int)
Ft = np.hstack([Xt, np.ones((20_000, 1))])
def acc_of(b): return float((((Ft @ b) > 0).astype(int) == yt).mean())
b_all = fit(F, y_obs)
b_drop = fit(F[~flag], y_obs[~flag])
y_rel = np.where(flag, 1 - y_obs, y_obs); b_rel = fit(F, y_rel)
print("test accuracy  noisy:", round(acc_of(b_all), 4), " drop flagged:", round(acc_of(b_drop), 4), " relabel flagged:", round(acc_of(b_rel), 4))
clean_flagged = int((flag & ~flip).sum())
print("clean rows lost by dropping:", clean_flagged, "  clean rows corrupted by relabelling:", clean_flagged)
```

**Output (my run):**
```text
flag precision: 0.62  95% CI 0.517 - 0.715
mislabelled rows among the 700 flagged: 434.0  (CI 362 - 501 )
lower bound on noise rate from flagged rows alone: 0.0155
with an audit of unflagged rows (9 of 300): total noise rate 0.0447
true noise rate: 0.0548
flagged: 340  flag precision: 0.626  flag recall of the noisy rows: 0.139
test accuracy  noisy: 0.7644  drop flagged: 0.7645  relabel flagged: 0.7645
clean rows lost by dropping: 127   clean rows corrupted by relabelling: 127
```
The text above matches this run: 62% precision, interval 51.7% to 71.5%, so about 434 bad rows (362 to 501) and a floor of 1.55%; with the invented 9-of-300 audit the total is 4.47%. In the simulation (true noise 5.5%, 5-fold cross-validated model) flagging at 0.9 confidence found 340 rows with 62.6% precision but only 13.9% of the true noisy rows, so the flagged count says little about the total. In that simulation drop, relabel and no cleaning gave the same clean-test accuracy (0.764 to 0.765), because a low-capacity linear model on balanced data is quite robust to 5% noise; the gain from cleaning shows up in evaluation labels and in flexible models that memorise noise, not here. Dropping or relabelling would have touched 127 rows that were actually correct.

**Follow-ups:**
- Would you use soft down-weighting? Yes when review is not possible: weight a row by 1 minus the estimated probability that its label is wrong, so uncertain rows count less without being deleted.
- How do you get an unbiased noise estimate cheaply? A random audit sample, stratified by class and by predicted confidence, with a second reviewer on disputed rows.
- What if the 38% valid flagged rows are one class? Then the filter is biased against that class; check the flagged share per class before acting.

**Common mistakes:** Treating the flagged share as the noise rate. Skipping the unflagged audit. Dropping valid hard examples. Relabelling with model predictions. Cleaning training data but not the test set. Reporting no intervals.

### Q35 ⭐⭐ 🟡 A 12-class ticket classifier is trained on 100,000 tickets where the biggest class holds 40% and five classes each hold under 1,000 tickets. Overall accuracy is 91% but the team says the small classes are what the business cares about. Explain which metrics and averaging you would use, how you would handle the rare classes, and how you would report results.
**Asked at:** Imbalanced-data and fraud-evaluation guides (techinterview.org 'Handling Imbalanced Datasets in Machine Learning', Dataford fraud-evaluation prompts such as 'how do you evaluate a fraud detection model on imbalanced data', a KDnuggets piece on SMOTE misuse, a Coresignal 'class imbalance interview trap' post); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Accuracy of 91% is mostly the big classes, so I would report per-class precision, recall and F1, summarise with macro-averaged F1 (every class counts equally), and handle the five rare classes with stratified splits, class weights or resampling inside training, and class-specific thresholds.

**Clarifying questions:**
- Which classes matter most, and is a miss in a rare class more costly than a false alarm? Why: it decides between recall-first and precision-first per class.
- Are the five rare classes distinct from the others, or do they sit inside a hierarchy (for example sub-types of one parent)? Why: a hierarchy allows a two-stage model and merged reporting.
- Are tickets one label each, or can a ticket have several labels? Why: multi-label needs per-label thresholds and different metrics.
- Is the rare-class share going to change in production? Why: precision depends on the class mix, so a new mix changes the numbers.
- How many examples of each rare class are in the test set? Why: under 100 test examples means a very wide interval.

**Approach:**
1. Show why 91% hides the problem: always predicting the biggest class gets 40% (the 40% class), and the rare classes are 3.5% of tickets, so even getting all of them wrong costs only 3.5 points of accuracy.
2. Get the full picture: a 12x12 confusion matrix, then per-class precision, recall and F1. Look at where each rare class goes (usually into one or two big neighbours).
3. Pick the averaging on purpose. Micro-F1 equals accuracy for single-label problems, so it adds nothing. Macro-F1 is the plain mean over classes and treats a 500-ticket class like a 40,000-ticket class. Weighted-F1 follows class size, so it looks like accuracy. Report macro-F1 as the headline and per-class numbers next to it; add macro-recall over the rare classes as the business number.
4. Fix the evaluation first: stratified split (and stratified cross-validation) so every class appears in every fold; a test set with enough examples per rare class; intervals on every rare-class recall.
5. Handle the rare classes in training: class weights (or sampling) inside the training folds only; threshold or prior shift per class using validation data; more labelled examples for the rare classes (active learning on low-confidence tickets); merge classes only if the business agrees.
6. Calibrate and re-check. Class weights distort probabilities, so recalibrate if the scores are used as probabilities.
7. Report as a table: class, support, precision, recall, F1, with intervals for the rare classes, plus macro-F1 and accuracy. Say clearly which numbers are weak.

**Metrics:**
- Precision_k = TP_k / (TP_k + FP_k) (correct predictions for class k / all tickets predicted as k); recall_k = TP_k / (TP_k + FN_k); F1_k = 2 x P x R / (P + R).
- Macro-F1 = mean of F1_k over the 12 classes. Weighted-F1 = sum of support_k x F1_k / total. Micro-F1 = overall accuracy.
- Rare-class macro-recall = mean recall over the five rare classes.
- Guardrails: confusion into the biggest class, number of test examples per rare class, and the interval on each rare recall.

**Risks:**
- Reporting weighted-F1 or accuracy and believing it speaks for the rare classes.
- Class weights that raise rare recall but ruin rare precision, so the support team gets flooded.
- Rare classes with 100 or fewer test examples: a recall of 0.35 may mean 0.27 to 0.44.
- Resampling before the split (the same leak as in Book 6 Part 3 Q2).
- Rare classes that are different in kind from their look-alikes (new product names, new languages), so more weight does not fix them.

**What the interviewer scores:**
- Strong: explains macro vs weighted vs micro and why micro equals accuracy here.
- Strong: asks which rare classes matter and reports per-class numbers with intervals.
- Strong: handles rare classes in the training folds only and tunes per-class thresholds on validation.
- Weak: "91% is good", or "use SMOTE" with no metric and no split discipline.
- Cross-reference: Book 1 Part 3 has "Multiclass metrics: macro vs micro vs weighted F1. When do you pick each?" and "How do you extend ROC-AUC and calibration to multiclass problems (one-vs-rest, one-vs-one, macro/weighted)?".

**Example:** (illustrative numbers) Class sizes 40,000, 15,000, 13,000, 11,000, 9,000, 5,000, 3,500 and the five rare ones 900, 800, 700, 600, 500 (total 100,000, so the rare five are 3.5%). The big classes have recall about 0.83 to 0.94 and the rare ones 0.55, 0.50, 0.45, 0.40 and 0.35. Accuracy comes to 91.0%, macro-F1 only 0.705, and the macro-recall over the rare five is 0.45. If the rare classes are all wrong, accuracy loses at most 3.5 points. Weak answer: "91% accuracy, good enough." Strong answer: "Accuracy hides the rare classes. I would report per-class P/R/F1 and macro-F1, then fix the rare classes with stratified folds, class weights and thresholds."

**Code:**
```python
import numpy as np
from scipy.stats import beta


# 12 classes, 100,000 tickets; sizes as in the prompt (invented split of the rest)
sizes = np.array([40000, 15000, 13000, 11000, 9000, 5000, 3500, 900, 800, 700, 600, 500])
assert sizes.sum() == 100_000 and sizes[0] / sizes.sum() == 0.40 and (sizes[7:] < 1000).all() and len(sizes) == 12
recall = np.array([0.945, 0.935, 0.925, 0.915, 0.905, 0.885, 0.83, 0.55, 0.50, 0.45, 0.40, 0.35])
rng = np.random.default_rng(35)
K = 12
C = np.zeros((K, K), int)                                   # confusion matrix: rows true, cols predicted
for i in range(K):
    C[i, i] = round(sizes[i] * recall[i])
    miss = sizes[i] - C[i, i]
    w = np.array([0.5 if j == 0 else 0.5 / (K - 2) for j in range(K)]); w[i] = 0
    w = w / w.sum()
    add = np.floor(miss * w).astype(int); add[0 if i else 1] += miss - add.sum()
    C[i] += add
    assert C[i].sum() == sizes[i]
tp = np.diag(C); support = C.sum(1); predicted = C.sum(0)
prec = tp / predicted; rec = tp / support; f1 = 2 * prec * rec / (prec + rec)
acc = tp.sum() / C.sum()
print("accuracy (= micro-F1):", round(float(acc), 4))
print("macro-F1 over all 12:", round(float(f1.mean()), 3), "  weighted-F1:", round(float((f1 * support).sum() / support.sum()), 3))
print("macro recall over the 5 rare classes:", round(float(rec[7:].mean()), 3), "  rare-class share of tickets:", round(support[7:].sum() / C.sum(), 3))
for i in range(K):
    print(f"class {i+1:2d} n={support[i]:6d} precision={prec[i]:.2f} recall={rec[i]:.2f} F1={f1[i]:.2f}")
assert abs(acc - 0.91) < 0.01
assert f1.mean() < acc - 0.05
# a 'predict the biggest class' baseline
print("baseline accuracy, always predict class 1:", sizes[0] / sizes.sum())
# rare classes: how well can recall be measured? Clopper-Pearson for class 12 if the test set holds 25% of it
n12 = int(support[11] * 0.25); k12 = round(n12 * rec[11])
lo, hi = beta.ppf(0.025, k12, n12 - k12 + 1), beta.ppf(0.975, k12 + 1, n12 - k12)
print(f"class 12 test positives {n12}, recall {k12/n12:.2f}, 95% CI {lo:.2f}-{hi:.2f}")
```

**Output (my run):**
```text
accuracy (= micro-F1): 0.9102
macro-F1 over all 12: 0.705   weighted-F1: 0.912
macro recall over the 5 rare classes: 0.45   rare-class share of tickets: 0.035
class  1 n= 40000 precision=0.92 recall=0.94 F1=0.93
class  2 n= 15000 precision=0.97 recall=0.94 F1=0.95
class  3 n= 13000 precision=0.96 recall=0.93 F1=0.94
class  4 n= 11000 precision=0.95 recall=0.92 F1=0.93
class  5 n=  9000 precision=0.94 recall=0.91 F1=0.92
class  6 n=  5000 precision=0.90 recall=0.89 F1=0.89
class  7 n=  3500 precision=0.85 recall=0.83 F1=0.84
class  8 n=   900 precision=0.49 recall=0.55 F1=0.52
class  9 n=   800 precision=0.44 recall=0.50 F1=0.47
class 10 n=   700 precision=0.38 recall=0.45 F1=0.41
class 11 n=   600 precision=0.32 recall=0.40 F1=0.35
class 12 n=   500 precision=0.25 recall=0.35 F1=0.29
baseline accuracy, always predict class 1: 0.4
class 12 test positives 125, recall 0.35, 95% CI 0.27-0.44
```
The text above matches this run: accuracy 0.9102, macro-F1 0.705 and weighted-F1 0.912, so weighted-F1 repeats the accuracy story while macro-F1 shows the gap. The rare five hold 3.5% of the tickets and have a macro recall of 0.45. An always-class-1 baseline gets 0.40. For class 12 a test set with 125 examples (25% of its 500 tickets) gives recall 0.35 with a 95% interval of 0.27 to 0.44.

**Follow-ups:**
- Why not only macro-F1? It hides which class is weak and gives equal weight to a class the business may not care about; use it as the headline and keep the table.
- Class weights or oversampling? Weights are simpler and keep every row; oversampling duplicates rows and can overfit if done before the split. Try weights first, and do either inside the training folds only.
- How do you handle a class with 100 training tickets? Combine active learning, simple rule features, hierarchical grouping and maybe a retrieval or LLM-assisted first pass, and be honest about the interval.

**Common mistakes:** Reporting accuracy or weighted-F1 as the headline. Calling micro-F1 a different number from accuracy in single-label tasks. Oversampling before the split. Skipping stratification. No intervals on rare classes.

### Q36 ⭐⭐ 🟡 A test set holds 20,000 rows with only 20 positives, and the model catches 14 of them (recall 70%). The team wants to say recall is 70% and to compare it with an older model that caught 12. Explain how uncertain these figures are, how you would build the test set or compare the models, and what you would claim.
**Asked at:** Imbalanced-data and fraud-evaluation guides (techinterview.org 'Handling Imbalanced Datasets in Machine Learning', Dataford fraud-evaluation prompts such as 'how do you evaluate a fraud detection model on imbalanced data', a KDnuggets piece on SMOTE misuse, a Coresignal 'class imbalance interview trap' post); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** With only 20 positives, "70% recall" really means somewhere between about 46% and 88%, and 14 versus 12 caught is no evidence the new model is better, so I would claim nothing yet and get more positives, or run a paired comparison on the same positives.

**Clarifying questions:**
- Are the 20 positives independent cases, or several rows from the same customers or events? Why: clustered positives mean the real sample size is even smaller.
- Did both models score the same 20,000 rows at the same threshold or the same alert budget? Why: only then is a paired comparison possible, and the thresholds must be comparable.
- How many positives could we get from other periods, other regions or labelling backlog? Why: the number of positives, not the number of rows, controls the precision of recall.
- Was the threshold chosen on this test set? Why: if yes, 70% is optimistic.
- What decision depends on this: a launch, a rollback, a report? Why: it sets how much evidence is enough.

**Approach:**
1. Compute the interval, not just the point. For 14 of 20, the exact (Clopper-Pearson) 95% interval is about 0.46 to 0.88; for 12 of 20 it is about 0.36 to 0.81. The two overlap almost completely.
2. Compare the models on the same positives (paired). Only positives where the two models differ matter: new-only catches (b) and old-only catches (c). Use an exact McNemar test (a sign test on b versus c). Best case, where the new model catches the old model's 12 plus 2 more, gives b = 2, c = 0 and a two-sided p-value of 0.5. A more typical split gives p near 0.7.
3. Say what the data supports: the new model is not shown to be better, and not shown to be worse. Also compare precision or false-alarm count at the same recall, since those use the 19,980 negatives and are better estimated.
4. Build a better test set: more positives. For 5 points of half-width around 70% you need about 323 positives. At a 0.1% rate that is 323,000 rows, so collect positives over a longer period, pool several time windows or regions, or label more of the backlog.
5. Enrich the test set, with care: keep all positives and a random share of negatives (say 5%), then weight each kept negative by 20 when computing precision and false-alarm rates. This shrinks the set and the labelling cost, but it does not narrow the recall interval, which depends only on the number of positives.
6. Use cross-validated or bootstrap out-of-fold scores across all data to get more positives into evaluation, and keep a time-based final check.
7. Claim carefully: "On a small test with 20 positives, the new model caught 14 and the old 12; this is not statistically distinguishable. We need about 300 positives to resolve a 10-point difference" and say what extra evidence you will gather.

**Metrics:**
- Recall = positives caught / positives (14 / 20). Report with an exact 95% interval.
- Paired comparison = counts of b (new-only) and c (old-only) caught positives, with an exact McNemar p-value, and a bootstrap interval for the difference in recall.
- False positive count or precision at the matched threshold, using the weights if negatives were subsampled.
- Guardrail: number of positives per slice; if a slice has under 30, do not report slice recall.

**Risks:**
- Choosing the winner on 2 extra catches and shipping on it.
- Using an unpaired test (Fisher) when the same rows are scored by both models, which wastes information (here Fisher gives 0.741 and McNemar 0.688 for the 4-versus-2 split, so the conclusion is the same, but with other splits they can differ).
- Tuning the threshold on the same 20 positives.
- Subsampling negatives without reweighting, so precision looks far too good.
- Treating the narrower interval from a bigger negative set as if it narrowed recall.

**What the interviewer scores:**
- Strong: states the interval (about 46% to 88%) and says the difference of 2 is within noise.
- Strong: proposes a paired test and a plan for more positives (count them, not rows).
- Strong: knows enrichment needs reweighting and does not shrink the recall interval.
- Weak: "70% beats 60%", or "add more negatives".
- Cross-reference: Book 1 Part 3 has "How do you compare two classifiers statistically? Bootstrap CI for AUC, DeLong test, McNemar test."

**Example:** (illustrative numbers) New model catches 14 of 20 (70%), old catches 12 (60%). If 10 of the positives are caught by both, then new-only = 14 - 10 = 4 and old-only = 12 - 10 = 2. Under the null each discordant case is a coin flip, so the exact two-sided p-value for 4 versus 2 is about 0.69. Even if the old model's 12 are all inside the new model's 14 (2 versus 0) the p-value is 0.5. Weak answer: "recall rose from 60% to 70%, ship it." Strong answer: "20 positives cannot tell 70% from 60%; I would pair the models, report intervals and collect about 300 positives."

**Code:**
```python
import math
import numpy as np
from scipy.stats import beta, binom, fisher_exact

def cp(k, n, a=0.05):
    return (beta.ppf(a / 2, k, n - k + 1) if k > 0 else 0.0, beta.ppf(1 - a / 2, k + 1, n - k) if k < n else 1.0)
def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h

# 1) how uncertain is 14 of 20 and 12 of 20?
for name, k in [("new", 14), ("old", 12)]:
    lo, hi = cp(k, 20); wl, wh = wilson(k, 20)
    print(f"{name}: recall {k/20:.2f}  exact 95% CI {lo:.3f}-{hi:.3f}   Wilson {wl:.3f}-{wh:.3f}")
assert round(cp(14, 20)[0], 2) == 0.46 and round(cp(14, 20)[1], 2) == 0.88

# 2) same 20 positives for both models -> paired comparison; only discordant positives matter
# best case for the new model: it catches the 12 the old one caught plus 2 more -> b=2, c=0
b, c = 2, 0
p_exact = 2 * binom.cdf(min(b, c), b + c, 0.5)          # two-sided exact McNemar (sign test)
print("best case b=2,c=0: two-sided exact McNemar p =", p_exact)
assert p_exact == 0.5
# a more typical split: new catches 14, old 12, overlap 10 -> new-only 4, old-only 2
b, c = 4, 2
p2 = min(1.0, 2 * binom.cdf(min(b, c), b + c, 0.5))
print("overlap 10: new-only 4, old-only 2: p =", round(float(p2), 3))
# unpaired Fisher (wrong test for same rows) is also nowhere near significant
print("unpaired Fisher on 14/20 vs 12/20: p =", round(float(fisher_exact([[14, 6], [12, 8]])[1]), 3))

# 3) how many positives would you need? half-width 0.05 around recall 0.7
n_pos = math.ceil(1.96 ** 2 * 0.7 * 0.3 / 0.05 ** 2)
base = 20 / 20_000
print("positives for +-5 points on recall 0.7:", n_pos, " rows needed at the current 0.1% rate:", round(n_pos / base))
assert n_pos == 323 and round(n_pos / base) == 323_000
# detecting 0.70 vs 0.60 paired, with discordance ~25%: rough n via normal approx on b-c
# simulate: how often does a truly WORSE (0.60) model look at least as good as a 0.70 one on 20 positives?
rng = np.random.default_rng(36)
a = rng.random((200_000, 20)) < 0.70
b_ = rng.random((200_000, 20)) < 0.60
look = (a.sum(1) <= b_.sum(1)).mean()
print("P(truly worse model catches >= as many of 20) :", round(float(look), 3))
assert 0.25 < look < 0.45
# 4) fix the test set: enrich positives (stratified sampling) and reweight negatives
neg_keep = 0.05                                           # keep 5% of negatives
pos_total, neg_total = 20, 19_980
neg_rows = round(neg_total * neg_keep)
print("enriched set: rows", pos_total + neg_rows, " positive share", round(pos_total / (pos_total + neg_rows), 3), " weight on each negative", 1 / neg_keep)
# but recall CI width does not shrink: it depends on positives, not on negatives
assert cp(14, 20)[1] - cp(14, 20)[0] > 0.35
# 5) a larger positive pool: 200 positives, same 70% vs 60% -> now separable?
print("200 positives: 140 vs 120 caught, exact CIs", [tuple(round(float(x), 3) for x in cp(k, 200)) for k in (140, 120)])
```

**Output (my run):**
```text
new: recall 0.70  exact 95% CI 0.457-0.881   Wilson 0.481-0.855
old: recall 0.60  exact 95% CI 0.361-0.809   Wilson 0.387-0.781
best case b=2,c=0: two-sided exact McNemar p = 0.5
overlap 10: new-only 4, old-only 2: p = 0.688
unpaired Fisher on 14/20 vs 12/20: p = 0.741
positives for +-5 points on recall 0.7: 323  rows needed at the current 0.1% rate: 323000
P(truly worse model catches >= as many of 20) : 0.308
enriched set: rows 1019  positive share 0.02  weight on each negative 20.0
200 positives: 140 vs 120 caught, exact CIs [(0.631, 0.763), (0.529, 0.668)]
```
The text above matches this run: the exact interval for 14 of 20 is 0.457 to 0.881 and for 12 of 20 is 0.361 to 0.809. The best case for the new model (b = 2, c = 0) gives p = 0.5, the 4-versus-2 split gives 0.688, and an unpaired Fisher test gives 0.741. About 323 positives (323,000 rows at the current 0.1% rate) are needed for a plus or minus 5-point interval at recall 0.7. In a simulation, a model with true recall 0.60 catches at least as many of 20 positives as a model with true recall 0.70 about 30.8% of the time. Enriching to 5% of negatives gives 1,019 rows with 2.0% positives and a weight of 20 per negative, but the recall interval stays as wide. With 200 positives (140 vs 120) the intervals are 0.631 to 0.763 and 0.529 to 0.668, still touching, which is why a paired test on the same rows matters.

**Follow-ups:**
- Could you bootstrap the 20? You can, but the bootstrap of 20 points is just as uncertain and tends to be too narrow at the extremes; the exact interval is safer.
- What if positives are rare and cannot be collected? Use all historical positives with cross-validation, pool windows, use a proxy label with a documented bias, and state a wide interval in the claim.
- Can I trust ROC-AUC or PR-AUC more? They also depend on the 20 positives, so the same uncertainty applies; report their bootstrap interval.

**Common mistakes:** Quoting 70% without an interval. Reading 14 versus 12 as a win. Using an unpaired test for paired data. Tuning the threshold on the test set. Subsampling negatives without weights. Confusing rows with positives.

### Q37 ⭐⭐ 🟡 A feature is missing in 15,000 of 100,000 rows (15%) and is strongly related to two other columns. The team debates median imputation, iterative model-based imputation and a tree model that handles missing values natively. Explain how you would choose between them, how you would judge imputation quality, and how you would keep imputation inside the cross-validation loop.
**Asked at:** Missing-data interview explainers (a PrachHub 'Missing Data, Imputation, And Selection Bias' concept page, ydata.ai 'understanding missing data mechanisms', a Towards Data Science 'Talking About Missing Data' article, a Daily Dose of Data Science post on three types of missing values); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** I would choose by testing on the data, not by taste: mask known values in the same pattern as the real missingness, compare imputers on error and on the downstream model, add a missing-indicator, and fit every imputer inside the training folds only.

**Clarifying questions:**
- Why is the value missing: not collected, not applicable, or hidden because of the outcome? Why: it decides whether missing means "unknown" or carries signal, and whether imputing is safe.
- Does the missingness depend on other columns (the prompt says the feature is strongly related to two columns, which suggests it can be predicted from them)? Why: if so the data are plausibly missing at random given those columns, and model-based imputation works.
- Will the same missingness pattern appear at serving time, and how are missing values fed at inference? Why: an imputation that needs many other rows or the target cannot run in production.
- What model will use the feature: linear, tree boosting, neural? Why: trees can often use missing values directly, linear models need numbers.
- Is the goal prediction, or a coefficient or causal estimate? Why: for inference, multiple imputation with proper uncertainty matters; for prediction, a good point fill plus an indicator is usually enough.

**Approach:**
1. Diagnose the mechanism. Compare missing and observed rows on the other columns, and model the missing flag from those columns. If it is predictable from observed columns (as here: missing rate rises from 3% to 34% across quartiles of one column in my run), it is not completely random. Missing at random versus missing because of the value itself cannot be told apart from the data alone; that needs domain knowledge.
2. List candidates: median fill plus an indicator; regression or iterative (chained-equations style) imputation from the related columns, plus an indicator; a model that handles missing values natively (gradient-boosted trees learn which side of a split missing rows go to).
3. Judge imputation quality in two ways. Direct: hide some known values in the same pattern as the real missingness, impute, and measure the error (RMSE) against the hidden truth, and compare the distribution shape. Downstream: train the final model on each version and compare AUC or log loss on a held-out set, especially on rows that were missing.
4. Keep imputation inside the cross-validation loop. For each fold, fit the imputer on the training part only (the median, the regression coefficients), then apply it to the validation part. In scikit-learn this is a Pipeline with the imputer as the first step; the same applies to scalers and target encoders. Never use the target to impute.
5. Add a missing indicator when missingness may carry signal, and test whether it helps.
6. For uncertainty, use multiple imputation (several imputed copies, pool the results) if you need standard errors; for pure prediction a single good imputation plus an indicator is usually enough.
7. Check the serving path: the imputer is saved with the model, handles one row at a time, and has a fallback value for new missing patterns. Monitor the missing rate in production.

**Metrics:**
- Imputation RMSE = square root of the mean squared difference between imputed and true values on the masked known cells, compared with the standard deviation of the feature.
- Downstream AUC (or log loss) on a clean held-out set, overall and on rows that were missing.
- Calibration and stability: the spread of the metric across folds and seeds.
- Guardrail: the missing rate and the imputed-value distribution at serving versus training.

**Risks:**
- Fitting the imputer on all data before the split (mild for a median, severe for target-based fills).
- Using the target to impute: offline metrics rise, serving cannot do it.
- Median fill squeezes the variance and breaks the relationship with the related columns.
- Single imputation understates uncertainty for inference.
- Masking values at random when the real missingness is not random, so the quality check is too optimistic.

**What the interviewer scores:**
- Strong: asks why the value is missing and tests candidates by masking known values under a realistic pattern.
- Strong: puts the imputer inside each training fold (a Pipeline) and never uses the target.
- Strong: mentions the missing indicator and that trees can use missingness directly, with a note that the choice should still be tested.
- Weak: "always use the median" or "iterative imputation is always better".
- Cross-reference: Book 1 Part 1 has "How do you handle missing values? Compare dropping, mean/median, model-based imputation and missing-indicator features; when is missingness informative?", Book 1 Part 4 has "How do tree-based models handle missing values, categorical variables, outliers and unscaled features?", and Book 6 Part 3 Q15 "A feature's missing values were filled with the mean target value within each city..." covers the target-leak version.

**Example:** (illustrative numbers) 100,000 rows, a feature missing in 15,000 (15%). The feature has a standard deviation of 2.3 and is related to two other columns. Median fill guesses the same number for everyone, so its error on hidden values is about as large as the standard deviation (2.4 in my run). A regression from the two related columns brings the error to about 0.7. Weak answer: "median is simple and robust, use it." Strong answer: "mask some known values, compare errors and downstream AUC, keep it in the CV loop, add an indicator."

**Code:**
```python
import numpy as np
from scipy.stats import rankdata

rng = np.random.default_rng(37)
n = 100_000
x1 = rng.normal(size=n); x2 = rng.normal(size=n)
z = 2.0 * x1 - 1.0 * x2 + rng.normal(scale=0.7, size=n) + 3.0          # feature with missing values; strongly related to x1, x2
logit = 0.9 * (z - 3.0) + 0.5 * x1 - 0.3 * x2 - 1.0
y = (rng.random(n) < 1 / (1 + np.exp(-logit))).astype(int)
# MAR: missingness depends on x1, x2 (observed), tuned to 15%
t = -2.3 + 1.2 * x1 + 0.8 * x2
m = rng.random(n) < 1 / (1 + np.exp(-t))
print("missing share:", round(float(m.mean()), 3), " mean z when missing / observed:", round(float(z[m].mean()), 2), round(float(z[~m].mean()), 2))
assert 0.14 < m.mean() < 0.16

def auc(y, s):
    r = rankdata(s); n1 = int(y.sum()); return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * (len(y) - n1))
def fit(F, t, iters=20, l2=1e-3):
    b = np.zeros(F.shape[1])
    for _ in range(iters):
        q = 1 / (1 + np.exp(-F @ b)); g = F.T @ (q - t) + l2 * b
        H = (F * (q * (1 - q))[:, None]).T @ F + l2 * np.eye(len(b)); b -= np.linalg.solve(H, g)
    return b
def lin_fit(A, t): return np.linalg.lstsq(A, t, rcond=None)[0]

# imputers: each is fitted on a training part only, then applied to any part
def make_median(Xa, za, ma, ya=None):
    med = np.median(za[~ma])
    return lambda Xb, zb, mb: (np.where(mb, med, zb), mb.astype(float))
def make_regress(Xa, za, ma, ya=None):
    A = np.c_[Xa, np.ones(len(Xa))]; beta_ = lin_fit(A[~ma], za[~ma])
    return lambda Xb, zb, mb: (np.where(mb, np.c_[Xb, np.ones(len(Xb))] @ beta_, zb), mb.astype(float))
def make_leaky_target(Xa, za, ma, ya):                       # includes the TARGET in the imputation model
    A = np.c_[Xa, ya, np.ones(len(Xa))]; beta_ = lin_fit(A[~ma], za[~ma])
    return lambda Xb, zb, mb, yb: (np.where(mb, np.c_[Xb, yb, np.ones(len(Xb))] @ beta_, zb), mb.astype(float))

X = np.c_[x1, x2]
tr = np.arange(n) < 70_000; te = ~tr
res = {}
# a) imputation quality on rows where z is known: mask them under the same mechanism, impute, score RMSE
known = ~m
# hide a further share of the known values with the same MAR mechanism
msk = known & (rng.random(n) < 1 / (1 + np.exp(-(t + 0.0))))
for name, mk in [("median", make_median), ("regression", make_regress)]:
    imp = mk(X[tr], z[tr], m[tr] | msk[tr])
    zi, _ = imp(X[te], z[te], msk[te] | m[te])
    err = zi[msk[te]] - z[te][msk[te]]
    print(f"imputation RMSE on masked known values, {name:10s}: {np.sqrt((err ** 2).mean()):.3f}   (std of z {z.std():.2f})")

# b) downstream AUC, imputer fitted on the training part only
def downstream(mk, add_flag=True):
    imp = mk(X[tr], z[tr], m[tr])
    ztr, ftr = imp(X[tr], z[tr], m[tr]); zte, fte = imp(X[te], z[te], m[te])
    cols = lambda Xb, zb, fb: np.c_[Xb, zb, fb] if add_flag else np.c_[Xb, zb]
    Ftr = np.c_[cols(X[tr], ztr, ftr), np.ones(tr.sum())]; Fte = np.c_[cols(X[te], zte, fte), np.ones(te.sum())]
    b = fit(Ftr, y[tr]); sc = Fte @ b; return auc(y[te], sc), auc(y[te][m[te]], sc[m[te]])
bf = fit(np.c_[X[tr], z[tr], np.ones(tr.sum())], y[tr]); sf = np.c_[X[te], z[te], np.ones(te.sum())] @ bf
full, full_m = auc(y[te], sf), auc(y[te][m[te]], sf[m[te]])
print("AUC with z fully observed (ceiling): all test rows", round(float(full), 4), "  rows that are missing in practice", round(float(full_m), 4))
for name, mk in [("median", make_median), ("regression", make_regress)]:
    for flag in (False, True):
        a_all, a_m = downstream(mk, flag); print(f"AUC, {name:10s} flag={flag!s:5s}: all rows {a_all:.4f}   missing-rows only {a_m:.4f}")
# c) the leak: impute using the target, on both parts (fine offline, impossible at serving time)
imp = make_leaky_target(X[tr], z[tr], m[tr], y[tr])
ztr, ftr = imp(X[tr], z[tr], m[tr], y[tr]); zte, fte = imp(X[te], z[te], m[te], y[te])
b = fit(np.c_[X[tr], ztr, ftr, np.ones(tr.sum())], y[tr])
sl = np.c_[X[te], zte, fte, np.ones(te.sum())] @ b
leak_auc, leak_m = auc(y[te], sl), auc(y[te][m[te]], sl[m[te]])
print("AUC with target-aware imputation (leak): all rows", round(float(leak_auc), 4), "  missing-rows only", round(float(leak_m), 4))
assert leak_m > full_m + 0.01
# d) imputer fitted on all rows vs inside the training fold: for a label-free imputer the gap is tiny, still do it inside
imp_all = make_median(X, z, m)
zall, _ = imp_all(X, z, m)
print("median fitted on all rows:", round(float(np.median(z[~m])), 4), " fitted on train part:", round(float(np.median(z[tr & ~m])), 4))
print("MAR check: missing rate in x1 quartiles:", [round(float(m[(x1 >= lo) & (x1 < hi)].mean()), 3) for lo, hi in zip(np.quantile(x1, [0, .25, .5, .75]), np.r_[np.quantile(x1, [.25, .5, .75]), 1e9])])
```

**Output (my run):**
```text
missing share: 0.151  mean z when missing / observed: 4.07 2.82
imputation RMSE on masked known values, median    : 2.412   (std of z 2.34)
imputation RMSE on masked known values, regression: 0.694   (std of z 2.34)
AUC with z fully observed (ceiling): all test rows 0.9049   rows that are missing in practice 0.8972
AUC, median     flag=False: all rows 0.8988   missing-rows only 0.8845
AUC, median     flag=True : all rows 0.8998   missing-rows only 0.8846
AUC, regression flag=False: all rows 0.9031   missing-rows only 0.8847
AUC, regression flag=True : all rows 0.9031   missing-rows only 0.8847
AUC with target-aware imputation (leak): all rows 0.9069   missing-rows only 0.9126
median fitted on all rows: 2.8294  fitted on train part: 2.8376
MAR check: missing rate in x1 quartiles: [0.031, 0.082, 0.153, 0.336]
```
The text above matches this run: 15.1% of the rows are missing, with the missing rate rising from 3.1% to 33.6% over quartiles of x1, so the pattern is predictable from observed columns. Median imputation has an error of 2.412 (the feature's standard deviation is 2.34), regression imputation 0.694. The downstream effect on AUC is small here because the feature is nearly a function of the two other columns and the model is linear: ceiling 0.9049 with the true values, 0.8988 (median), 0.9031 (regression); on the rows that were actually missing it is 0.8972 (ceiling), 0.8845 (median) and 0.8847 (regression). The missing indicator adds almost nothing (0.8998 vs 0.8988) because this mechanism depends on observed columns only. Target-aware imputation scores 0.9126 on the missing rows, above the 0.8972 ceiling you would get with the real values, which proves it is a leak that cannot be reproduced in production. The median fitted on all rows (2.8294) versus on the training part (2.8376) differs a little, which shows why fitting inside the fold is a habit, not a big effect for a median.

**Follow-ups:**
- Will the native tree handling just win? It often does when missingness carries signal, since it learns a branch for missing, but it is not guaranteed and I could not run one here with the standard library; test it against imputed versions on the same folds.
- Why add an indicator? If the reason for missing is related to the outcome, the flag carries information that any fill removes; test it and keep it only if it helps.
- When do you need multiple imputation? When you report coefficients or intervals and need honest uncertainty; for prediction alone, it is rarely worth the cost.

**Common mistakes:** Fitting the imputer on the full data before cross-validation. Using the target to fill. Judging imputation only by its RMSE and not by the downstream metric. Hiding values at random when the real pattern is not random. Forgetting the serving path.

### Q38 ⭐⭐ 🔴 An audit of 2,000 random transactions with intensive investigation found 25 frauds, but only 20 of them carry a fraud label in the system, while the labelled fraud rate overall is 1%. Explain what kind of label noise this is, how it affects the training, the measured recall and the measured precision, and how you would estimate and handle it.
**Asked at:** Noisy-label and annotator-disagreement material (Tanno et al., CVPR 2019 on annotator confusion matrices; a Codemia data-labelling course page); research and course pages rather than interview banks, so the scenario is partly editor-designed; search snippets only, not opened
**Say this first (1 line):** This is one-sided, class-conditional label noise (real frauds missing a fraud label, about 20% of them), probably not random, so the model learns to treat hidden fraud as normal, measured recall looks better than the truth, measured precision looks worse, and I would fix it with an audit-based estimate and review of the unlabelled-but-suspicious cases.

**Clarifying questions:**
- How do frauds get a label today (chargebacks, rules, analyst review)? Why: it tells me which kinds of fraud are systematically missing.
- Did the audit also check the 1,975 non-fraud rows for false fraud labels, and were any of the 20 labelled rows wrong? Why: the one-sided story needs "no false positives", which I should verify.
- Was the audit sample truly random and the investigation blind to the system label? Why: a biased audit biases the 80% figure.
- How is model performance reported today, and how is the review queue chosen from the scores? Why: the same missing labels may bias both metrics and training.
- What is the business cost of an undetected fraud versus a false alert? Why: it sets how much effort goes into recovering missing labels.

**Approach:**
1. Do the audit arithmetic. 25 of 2,000 are truly fraud (1.25%); 20 carry a label (1.0%, matching the system's overall 1% labelled rate). So P(label = fraud | fraud) is 20 / 25 = 80%, with a wide 95% interval of about 59% to 93%. If none of the other 1,975 rows has a false fraud label, then P(label = fraud | not fraud) is about 0.
2. Name it. This is asymmetric, class-conditional label noise where positives are missing (a false-negative-only pattern, like positive-unlabelled data). It is probably not completely random, because the frauds nobody noticed are different from the frauds somebody did.
3. Effect on training. The model sees about 20% of the fraud as "legitimate", so it learns that hidden-fraud patterns are normal and gives them low scores. Overall prevalence is understated (1.0% versus 1.25%), probabilities are too low, and recall on the hidden kind of fraud is poor.
4. Effect on measured recall. Recall measured against labels counts only labelled frauds, which are the ones the existing process notices and the model resembles. Measured recall is therefore too high compared with the true recall (in my run, 0.277 measured versus 0.236 true).
5. Effect on measured precision. A true fraud the model flags but nobody labelled is scored as a false positive, so measured precision is too low (0.715 versus 0.763 true in my run).
6. Estimate it properly. Keep running a random investigated audit and estimate label sensitivity overall and by fraud type, channel or amount band. Do not apply one global factor: the sensitivity among the frauds the model catches (0.937 in my run) is much higher than among all frauds (0.801).
7. Handle it. For evaluation, use audited samples with weights, not the system labels alone. For training, send high-score unlabelled cases to investigation (active relabelling), treat labels as positive-unlabelled (weight unlabelled rows less or use a PU loss), add hidden-pattern detectors, and track label sensitivity as a monitored number.

**Metrics:**
- Label sensitivity = labelled frauds / true frauds in the audit (20 / 25 = 0.80), with an exact interval and by segment.
- Measured precision = flagged rows with a fraud label / flagged rows; true precision = flagged true frauds / flagged rows (needs investigation of flagged rows).
- Measured recall = flagged labelled frauds / labelled frauds; true recall = flagged true frauds / all true frauds (needs the audit).
- Guardrails: audit sample size, the labelled-fraud rate over time (a drop can be a labelling delay, not less fraud), and recall on frauds that were found late.

**Risks:**
- Reporting recall from system labels only: it rewards the model for resembling the labelling process.
- Believing precision is low and tightening the threshold, which hides real fraud.
- Applying a single correction factor such as dividing recall by 0.8.
- An audit of only 25 frauds: the sensitivity interval is wide, so be careful with segment cuts.
- Training on these labels and then evaluating on the same label source: the loop reinforces the blind spot (see also Book 6 Part 3 Q29 "Only the 20,000 of 1,000,000 transactions (2%) flagged by old rules were reviewed by investigators...").

**What the interviewer scores:**
- Strong: names it as one-sided, class-conditional (and probably not random) noise and computes 80% from the audit.
- Strong: states the direction of each bias (recall too high, precision too low, prevalence too low) and why.
- Strong: proposes a random audit, segment-level sensitivity, and review of high-score unlabelled cases, not one global fudge factor.
- Weak: "label noise is symmetric, so ignore it", or "just scale recall by 1.25".
- Cross-reference: Book 1 Part 3 has "Positive-unlabeled learning and noisy labels: when negatives are really unlabeled, how does that change metrics and training?".

**Example:** (illustrative numbers) The model flags 600 transactions. Labels say 430 of them are fraud (measured precision 71.7%). Investigators check the 170 others and find 28 more true frauds, so true precision is 458 / 600 = 76.3%. Across the whole test set there are 1,925 labelled frauds and 2,420 true frauds (labelled share 79.5%, about 80%); the model catches 430 labelled and 458 true: measured recall 430 / 1,925 = 22.3%, true recall 458 / 2,420 = 18.9%. Weak answer: "recall is 22%, precision is 72%." Strong answer: "labels miss 20% of fraud, so recall is overstated and precision understated; I need an audit-based estimate."

**Code:**
```python
import math
import numpy as np
from scipy.stats import beta

# 1) the audit arithmetic
audit, true_fraud, labelled = 2000, 25, 20
print("true fraud rate in audit:", true_fraud / audit, "  labelled fraud rate in audit:", labelled / audit)
sens = labelled / true_fraud
lo, hi = beta.ppf(0.025, labelled, true_fraud - labelled + 1), beta.ppf(0.975, labelled + 1, true_fraud - labelled)
print("label sensitivity P(label=fraud | fraud):", sens, " 95% CI", round(float(lo), 3), "-", round(float(hi), 3))
assert sens == 0.8 and true_fraud / audit == 0.0125 and labelled / audit == 0.01
# 2) simulate the consequences. Frauds come in two kinds: 'seen' (the old rules catch them, so they get labelled)
#    and 'hidden' (nobody notices them, so they are mostly unlabelled): noise is NOT random.
rng = np.random.default_rng(38)
n = 400_000
X = rng.normal(size=(n, 3))
fraud = rng.random(n) < 0.0125
hidden = fraud & (rng.random(n) < 0.25)
seen = fraud & ~hidden
X[seen, 0] += 2.5; X[seen, 1] += 1.0                  # seen frauds look like the old rules' targets
X[hidden, 2] += 2.5; X[hidden, 1] += 1.0              # hidden frauds look different
lab = np.where(seen, rng.random(n) < 0.96, np.where(hidden, rng.random(n) < 0.28, False))
print("true fraud rate:", round(float(fraud.mean()), 4), " labelled rate:", round(float(lab.mean()), 4), " label sensitivity:", round(float(lab[fraud].mean()), 3))
assert 0.76 < lab[fraud].mean() / 1 < 0.84
tr = np.arange(n) < 250_000; te = ~tr
def fit(F, t, iters=25, l2=1e-3):
    b = np.zeros(F.shape[1])
    for _ in range(iters):
        q = 1 / (1 + np.exp(-F @ b)); g = F.T @ (q - t) + l2 * b
        H = (F * (q * (1 - q))[:, None]).T @ F + l2 * np.eye(len(b)); b -= np.linalg.solve(H, g)
    return b
F = np.c_[X, X ** 2, np.ones(n)]
b = fit(F[tr], lab[tr].astype(float))
s = F[te] @ b
k = 600                                     # review capacity: flag the top 600 test rows
top = np.argsort(-s)[:k]
flag = np.zeros(te.sum(), bool); flag[top] = True
lab_te, fr_te = lab[te], fraud[te]
tp_lab = (flag & lab_te).sum(); tp_true = (flag & fr_te).sum()
print(f"flagged {k}: label-precision {tp_lab/k:.3f}  true-precision {tp_true/k:.3f}")
print(f"label-recall {tp_lab/lab_te.sum():.3f}  true-recall {tp_true/fr_te.sum():.3f}")
print("recall of hidden frauds:", round(float((flag & hidden[te]).sum() / hidden[te].sum()), 3), " recall of seen frauds:", round(float((flag & seen[te]).sum() / seen[te].sum()), 3))
assert tp_true / k > tp_lab / k                     # precision understated
assert tp_lab / lab_te.sum() > tp_true / fr_te.sum()  # recall overstated
# 3) correct the headline with the audit: recall_true = TP_true / fraud_total. Needs an audited estimate of how many are missed
# audit-based estimate on the test slice: investigate a random 2,000 of the test rows
aud = rng.choice(te.sum(), 2000, replace=False)
est_fraud_rate = fr_te[aud].mean(); est_sens = lab_te[aud][fr_te[aud]].mean() if fr_te[aud].any() else float('nan')
print("audit sample: true frauds", int(fr_te[aud].sum()), " labelled", int(lab_te[aud][fr_te[aud]].sum()), " est. sensitivity", round(float(est_sens), 2))
sens_flagged = tp_lab / tp_true
print("label sensitivity among frauds the model flagged:", round(float(sens_flagged), 3), " among all frauds:", round(float(lab_te[fr_te].mean()), 3))
assert sens_flagged > lab_te[fr_te].mean() + 0.1     # the model's catches are the easy-to-label ones, so one global factor misleads
```

**Output (my run):**
```text
true fraud rate in audit: 0.0125   labelled fraud rate in audit: 0.01
label sensitivity P(label=fraud | fraud): 0.8  95% CI 0.593 - 0.932
true fraud rate: 0.0125  labelled rate: 0.0099  label sensitivity: 0.791
flagged 600: label-precision 0.715  true-precision 0.763
label-recall 0.277  true-recall 0.236
recall of hidden frauds: 0.024  recall of seen frauds: 0.302
audit sample: true frauds 23  labelled 18  est. sensitivity 0.78
label sensitivity among frauds the model flagged: 0.937  among all frauds: 0.801
```
The text above matches this run: the audit gives 80% sensitivity with an interval of 0.593 to 0.932. In the simulation (true fraud 1.25%, labelled 0.99%, sensitivity 0.791) the top-600 flags have measured precision 0.715 versus true precision 0.763, and measured recall 0.277 versus true recall 0.236. Recall of hidden frauds is 0.024 against 0.302 for seen frauds: the model learned the labelling process. The label sensitivity among frauds the model flagged is 0.937 versus 0.801 overall, which is why one global correction factor does not work. The second audit (23 true frauds, 18 labelled, sensitivity 0.78) shows how wide a 2,000-row audit stays.

**Follow-ups:**
- Can you correct the metrics with the 80%? Only if label sensitivity is the same for the flagged and the unflagged frauds; it usually is not (0.937 versus 0.801 here), so audit the flagged rows and the unflagged rows separately.
- Is this MCAR, MAR or MNAR? The missing fraud labels depend on the kind of fraud (which the features partly describe) and on whether anyone noticed it, so it behaves like not-at-random labelling; you cannot prove that from the labels alone, which is why the random audit is needed.
- What would you change in the pipeline? Randomly investigate a small share of every score band each week, so you always have unbiased labels to evaluate and retrain on.

**Common mistakes:** Treating missing labels as true negatives. Using system labels for evaluation. Dividing recall by 0.8. Not checking for false fraud labels. Ignoring that the audit itself has a wide interval.

### Q39 ⭐⭐ 🔴 On a streaming app, users rate only about 2% of the titles they watch, the average rating among rated titles is 4.3, and a random prompt to 1,000 users gives an average of 3.6 on the titles they watched. A recommender is trained only on the observed ratings. Explain what missing-data mechanism is at work, how it distorts the model and how you would correct or evaluate for it.
**Asked at:** Missing-data interview explainers (a PrachHub 'Missing Data, Imputation, And Selection Bias' concept page, ydata.ai 'understanding missing data mechanisms', a Towards Data Science 'Talking About Missing Data' article, a Daily Dose of Data Science post on three types of missing values); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** This is data missing not at random: people rate more when they loved a title, so the observed 4.3 is inflated against the 3.6 from the random prompt, and I would correct the training with weights estimated from a random-sample probe and evaluate on that probe, not on the observed ratings.

**Clarifying questions:**
- How was the random prompt delivered, and what share of prompted users answered? Why: if only some users replied, the probe has its own non-response bias.
- Does the 3.6 average cover the same titles and the same kind of users as the 4.3? Why: a gap from a different user or title mix is not the same as a gap from selection.
- Is rating a star score only, or are there other signals (watch time, completion, thumbs)? Why: implicit feedback is observed for everyone and is a better base for training.
- What does the recommender decide: the top-N list, or a predicted rating shown to users? Why: ranking and rating prediction suffer differently.
- Can we keep a small random-exposure or random-prompt stream going? Why: unbiased data is the fix that scales.

**Approach:**
1. Compute the gap. Observed mean 4.3 among rated titles versus 3.6 from a random prompt: 0.7 stars higher. With 1,000 users the sampling error of 3.6 is about 0.035 if each user gives one rating (a bit more if ratings are clustered by user), so the gap is not noise.
2. Name the mechanism. The chance of rating depends on the rating itself (people rate what they love or hate), so the data are missing not at random. Missing completely at random would give the same mean in both groups, and missing at random given observed covariates would be fixable with those covariates alone.
3. Say what it does to the model. A model trained only on observed ratings predicts too high for titles in general (a mean prediction near 4.1 in my run versus a true average near 3.6), and it ranks titles by what raters liked, not by what the average viewer would like. Titles that are watched but rarely rated look the same as unwatched ones.
4. Use the random probe as the anchor. It gives an unbiased distribution of ratings, and by comparing it with the observed distribution you can estimate how rating propensity varies with the star level, then weight observed rows by the inverse of that propensity (inverse propensity weighting).
5. Train with weights, or add a model of "was it rated" (a selection model), or use implicit feedback (watched, completed) as the main training signal, where exposure is known.
6. Evaluate on unbiased data: the random probe, a small randomised exposure test, or an online A/B test. Offline metrics on the observed ratings reward models that agree with the raters, which is the bias again.
7. Keep a standing randomised sample, and monitor the gap between observed and probe averages over time.

**Metrics:**
- Selection gap = observed mean rating - probe mean rating (4.3 - 3.6 = 0.7).
- Rating propensity by star = share of watched titles at that star level that get rated, relative to the overall rate (estimated as observed share / probe share, scaled by the overall 2%).
- Probe RMSE (or NDCG on probe items) of the model, versus RMSE on observed ratings.
- Guardrails: probe response rate, effective sample size after weighting (large weights inflate variance), and online metrics (watch time, retention).

**Risks:**
- Trusting the 4.3 or any model trained on it.
- Weights that explode: a rarely rated group gets a huge weight and the estimate gets noisy. Clip or stabilise weights.
- The probe is itself biased by non-response or by who sees the prompt.
- You cannot prove MNAR from the observed ratings alone; the random probe is the extra information that exposes it.
- Mixing up two selection steps: what users choose to watch (exposure, driven by the recommender) and what they choose to rate.

**What the interviewer scores:**
- Strong: calls it MNAR (rating depends on the rating), uses the random prompt as evidence, and explains the effect on both level and ranking.
- Strong: proposes inverse propensity weighting from a random sample, implicit feedback, and unbiased evaluation.
- Strong: notes weights need clipping and a check of effective sample size.
- Weak: "average rating is 4.3, so users like the catalogue", or "impute the missing ratings with the mean".
- Cross-reference: Book 6 Part 3 Q26 "An app sent a satisfaction survey to 250,000 users and 10,000 replied..." covers non-response bias in surveys, and Book 1 Part 7 has "Explain matrix factorization for recommendations. How is it trained (SGD vs ALS), why not treat missing entries as zeros, and what does the embedding size control?".

**Example:** (illustrative numbers) Suppose 100 watched titles with true ratings: 6 one-star, 10 two-star, 28 three-star, 30 four-star, 26 five-star (mean 3.6). People rate five-star titles 12.5 times as often as one-star ones (about 0.3% of one-star titles get rated against about 4% of five-star ones, which makes the overall rate about 2%). Rated titles then skew to four and five stars and the mean among rated titles is about 4.3. Weak answer: "the average rating is 4.3." Strong answer: "ratings are missing not at random; the random prompt says 3.6; weight by inverse propensity and evaluate on the probe."

**Code:**
```python
import numpy as np

rng = np.random.default_rng(39)
stars = np.arange(1, 6)
# true rating distribution among titles watched (invented), probability of rating given the star level (invented)
pmf = np.array([0.06, 0.10, 0.28, 0.30, 0.26]); p_rate = np.array([0.004, 0.006, 0.012, 0.025, 0.050]) * 0.81
true_mean = float((pmf * stars).sum())
rate_overall = float((pmf * p_rate).sum())
obs_pmf = pmf * p_rate / rate_overall
obs_mean = float((obs_pmf * stars).sum())
print("true mean among watched:", round(true_mean, 3), " rating rate:", round(rate_overall, 4), " mean among rated:", round(obs_mean, 3))
assert abs(true_mean - 3.6) < 0.05 and abs(rate_overall - 0.02) < 0.003 and abs(obs_mean - 4.3) < 0.05

# simulate: 200,000 users x 10 watched titles in the natural world; 1,000 users x 10 titles in the random prompt
n_nat = 2_000_000
r = rng.choice(stars, n_nat, p=pmf)
seen = rng.random(n_nat) < p_rate[r - 1]
print("natural ratings observed:", int(seen.sum()), " share:", round(float(seen.mean()), 4), " mean:", round(float(r[seen].mean()), 3))
n_probe = 10_000
rp = rng.choice(stars, n_probe, p=pmf)
print("random prompt: n =", n_probe, " mean:", round(float(rp.mean()), 3), " (se about", round(float(rp.std() / np.sqrt(n_probe)), 3), ")")

# the gap is selection, not noise: observed mean 4.3 vs probe 3.6
gap = r[seen].mean() - rp.mean()
assert gap > 0.6

# correct with inverse-propensity weights estimated from the probe: P(rated | star) is proportional to obs_pmf / probe_pmf
obs_counts = np.bincount(r[seen], minlength=6)[1:] / seen.sum()
probe_pmf = np.bincount(rp, minlength=6)[1:] / n_probe
w = probe_pmf / obs_counts                         # relative weight per star = 1 / relative propensity
ipw_mean = (w[r[seen] - 1] * r[seen]).sum() / w[r[seen] - 1].sum()
print("IPW-corrected mean of observed ratings:", round(float(ipw_mean), 3), "(probe", round(float(rp.mean()), 3), ")")
assert abs(ipw_mean - rp.mean()) < 0.05
print("weights per star (relative):", np.round(w / w[0], 2))

# a model trained on observed ratings only: item-level offset learned from observed mean; evaluate on probe
# (every title has a quality q; rating = clip(round(q + noise))); rating propensity rises with the star level
n_items = 500
q = rng.normal(3.6, 0.5, n_items)
def draw(items):
    return np.clip(np.rint(q[items] + rng.normal(0, 0.9, len(items))), 1, 5).astype(int)
watch_items = rng.integers(0, n_items, 3_000_000)
rating = draw(watch_items)
got = rng.random(len(watch_items)) < p_rate[rating - 1]
tr_i, tr_r = watch_items[got], rating[got]
mu_obs = np.array([tr_r[tr_i == i].mean() if (tr_i == i).any() else tr_r.mean() for i in range(n_items)])
probe_items = rng.integers(0, n_items, 20_000); probe_r = draw(probe_items)
pred = mu_obs[probe_items]
print("model trained on observed ratings: mean prediction on probe", round(float(pred.mean()), 3), " probe mean", round(float(probe_r.mean()), 3))
print("RMSE on observed ratings (last 20,000 rated rows, rated-only view):", round(float(np.sqrt(((mu_obs[tr_i[-20000:]] - tr_r[-20000:]) ** 2).mean())), 3),
      " RMSE on the random probe:", round(float(np.sqrt(((pred - probe_r) ** 2).mean())), 3))
assert pred.mean() - probe_r.mean() > 0.4
# fix: weight training rows by 1/propensity (star level) so training matches the probe; compare probe RMSE
probe_all = draw(rng.integers(0, n_items, 10_000))      # a random prompt, as in the scenario
pp = np.bincount(probe_all, minlength=6)[1:] / len(probe_all); oo = np.bincount(tr_r, minlength=6)[1:] / len(tr_r)
wt = (pp / oo)[tr_r - 1]                                # weights estimated from the probe, not from the hidden propensities
mu_w = np.array([(wt[tr_i == i] * tr_r[tr_i == i]).sum() / wt[tr_i == i].sum() if (tr_i == i).any() else tr_r.mean() for i in range(n_items)])
pw = mu_w[probe_items]
print("IPW model: mean prediction on probe", round(float(pw.mean()), 3), " RMSE on probe", round(float(np.sqrt(((pw - probe_r) ** 2).mean())), 3))
assert np.sqrt(((pw - probe_r) ** 2).mean()) < np.sqrt(((pred - probe_r) ** 2).mean())
```

**Output (my run):**
```text
true mean among watched: 3.6  rating rate: 0.02  mean among rated: 4.313
natural ratings observed: 40078  share: 0.02  mean: 4.308
random prompt: n = 10000  mean: 3.597  (se about 0.012 )
IPW-corrected mean of observed ratings: 3.597 (probe 3.597 )
weights per star (relative): [1.   0.7  0.34 0.17 0.08]
model trained on observed ratings: mean prediction on probe 4.075  probe mean 3.575
RMSE on observed ratings (last 20,000 rated rows, rated-only view): 0.76  RMSE on the random probe: 1.02
IPW model: mean prediction on probe 3.587  RMSE on probe 0.89
```
The text above matches this run: with the invented propensities the true mean is 3.6, the rating rate 2.0% and the mean among rated titles 4.313 (simulated 4.308). The random probe gives 3.597 (standard error about 0.012 for 10,000 ratings). Inverse propensity weights estimated from the probe bring the observed mean back to 3.597. A per-title model trained on the observed ratings predicts 4.075 on average for probe items against a probe mean of 3.575, and its RMSE is 0.76 on observed ratings but 1.02 on the random probe. With probe-estimated weights, the mean prediction is 3.587 and the probe RMSE falls to 0.89. The weighted model is better, not perfect, because each title has only a few ratings.

**Follow-ups:**
- Why not impute the missing ratings with the mean? The mean of observed ratings is biased high (4.3) and imputing it just copies the bias into the matrix; missing does not mean "average".
- Why is implicit feedback better? Watching, completing and re-watching are observed for most users, so exposure and engagement are known; they measure a different thing from stated ratings, but they are less self-selected.
- What if you have no random probe? Use a small randomised exposure test, instrumental signals such as prompt placement, or model the selection and report the result as an assumption-dependent estimate.

**Common mistakes:** Reporting 4.3 as the satisfaction level. Imputing missing ratings with the observed mean. Evaluating on the same biased ratings. Unclipped weights. Treating the probe as perfect.

### Q40 ⭐ 🔴 A team estimates that its crowd-sourced labels have asymmetric class-conditional noise: some true positives are labelled negative much more often than the reverse, and it has only 500 trusted labels. Explain how you would estimate the noise transition matrix, how you would use it to correct the loss, and where such correction breaks down.
**Asked at:** Noisy-label and annotator-disagreement material (Tanno et al., CVPR 2019 on annotator confusion matrices; a Codemia data-labelling course page); research and course pages rather than interview banks, so the scenario is partly editor-designed; search snippets only, not opened
**Say this first (1 line):** I would estimate the 2x2 noise matrix by comparing crowd labels with the 500 trusted labels, put it into a forward-corrected loss so the model learns the true-class probabilities, and I would warn that it fixes calibration and thresholds more than ranking, and fails when the noise depends on the example.

**Clarifying questions:**
- Are the 500 trusted labels a random sample, or were they chosen (easy items, disputed items, one class)? Why: a chosen sample gives a biased matrix.
- How many of the 500 are true positives? Why: the rarer class is the one whose flip rate is estimated worst (164 positives in my run gives wide intervals).
- Do crowd workers differ a lot, and do items carry several labels? Why: with several labels per item you can estimate a confusion matrix per worker and aggregate, instead of one global matrix.
- Does noise depend on the item (blurry images, ambiguous text)? Why: a single class-level matrix assumes it does not.
- What does the model output get used for: ranking, a threshold, or probabilities? Why: it tells me whether the correction is worth the risk.

**Approach:**
1. Define the matrix. T[i][j] = P(crowd label = j | true class = i). For two classes it has two free numbers: the share of true positives labelled negative and the share of true negatives labelled positive. Rows sum to 1.
2. Estimate it from the trusted rows. Count how crowd labels fall within each trusted class: T[1][0] = true positives labelled negative / true positives. Give each cell an interval (the positive row has the fewest rows).
3. Reduce variance. If there are several crowd votes per item, fit a confusion matrix per annotator with a latent-class model (Dawid-Skene style) using the trusted labels as anchors. Or use anchor points: examples the model is very sure belong to each class can estimate T without trusted labels (needs good model calibration).
4. Correct the loss. Forward correction: let p be the model's class probabilities and q = p x T the probabilities of the noisy label; train with cross-entropy between the crowd label and q. The model then learns the clean probabilities p. Backward correction multiplies the vector of losses by the inverse of T instead (needs T invertible, can give negative losses).
5. Check it. Does the corrected model's predicted positive rate match the trusted rate? Compare the corrected model with a naive one and with a model trained on the 500 trusted rows alone, on a held-out clean test set. Also use trusted labels to fine-tune or to validate.
6. Know where it breaks (next section) and keep the trusted labels as the final judge. Prefer improving labels (a second pass on disputed items, better guidelines) where cheap.

**Metrics:**
- T[i][j] estimates with 95% intervals; the determinant of T (zero means the labels carry no information; near zero means unstable correction).
- Mean predicted positive probability versus the clean positive rate on a trusted test set (calibration).
- AUC and PR-AUC on the clean test set, plus precision and recall at the working threshold.
- Guardrails: stability of the model across different draws of the trusted set, and the size of the corrected-loss gradient (exploding values signal a bad T).

**Risks:**
- A rare positive row: with 164 true positives among 500 trusted rows, the flip rate of positives is known only to within a few points.
- Noise that depends on the example (hard positives lost more often): a single global matrix over-corrects easy items and under-corrects hard ones.
- Near-singular or wrongly estimated T: the corrected loss becomes unstable or biased.
- Trusted rows chosen non-randomly.
- Correcting the loss while the validation set is still crowd-labelled, so the benefit is invisible.

**What the interviewer scores:**
- Strong: defines T with the correct direction (true to noisy), estimates it from trusted labels with intervals, and writes the forward-corrected loss.
- Strong: says the correction mainly restores calibration and the threshold, and that ranking (AUC) barely changes.
- Strong: lists failure modes: instance-dependent noise, a poorly estimated or near-singular T, trusted-label sampling bias.
- Weak: "just remove the noisy labels" with no way to find them, or "use T without checking it".
- Cross-reference: Book 6 Part 3 Q34 "On a training set of 28,000 rows, a cross-validated model strongly disagrees with the given label..." for flagging and auditing noisy rows, and Book 1 Part 3 has "Positive-unlabeled learning and noisy labels: when negatives are really unlabeled, how does that change metrics and training?".

**Example:** (illustrative numbers) Of 500 trusted rows, 164 are positive and 336 negative. The crowd labelled 115 of the positives as positive and 49 as negative, and 326 of the negatives as negative and 10 as positive. Then T[1][0] = 49 / 164 = 0.299 and T[0][1] = 10 / 336 = 0.030. A model that outputs p = 0.60 for an item has noisy-label probability q1 = 0.60 x 0.70 + 0.40 x 0.03 = 0.432. Weak answer: "crowd labels are noisy, collect more." Strong answer: "estimate the flip rates from the trusted set, train with a forward-corrected loss, and validate on trusted labels."

**Code:**
```python
import numpy as np
from scipy.optimize import minimize
from scipy.stats import rankdata

rng = np.random.default_rng(40)
def auc(y, s):
    r = rankdata(s); n1 = int(y.sum()); return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * (len(y) - n1))
sig = lambda a: 1 / (1 + np.exp(-a))

n = 30_000
X = rng.normal(size=(n, 4)); w_true = np.array([1.2, -0.8, 0.6, 0.0])
y = (rng.random(n) < sig(X @ w_true - 1.0)).astype(int)                     # about 30% positive
# T[i][j] = P(noisy label = j | true class = i): positives are lost far more often than negatives are invented
T = np.array([[0.96, 0.04], [0.30, 0.70]])
noisy = np.where(rng.random(n) < T[y, 1], 1, 0)
print("true positive rate:", round(float(y.mean()), 3), " noisy positive rate:", round(float(noisy.mean()), 3))

# 1) estimate T from 500 trusted labels (a random 500 rows that also have a crowd label)
trusted = rng.choice(n, 500, replace=False)
yt, nt = y[trusted], noisy[trusted]
That = np.array([[np.mean(nt[yt == i] == j) for j in (0, 1)] for i in (0, 1)])
print("trusted rows: positives", int((yt == 1).sum()), " negatives", int((yt == 0).sum()))
print("estimated T:\n", np.round(That, 3), "\ntrue T:\n", T)
# how stable? re-draw 500 trusted rows 300 times
est = []
for _ in range(300):
    idx = rng.choice(n, 500, replace=False); a, b = y[idx], noisy[idx]
    est.append([b[a == 1].__eq__(0).mean(), b[a == 0].__eq__(1).mean()])
est = np.array(est)
print("sd of P(noisy=0|true=1):", round(float(est[:, 0].std()), 3), "  sd of P(noisy=1|true=0):", round(float(est[:, 1].std()), 3))
assert est[:, 0].std() > 2 * est[:, 1].std()               # the rare class is the poorly estimated one

# 2) train three logistic models: naive on noisy, forward-corrected loss with estimated T, and trusted-only
F = np.c_[X, np.ones(n)]
tr = np.arange(n) < 20_000; te = ~tr
def nll_plain(w, F, t): p = np.clip(sig(F @ w), 1e-9, 1 - 1e-9); return -np.mean(t * np.log(p) + (1 - t) * np.log(1 - p))
def nll_forward(w, F, t, Tm):
    p1 = sig(F @ w)
    q1 = np.clip(p1 * Tm[1, 1] + (1 - p1) * Tm[0, 1], 1e-9, 1 - 1e-9)    # P(noisy label = 1 | x) = sum_i P(y=i|x) T[i,1]
    return -np.mean(t * np.log(q1) + (1 - t) * np.log(1 - q1))
def run(fun, *args):
    return minimize(fun, np.zeros(F.shape[1]), args=args, method="L-BFGS-B").x
w_naive = run(nll_plain, F[tr], noisy[tr])
w_fwd = run(nll_forward, F[tr], noisy[tr], That)
w_fwd_true = run(nll_forward, F[tr], noisy[tr], T)
tt = np.intersect1d(trusted, np.where(tr)[0])
w_trust = run(nll_plain, F[trusted], y[trusted])                              # 500 clean rows only
def report(name, w):
    s = F[te] @ w
    print(f"{name:34s} AUC {auc(y[te], s):.4f}   mean predicted P(y=1) {sig(s).mean():.3f} (truth {y[te].mean():.3f})")
    return sig(s).mean()
m_n = report("naive on noisy labels", w_naive)
m_f = report("forward-corrected, T estimated", w_fwd)
m_t = report("forward-corrected, T true", w_fwd_true)
m_c = report("trusted 500 only", w_trust)
assert abs(m_f - y[te].mean()) < abs(m_n - y[te].mean())

# 3) where it breaks: (a) instance-dependent noise (hard positives lost more), (b) near-singular T
hard = X[:, 0] < 0
noisy_id = np.where(rng.random(n) < np.where(y == 1, np.where(hard, 0.55, 0.12), 0.04), 1 - y, y)
rate_hard = (noisy_id[y == 1][hard[y == 1]] == 0).mean(); rate_easy = (noisy_id[y == 1][~hard[y == 1]] == 0).mean()
print("instance-dependent noise: positives lost, hard", round(float(rate_hard), 3), " easy", round(float(rate_easy), 3))
T_glob = np.array([[0.96, 0.04], [0.30, 0.70]])
w_id = run(nll_forward, F[tr], noisy_id[tr], T_glob)
w_id_n = run(nll_plain, F[tr], noisy_id[tr])
print("instance-dependent: AUC naive", round(float(auc(y[te], F[te] @ w_id_n)), 4), " corrected with one global T", round(float(auc(y[te], F[te] @ w_id)), 4))
print("determinant of T (0 means labels carry no information):", round(float(np.linalg.det(T)), 3), " if T=[[.8,.2],[.55,.45]]:", round(float(np.linalg.det(np.array([[.8, .2], [.55, .45]]))), 3))
```

**Output (my run):**
```text
true positive rate: 0.329  noisy positive rate: 0.258
trusted rows: positives 164  negatives 336
estimated T:
 [[0.97  0.03 ]
 [0.299 0.701]] 
true T:
 [[0.96 0.04]
 [0.3  0.7 ]]
sd of P(noisy=0|true=1): 0.037   sd of P(noisy=1|true=0): 0.01
naive on noisy labels              AUC 0.8196   mean predicted P(y=1) 0.255 (truth 0.324)
forward-corrected, T estimated     AUC 0.8196   mean predicted P(y=1) 0.335 (truth 0.324)
forward-corrected, T true          AUC 0.8196   mean predicted P(y=1) 0.326 (truth 0.324)
trusted 500 only                   AUC 0.8188   mean predicted P(y=1) 0.310 (truth 0.324)
instance-dependent noise: positives lost, hard 0.556  easy 0.119
instance-dependent: AUC naive 0.8146  corrected with one global T 0.8137
determinant of T (0 means labels carry no information): 0.66  if T=[[.8,.2],[.55,.45]]: 0.25
```
The text above matches this run: the true positive rate is 32.9% but the crowd labels show 25.8%. The 500 trusted rows contain 164 positives and 336 negatives and give T[1][0] = 0.299 and T[0][1] = 0.03 against true 0.30 and 0.04. Across 300 redraws, the standard deviation of the positive-row flip rate is 0.037 against 0.010 for the negative row, so the rare class is the poorly known one. AUC is 0.8196 for the naive, forward-corrected (estimated T) and forward-corrected (true T) models, so ranking does not change, but the mean predicted positive probability is 0.255 for the naive model (truth 0.324), 0.335 with the estimated T and 0.326 with the true T. The model trained on the 500 trusted rows alone gets AUC 0.8188 and a mean of 0.310, which for a simple four-feature model is a serious competitor. When noise depends on the example (positives lost 0.556 of the time on hard items, 0.119 on easy ones), correcting with one global T does not help: AUC 0.8137 against 0.8146 for the naive model. The determinant of T is 0.66 here; for T = [[0.8, 0.2], [0.55, 0.45]] it is 0.25, closer to the point where labels carry no information.

**Follow-ups:**
- Forward or backward correction? Forward correction keeps the loss a valid cross-entropy and is more stable; backward correction needs the inverse of T and can produce negative loss values.
- Can you estimate T without any trusted labels? Under assumptions (anchor points, a good clean-ish model), yes, but check against the trusted labels when you have them.
- Would you rather spend the effort on cleaning? Often yes. A second review of the disputed items, or relabelling the most uncertain 1,000 rows, usually beats a clever loss when the noise is instance-dependent.

**Common mistakes:** Mixing up the direction of T (true to noisy, not noisy to true). Estimating T from a non-random trusted sample. Ignoring the interval for the rare class. Expecting AUC to rise. Using one global T for example-dependent noise. Validating on crowd labels.

### Q41 ⭐ 🔴 Dropping the 5% of 60,000 training rows with the highest loss (3,000 rows) raised validation accuracy by 1.0 percentage point, but accuracy for a dialect group that makes up 4% of the data (2,400 rows) fell, because 900 of the dropped rows belong to that group. Explain what the loss filter is really removing, how you would separate noise from hard but valid examples, and how you would check fairness of the cleaning step.
**Asked at:** Noisy-label and annotator-disagreement material (Tanno et al., CVPR 2019 on annotator confusion matrices; a Codemia data-labelling course page); research and course pages rather than interview banks, so the scenario is partly editor-designed; search snippets only, not opened
**Say this first (1 line):** A top-loss filter removes two things at once, wrong labels and correct-but-hard rows, and here 900 of the 3,000 rows it dropped (30%) came from a group that is only 4% of the data, so it is also a bias.

**Clarifying questions:**
- Is the 1.0 point gain on a validation set that has the same noisy labels as training? Why: a noisy validation set can reward a model for agreeing with the filter, not for being right.
- How is the dialect group defined and how many validation rows does it have? Why: 4% of validation may be too few rows to see a drop; I need the interval.
- Was the loss computed by a model trained on the same rows (in-sample) or out-of-fold? Why: in-sample loss shrinks on memorised noise, so out-of-fold loss is the cleaner signal.
- Can I get a human relabel of a sample of the dropped rows? Why: it is the only direct measure of how many dropped rows were really wrong.
- Does the group matter for the product (a market, a legal duty)? Why: it sets how much accuracy loss I tolerate there.

**Approach:**
1. Do the arithmetic first. The group lost 900 of 2,400 rows = 37.5%. Everyone else lost 2,100 of 57,600 = 3.65%. The group is dropped about 10 times as often, and its share of the data falls from 4% to 2.63%.
2. Name the cause. Loss is high for two reasons: the label is wrong, or the model has not learned the example yet. A group the model has seen less of has more of the second kind, so a single global cut-off picks them first.
3. Separate the two kinds. Use out-of-fold loss, then ask a second, independent signal: a different model's disagreement, annotator disagreement, or a human check on a sample. Drop only rows where both agree it is wrong.
4. Cut within each group, not globally: compare each row's loss to the loss distribution of its own group.
5. Prefer relabel or down-weight over delete for rows that are only flagged by loss.
6. Audit the cleaning step as a model change: report accuracy and error rate per group before and after, with an interval, on a validation set whose labels were reviewed.

**Metrics:**
- Per-group drop rate = rows dropped in the group / rows in the group (37.5% vs 3.65% here).
- Noise precision = dropped rows that a human says were wrong / dropped rows. Noise recall = wrong rows dropped / all wrong rows (needs the audit sample).
- Per-group accuracy delta with a 95% interval, on reviewed labels.
- Guardrails: no group's accuracy falls by more than a set margin (say 1 point); drop-rate ratio between groups stays near 1.

**Risks:**
- A validation set with the same noise can make a harmful filter look good.
- Deleting hard valid rows makes the model confident and wrong on the group that the rows described.
- A second signal that is itself weaker on the group repeats the bias.
- Reviewers only see dropped rows, so they never learn how many wrong rows stayed.

**What the interviewer scores:**
- Strong: states that loss mixes "wrong" and "hard", and shows the 37.5% vs 3.65% drop rates.
- Strong: proposes a second signal and a human sample to estimate noise precision, not trust loss alone.
- Strong: treats the filter as a model change and audits per group.
- Weak: "accuracy went up so the filter works."
- Weak: raises the cut-off to be safe without measuring who is dropped.

**Example:** (illustrative numbers) The code builds 60,000 rows with 3% wrong labels, a group of 2,400 whose clean rows have higher loss, and drops the top 5%. A global cut removes 3,000 rows, 62% of them truly wrong, but also 845 valid group rows. A per-group cut with the same 5% rate removes only 63 valid group rows. Requiring a second signal drops 1,699 rows with 94% noise precision and 86% noise recall. Weak answer: "drop the top 5% loss, accuracy went up." Strong answer: "That also drops 37.5% of the dialect group; I would cut per group, confirm with a second signal and a human sample, and report accuracy for that group."

**Code:**
```python
# Q41: loss-filter cleaning and a small dialect group. Illustrative numbers.
import numpy as np

# --- prompt arithmetic ---
N, drop, G, g_drop = 60_000, 3_000, 2_400, 900
assert drop == int(0.05 * N) and G == int(0.04 * N)
print(f"group rows dropped: {g_drop}/{G} = {g_drop/G:.1%}")
print(f"other rows dropped: {drop-g_drop}/{N-G} = {(drop-g_drop)/(N-G):.2%}")
print(f"group share of dropped rows: {g_drop/drop:.0%} vs {G/N:.0%} of data")
assert g_drop / G == 0.375 and round((drop-g_drop)/(N-G), 4) == 0.0365
assert g_drop / drop == 0.30
print(f"group share after drop: {(G-g_drop)/(N-drop):.2%}")
assert round((G-g_drop)/(N-drop), 4) == 0.0263

# --- simulation: three kinds of rows (all distributions invented) ---
rng = np.random.default_rng(41)
grp = np.zeros(N, bool); grp[:G] = True
noisy = rng.random(N) < 0.03                      # 3% wrong labels in both groups
loss = np.where(grp, rng.exponential(0.50, N), rng.exponential(0.10, N))  # group is harder
loss = np.where(noisy, 2.0 + rng.exponential(0.8, N), loss)               # wrong labels: high loss

def report(name, dropped):
    d = int(dropped.sum())
    n_noisy = int((dropped & noisy).sum())
    g_valid = int((dropped & grp & ~noisy).sum())
    print(f"{name:34s} dropped={d:5d} noise_precision={n_noisy/d:.2f} "
          f"noise_recall={n_noisy/noisy.sum():.2f} valid_group_rows_lost={g_valid}")
    return d, n_noisy, g_valid

thr = np.quantile(loss, 0.95)
a = report("A global top-5% loss", loss >= thr)
tg = np.quantile(loss[grp], 0.95); to = np.quantile(loss[~grp], 0.95)
b = report("B per-group top-5% loss", np.where(grp, loss >= tg, loss >= to))
# C: need loss in the top 5% AND a second signal (here: a second model disagrees, simulated
# as firing on 85% of noisy rows and 10% of clean rows). Illustrative second signal.
second = np.where(noisy, rng.random(N) < 0.85, rng.random(N) < 0.10)
c = report("C top-5% loss AND second signal", (loss >= thr) & second)

print(f"A dropped group rows total: {int((loss>=thr)[grp].sum())} of {G}")
assert a[2] > 5 * b[2] > 0 and a[2] > c[2]          # global filter loses most valid group rows
assert c[1] / c[0] > a[1] / a[0]                     # second signal raises noise precision
# group-wise accuracy cost of each policy is not simulated: check it with a real group eval set.
```

**Output (my run):**
```text
group rows dropped: 900/2400 = 37.5%
other rows dropped: 2100/57600 = 3.65%
group share of dropped rows: 30% vs 4% of data
group share after drop: 2.63%
A global top-5% loss               dropped= 3000 noise_precision=0.62 noise_recall=1.00 valid_group_rows_lost=845
B per-group top-5% loss            dropped= 3000 noise_precision=0.62 noise_recall=1.00 valid_group_rows_lost=63
C top-5% loss AND second signal    dropped= 1699 noise_precision=0.94 noise_recall=0.86 valid_group_rows_lost=80
A dropped group rows total: 902 of 2400
```
The simulation is invented and easy (wrong labels have much higher loss than anything else), so the exact counts are only a demonstration of the pattern. The 845 valid group rows lost under the global cut is close to the prompt's 900.

**Follow-ups:**
- Why not just oversample the group after dropping? It restores the count but not the lost hard examples; the rows you added back are copies of the easy ones.
- How do you pick the 5%? From the estimated noise rate (an audit sample), not a fixed number. Here the audit would say about 3%, so 5% already drops too many valid rows. See Q40 in this part (asymmetric label noise).

**Common mistakes:** Treating high loss as proof of a wrong label. Using one global cut-off. Judging the filter on an aggregate metric dominated by the 96% majority. Deleting instead of reviewing or down-weighting. Never auditing per group.

### Q42 ⭐ 🔴 A text corpus of 1,000,000 documents used for quarterly retraining now includes 600,000 documents generated by earlier versions of the model, so real data is 400,000 documents (40%). Quality metrics on a fixed real test set drift down each quarter. Explain what mechanism could be at work, how you would measure it, and what data policy you would set.
**Asked at:** AI-era LLM-labelling, weak-supervision and synthetic-data material (an arXiv 2026 abuse-detection paper using LLM annotators, an arXiv survey on LLM-driven synthetic data, an arXiv paper on weak data and model collapse, a Codemia labelling course page); emerging practitioner and research theme, not a confirmed interview staple; search snippets only, not opened
**Say this first (1 line):** This looks like model collapse: each generation of synthetic text under-represents rare content, so the tail of the real distribution thins out every quarter, and the fix is to keep a fresh real-data anchor and track tail metrics, not just the average.

**Clarifying questions:**
- Are the 600,000 generated documents filtered, deduplicated or tagged? Why: unfiltered synthetic text carries the model's sampling bias straight back in.
- Is the real part fresh each quarter, or is it the same 400,000 documents? Why: fresh real data keeps the tail alive; a reused set does not.
- Is the real test set held out and frozen, and does it have tail slices (rare topics, languages, long documents)? Why: an average can hide the tail loss.
- Were the earlier models sampled with low temperature or top-p? Why: that is what sharpens the synthetic distribution toward common content.
- Do the synthetic documents mostly come from the previous model, or from many different models? Why: one source repeats one bias.

**Approach:**
1. State the mechanism. A model learns the data it sees. When it writes text it samples common content more than rare content (sampling settings, and finite samples). The next model trains on that thinner distribution, and its output is thinner again. Rare topics shrink first, because they appear few times and one miss removes them.
2. Measure it, not just assert it. On the fixed real test set, report loss on a head slice and a tail slice separately; measure diversity of the generated corpus (distinct n-grams, topic counts); estimate the synthetic share of each quarter's data.
3. Reproduce the direction on a small controlled run: train with 0%, 40% and 100% real data and see which one keeps the tail.
4. Set the data policy: keep a real anchor with fresh real data each quarter, accumulate real data and do not replace it, tag provenance on every document, cap the synthetic share, filter and deduplicate synthetic text, and oversample tail topics from real data.
5. Gate retraining: if tail-slice loss on the frozen real set worsens beyond a margin, do not promote the new model.

**Metrics:**
- Tail-slice loss on the real test set: mean loss over documents in rare slices / count of those documents. Report next to head-slice loss.
- Tail mass of the training mix = share of probability on topics ranked beyond a chosen rank.
- Topic survival = topics with at least one document / topics in the real data.
- Synthetic share = synthetic documents / all documents (60% now).
- Guardrails: tail-slice loss, topic survival, and distinct n-gram ratio do not drop quarter over quarter.

**Risks:**
- The average loss can look flat while the tail collapses; a head-only test set hides it.
- Synthetic share creeps up because generating text is cheap and real text is scarce.
- The real test set may itself contain model-generated text (contamination).
- Detectors for generated text are unreliable, so provenance tags at creation time matter more than detection later.

**What the interviewer scores:**
- Strong: names the mechanism (tail loss compounding across generations) and says why rare content goes first.
- Strong: asks for tail slices on a frozen real set and measures it.
- Strong: sets a policy with an anchor, provenance, a cap and an accumulate-not-replace rule.
- Weak: "add more data" or "the test set is just different."
- Weak: bans synthetic data entirely without saying where it helps.

**Example:** (illustrative numbers) The code uses 5,000 topics with a Zipf-shaped real distribution and a sampler that favours common topics slightly (temperature below 1). Real tail mass (topics ranked beyond 500) is 0.253. With 40% fresh real data each quarter, the trained mix's tail mass falls and settles at 0.132 after eight quarters (the deterministic limit is 0.130); no topic goes to zero. With 0% real data it falls to 0.000 by quarter 8 and 4,881 of 5,000 topics have zero probability. Weak answer: "the model is overfitting." Strong answer: "Synthetic share is 60%, tail loss compounds; I would anchor with fresh real data, tag provenance and gate on tail slices."

**Code:**
```python
# Q42: recursive training on model output. Toy: a categorical "topic" distribution. Illustrative.
import numpy as np

N, SYN, REAL = 1_000_000, 600_000, 400_000
assert SYN + REAL == N and REAL / N == 0.40 and SYN / N == 0.60

K = 5_000                                   # topics, Zipf-like true distribution
ranks = np.arange(1, K + 1)
p_true = 1.0 / ranks; p_true /= p_true.sum()
TAIL = ranks > 500                          # tail = topics ranked below 500
print(f"true tail mass (rank>500): {p_true[TAIL].sum():.3f}")

def sharpen(p, a=1.15):                     # sampling with temperature < 1 favours common topics
    q = p ** a
    return q / q.sum()

def run(real_share, quarters=8, seed=7):
    rng = np.random.default_rng(seed)
    p = p_true.copy()                       # quarter-0 model = true distribution
    rows = []
    for q in range(1, quarters + 1):
        n_real = int(N * real_share); n_syn = N - n_real
        c = rng.multinomial(n_real, p_true) + rng.multinomial(n_syn, sharpen(p))
        p = c / c.sum()                     # next model = empirical mix it was trained on
        rows.append((q, p[TAIL].sum(), int((p == 0).sum())))
    return rows

for share in (0.40, 0.0):
    print(f"real share {share:.0%}:")
    rows = run(share)
    for q, tail, dead in rows:
        if q in (1, 2, 4, 8):
            print(f"  quarter {q}: tail mass {tail:.3f}  topics with zero probability {dead}")
    if share == 0.40: r40 = rows
    else: r0 = rows

# deterministic fixed point for the 40% case (expected value, no sampling noise)
p = p_true.copy()
for _ in range(200):
    p = 0.4 * p_true + 0.6 * sharpen(p)
print(f"40% real, long-run expected tail mass: {p[TAIL].sum():.3f} (true {p_true[TAIL].sum():.3f})")

assert r0[-1][1] < r40[-1][1] < p_true[TAIL].sum()   # more real data -> less tail loss; still below truth
assert r0[-1][2] > r40[-1][2]                        # fewer extinct topics with real data
assert r0[0][1] > r0[-1][1]                          # tail shrinks over quarters without real data
```

**Output (my run):**
```text
true tail mass (rank>500): 0.253
real share 40%:
  quarter 1: tail mass 0.188  topics with zero probability 0
  quarter 2: tail mass 0.156  topics with zero probability 0
  quarter 4: tail mass 0.137  topics with zero probability 0
  quarter 8: tail mass 0.132  topics with zero probability 0
real share 0%:
  quarter 1: tail mass 0.142  topics with zero probability 0
  quarter 2: tail mass 0.063  topics with zero probability 41
  quarter 4: tail mass 0.006  topics with zero probability 2455
  quarter 8: tail mass 0.000  topics with zero probability 4881
40% real, long-run expected tail mass: 0.130 (true 0.253)
```
This is a toy: a categorical distribution, not a language model. It shows the direction and the role of the real share, not the size of the effect in any real system. Note that 40% real data does not restore the original tail (0.132 versus 0.253); it only stops the collapse.

**Follow-ups:**
- Is a 40% real share safe? It stopped the collapse in the toy but still under-represents the tail, so I would still oversample tail topics from real data and keep checking tail loss.
- Can synthetic data help? Yes for filling known gaps with checked, tagged examples; the problem is replacing real data with unchecked model output. See Q33 in this part (synthetic rows for a rare class).

**Common mistakes:** Watching only average loss. Replacing old real data with new synthetic data. Having no provenance tags. Letting the test set include generated text. Assuming a detector can clean the corpus afterwards.

### Q43 ⭐ 🔴 A team labelled training data with one LLM and now uses the same LLM as the judge to measure whether the trained classifier is accurate, and the reported agreement is 96%. Explain the circularity, how you would build an independent evaluation set, and how you would measure and report the bias of the LLM labels by segment.
**Asked at:** AI-era LLM-labelling, weak-supervision and synthetic-data material (an arXiv 2026 abuse-detection paper using LLM annotators, an arXiv survey on LLM-driven synthetic data, an arXiv paper on weak data and model collapse, a Codemia labelling course page); emerging practitioner and research theme, not a confirmed interview staple; search snippets only, not opened
**Say this first (1 line):** A 96% agreement with the same LLM that made the labels only says the classifier copies the LLM, including its mistakes, so I would build a small independent human-labelled set, sampled by segment, and report accuracy and LLM-label bias per segment with intervals.

**Clarifying questions:**
- Is the 96% the agreement between the classifier and the LLM judge on held-out rows? Why: that is what "agreement" can only mean here, and it measures imitation, not truth.
- Which segments matter (language, product, user type, rare classes)? Why: LLM errors are rarely uniform, and the segments set the audit strata.
- Do we have any human labels today, even old ones? Why: they can seed the gold set and a first bias estimate.
- How many humans can label, and is there a clear guideline? Why: it sets the audit size and whether two annotators are needed.
- Is the judge prompt the same as the labelling prompt? Why: the more alike they are, the more the errors correlate.

**Approach:**
1. Name the circle. The same model made the labels and judges the result. If the LLM has a blind spot, the classifier learns it, and the judge shares it, so both agree and both are wrong.
2. Build an independent set: draw a random stratified sample of production-like rows, with a fixed number per segment (400 per segment gives a worst-case half-width of 4.9 points), and have humans label it with a written guideline, two annotators on a subset to measure their own agreement. Keep it out of training and prompt tuning.
3. Measure the LLM labels against it by segment: accuracy, and error direction (false positive vs false negative). Reweight segments by their real population share for the overall number.
4. Measure the classifier on the same set. Report classifier-vs-human, LLM-vs-human, and classifier-vs-LLM side by side.
5. Report with intervals and a bias table by segment. If one segment is far worse, fix it (relabel it by humans, add targeted examples) and do not average it away.
6. Refresh the gold set on a schedule and never use it to tune the LLM prompt without a second holdout.

**Metrics:**
- Agreement(classifier, LLM) = rows where both give the same label / rows scored. Measures copying, not correctness.
- Accuracy(classifier, human) = rows where the classifier matches the human label / rows in the audit set, per segment and weighted overall.
- LLM label bias per segment = 1 - accuracy(LLM, human) in the segment, plus the false-positive and false-negative split.
- Interval: Wilson or normal, half-width about 1.96 x sqrt(p(1-p)/n).
- Guardrails: annotator agreement on a double-labelled subset; no segment's classifier accuracy falls below a floor.

**Risks:**
- Humans following a guideline written from the LLM's labels can inherit the same bias.
- A small segment with very few audit rows gives a wide interval.
- Reusing the gold set for prompt tuning leaks it.
- The classifier may beat the LLM on easy segments (it averages out random noise) and still copy the LLM on the hard one.

**What the interviewer scores:**
- Strong: says agreement with the labeller measures imitation, and explains why errors correlate.
- Strong: designs a stratified human audit with sample sizes and intervals, and reweights.
- Strong: reports bias by segment, not one number.
- Weak: "96% is great, ship it."
- Weak: swaps in a second LLM as the judge and calls it independent.

**Example:** (illustrative numbers) In the code, the LLM has a blind spot in the code-mixed segment (20% of rows). The classifier agrees with the LLM judge on 96.9% of 20,000 test rows. Against human truth it is 91.8% accurate overall and 61.2% accurate in code-mixed rows. LLM labels alone are 60.6% right in that segment versus 97.1% in English. A stratified audit of 400 rows per segment finds 57.8% in code-mixed (plus or minus 4.8) and a population-weighted LLM label accuracy of 89.3%. Weak answer: "96% agreement." Strong answer: "That is copying; the human audit shows about 61% in the code-mixed segment."

**Code:**
```python
# Q43: a classifier trained on LLM labels, judged by the same LLM. Illustrative simulation.
import numpy as np
rng = np.random.default_rng(43)

def make(n):
    seg = rng.choice(3, n, p=[0.70, 0.20, 0.10])         # 0 English, 1 code-mixed, 2 other
    xa = rng.normal(size=n)                               # the real signal
    y = (xa > 0).astype(int)                       # human truth
    return seg, xa, y

def llm_label(seg, xa, y):
    # LLM is mostly right, but has a systematic blind spot: in segment 1, when xa is in (0, 1.2) it says 0
    out = y.copy()
    blind = (seg == 1) & (xa > 0) & (xa < 1.2)
    out[blind] = 0
    # plus 3% random errors everywhere
    flip = rng.random(len(y)) < 0.03
    out[flip] = 1 - out[flip]
    return out

def feats(seg, xa):
    s1 = (seg == 1).astype(float)
    return np.column_stack([np.ones(len(xa)), xa, s1, s1 * xa, s1 * (xa > 0), s1 * (xa > 1.2)])

def fit_logit(X, t, iters=30):
    w = np.zeros(X.shape[1])
    for _ in range(iters):
        p = 1 / (1 + np.exp(-X @ w))
        g = X.T @ (p - t) + 1e-6 * w
        H = (X * (p * (1 - p))[:, None]).T @ X + 1e-6 * np.eye(len(w))
        w -= np.linalg.solve(H, g)
    return w

seg, xa, y = make(60_000); lab = llm_label(seg, xa, y)
w = fit_logit(feats(seg, xa), lab)

seg_t, xa_t, y_t = make(20_000); lab_t = llm_label(seg_t, xa_t, y_t)   # test rows with LLM labels
pred = (feats(seg_t, xa_t) @ w > 0).astype(int)

agree = (pred == lab_t).mean()
acc_true = (pred == y_t).mean()
llm_acc = (lab_t == y_t).mean()
print(f"classifier vs LLM judge agreement : {agree:.3f}")
print(f"classifier vs human truth accuracy: {acc_true:.3f}")
print(f"LLM labels vs human truth accuracy: {llm_acc:.3f}")
for s, nm in enumerate(["English", "code-mixed", "other"]):
    m = seg_t == s
    print(f"  {nm:10s} share {m.mean():.2f}  agree-with-LLM {(pred[m]==lab_t[m]).mean():.3f}  "
          f"acc-vs-truth {(pred[m]==y_t[m]).mean():.3f}  LLM-label acc {(lab_t[m]==y_t[m]).mean():.3f}")
assert agree > 0.95 and acc_true < agree - 0.02

# independent set: stratified human audit, 400 rows per segment, then reweight to population shares
n_per = 400
share = np.array([0.70, 0.20, 0.10])
est = []; 
for s in range(3):
    idx = np.where(seg_t == s)[0]; pick = rng.choice(idx, n_per, replace=False)
    acc = (lab_t[pick] == y_t[pick]).mean()
    half = 1.96 * np.sqrt(acc * (1 - acc) / n_per)
    est.append(acc); print(f"  audit seg {s}: LLM label accuracy {acc:.3f} +/- {half:.3f}")
overall = float(np.dot(share, est))
print(f"population-weighted LLM label accuracy = {overall:.3f}")
assert abs(overall - llm_acc) < 0.02
print(f"worst-case half width at n=400, p=0.5: {1.96*np.sqrt(0.25/400):.3f}")
assert round(1.96*np.sqrt(0.25/400), 3) == 0.049
```

**Output (my run):**
```text
classifier vs LLM judge agreement : 0.969
classifier vs human truth accuracy: 0.918
LLM labels vs human truth accuracy: 0.896
  English    share 0.70  agree-with-LLM 0.968  acc-vs-truth 0.997  LLM-label acc 0.971
  code-mixed share 0.20  agree-with-LLM 0.970  acc-vs-truth 0.612  LLM-label acc 0.606
  other      share 0.10  agree-with-LLM 0.968  acc-vs-truth 0.997  LLM-label acc 0.970
  audit seg 0: LLM label accuracy 0.973 +/- 0.016
  audit seg 1: LLM label accuracy 0.578 +/- 0.048
  audit seg 2: LLM label accuracy 0.963 +/- 0.019
population-weighted LLM label accuracy = 0.893
worst-case half width at n=400, p=0.5: 0.049
```
The blind spot is built into the simulation, so the numbers show the circularity, not how often it happens in practice.

**Follow-ups:**
- Why not use a stronger LLM as judge? It helps only if its errors are independent of the labeller's; otherwise it is the same circle. Use it to find disagreement rows for humans to review. See Q24 in this part (an audit of LLM-labelled tickets).
- How many audit rows do I need? For a segment accuracy near 0.5, a half-width of 5 points needs about 400 rows; rarer or higher-accuracy segments need fewer rows per point but still enough positives.

**Common mistakes:** Calling agreement with the labeller "accuracy". Using the same model, or the same prompt family, as labeller and judge. A single overall number with no segments. A gold set made from LLM-labelled rows that humans only skim. Tuning the prompt on the gold set.

### Q44 ⭐ 🔴 A model was trained on data imputed with an iterative multiple-imputation procedure that used the full data set, but at serving time a single request arrives with some fields missing and no other rows to borrow from. Explain why imputation for inference differs from imputation for prediction, how you would design serving-time handling, and how you would keep training and serving consistent.
**Asked at:** Missing-data interview explainers (a PrachHub 'Missing Data, Imputation, And Selection Bias' concept page, ydata.ai 'understanding missing data mechanisms', a Towards Data Science 'Talking About Missing Data' article, a Daily Dose of Data Science post on three types of missing values); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Multiple imputation is built to get honest estimates of parameters from a whole table; serving needs a fixed function that fills one row using only that row and stored training numbers, and that function must be the same one used to make the training features.

**Clarifying questions:**
- Did the imputation model include the target as a predictor? Why: that is standard for inference, but the target does not exist at serving, so training and serving fills differ.
- Which fields go missing at serving, and how often compared with training? Why: it sets the missing patterns I must handle, including two fields missing together.
- Is the missingness random, or does it depend on the value or on the outcome? Why: it decides whether filling is safe or the missing flag carries signal.
- What is the latency and the model family? Why: a tree model can take missing values natively; a linear model needs a fill.
- Can the serving system load a small imputation artifact (means, a covariance, coefficients)? Why: that is the cheapest consistent design.

**Approach:**
1. Separate the two jobs. Multiple imputation (several filled copies, then pooled by Rubin's rules) is for estimating parameters and their uncertainty. Prediction needs one stable value per request.
2. Fit the imputer on training rows only, store it as an artifact, and apply the same artifact at training and serving. Never refit it on test or serving data.
3. Do not let the imputer use the target. If it did, the training features contain target information that is not available at serving, and the model learns to lean on the filled value.
4. Handle any missing pattern with a function of the observed fields only, for example the conditional mean from a stored mean vector and covariance matrix, or a simple per-field default when little is observed.
5. Add missing-indicator features so the model can learn from the fact that a value is absent. Or use a model that handles missing values natively.
6. Train with the serving missing pattern: mask extra values in training at the rates seen in production, so the model has practised on filled values.
7. Test consistency: the offline pipeline run on one row must give the same features as the online one (a parity test), and track per-field missing rates in production.

**Metrics:**
- Serving-time R2 (or AUC) with the real missing pattern, compared with the no-missing upper bound and with training-time numbers. R2 = 1 - sum of squared errors / total sum of squares.
- Feature parity = share of rows where the online feature equals the offline feature within a tolerance (target 100%).
- Per-field missing rate in training vs in serving.
- Guardrails: metric on rows with each missing pattern, and a spike alert on missing rates.

**Risks:**
- A training fill that used the target makes offline numbers look better than serving.
- Two fields missing at once need a fill that handles that pattern, not a regression that expects the other to be present.
- Refitting the imputer on a serving batch shifts features over time and on small batches is unstable.
- Hiding all uncertainty behind a single fill; when many fields are missing, say so in the score or abstain.

**What the interviewer scores:**
- Strong: separates inference (Rubin's rules, parameter uncertainty) from prediction (one deterministic fill).
- Strong: spots target use in the training imputation as a training-serving mismatch.
- Strong: gives a concrete artifact, a parity test and masking in training.
- Weak: "just run the imputation at serving too" (it needs the other rows).
- Weak: fills with the global mean and does not measure the loss.

**Example:** (illustrative numbers) In the code, column 1 is missing in 50% of rows. Filling it with a regression that used the target gives a model coefficient of 1.209 on that column (truth 1.000). Filling without the target gives 1.003. At serving with the no-target fill, R2 is 0.763 for the target-informed training and 0.768 for the consistent one. The cost in this linear toy is small (about half an R2 point), and flexible models usually suffer more, but the coefficient is already wrong. With nothing missing R2 would be 0.878, so the missing values cost about 11 points; that is information lost, and no fill brings it back. For a row where only column 0 is observed (value 1.0), the stored covariance gives fills of 0.304 and 0.504. Weak answer: "run MICE at serving too." Strong answer: "Fit a stored imputer on training, without the target, mask during training, add missing flags and test parity."

**Code:**
```python
# Q44: imputation for training vs for serving one row. Illustrative simulation (numpy only).
import numpy as np
rng = np.random.default_rng(44)

mean = np.array([0.0, 0.0, 0.0]); 
cov = np.array([[1.0, 0.3, 0.5], [0.3, 1.0, 0.2], [0.5, 0.2, 1.0]])
def draw(n):
    X = rng.multivariate_normal(mean, cov, n)
    y = X[:, 0] + X[:, 1] + 0.5 * X[:, 2] + rng.normal(0, 0.7, n)
    return X, y

Xtr, ytr = draw(50_000); Xte, yte = draw(50_000)
miss_rate = 0.50                                   # column 1 missing in 50% of rows (MCAR here)
mtr = rng.random(len(ytr)) < miss_rate; mte = rng.random(len(yte)) < miss_rate

def ols(X, t):
    A = np.column_stack([np.ones(len(X)), X]); return np.linalg.lstsq(A, t, rcond=None)[0]
def pred(w, X): return np.column_stack([np.ones(len(X)), X]) @ w
def r2(t, p): return 1 - ((t - p) ** 2).sum() / ((t - t.mean()) ** 2).sum()

# imputers fitted on TRAINING rows only (stored as small coefficient vectors)
obs = ~mtr
w_noy = ols(Xtr[obs][:, [0, 2]], Xtr[obs, 1])                         # x1 ~ x0, x2          (no target)
w_y   = ols(np.column_stack([Xtr[obs][:, [0, 2]], ytr[obs]]), Xtr[obs, 1])   # x1 ~ x0, x2, y (uses target)

def impute(X, m, w, y=None):
    Z = X.copy()
    F = X[:, [0, 2]] if y is None else np.column_stack([X[:, [0, 2]], y])
    Z[m, 1] = pred(w, F)[m]
    return Z

# Train A: imputation used the target (like a "full data" imputation model). Train B: no target.
A = impute(Xtr, mtr, w_y, ytr); B = impute(Xtr, mtr, w_noy)
mA = ols(A, ytr); mB = ols(B, ytr)

# Serving: target unknown, only this row's other fields available
Se = impute(Xte, mte, w_noy)
print(f"coefficient on x1  A (target-informed fill): {mA[2]:.3f}   B (no target): {mB[2]:.3f}   truth 1.000")
rA = r2(yte, pred(mA, Se)); rB = r2(yte, pred(mB, Se)); rfull = r2(yte, pred(ols(Xtr, ytr), Xte))
print(f"serving R2  A: {rA:.3f}   B: {rB:.3f}   no missing at all: {rfull:.3f}")
assert rB > rA and mA[2] - mB[2] > 0.15 and abs(mB[2] - 1) < 0.05

# Pattern problem: at serving, x2 may ALSO be missing. Gaussian conditional mean for any observed subset.
def cond_mean(obs_idx, x_obs, miss_idx, mu, S):
    So = S[np.ix_(obs_idx, obs_idx)]; Smo = S[np.ix_(miss_idx, obs_idx)]
    return mu[miss_idx] + Smo @ np.linalg.solve(So, x_obs - mu[obs_idx])

mu_hat = Xtr.mean(0); S_hat = np.cov(Xtr.T)
row = np.array([1.0, np.nan, np.nan])
print("x1, x2 missing, x0=1.0 ->", np.round(cond_mean([0], row[[0]], [1, 2], mu_hat, S_hat), 3))
assert abs(cond_mean([0], row[[0]], [1, 2], mu_hat, S_hat)[0] - 0.3) < 0.03

# Multiple imputation draws spread; for ONE prediction use the mean (or train with missingness)
res_sd = np.std(Xtr[obs, 1] - pred(w_noy, Xtr[obs][:, [0, 2]]))
print(f"residual sd of the fill (what 'multiple' imputation adds as noise): {res_sd:.3f}")
```

**Output (my run):**
```text
coefficient on x1  A (target-informed fill): 1.209   B (no target): 1.003   truth 1.000
serving R2  A: 0.763   B: 0.768   no missing at all: 0.878
x1, x2 missing, x0=1.0 -> [0.304 0.504]
residual sd of the fill (what 'multiple' imputation adds as noise): 0.954
```
The data are Gaussian and linear, which is the easy case; I did not test other shapes.

**Follow-ups:**
- When is multiple imputation worth using at all? When you want valid standard errors for a parameter, such as in an analysis report, not for a latency-bound score.
- What if the data are missing not at random? Then no fill is right; the missing flag or a model of the missingness is needed. See Q37 in this part (a feature missing in 15,000 of 100,000 rows).

**Common mistakes:** Refitting the imputer at serving time. Using the target inside the imputer for a predictive model. Ignoring the case of several fields missing together. No parity test between offline and online. Forgetting missing flags.

### Q45 ⭐ 🔴 After a consent change, the share of 2,000,000 users with no tracked last_login rose from 8% (160,000 users) to 30% (600,000 users), and a retention model that used that feature degraded. Explain how the meaning of the missing value changed, what you would do about training data from before and after the change, and how you would handle it in the model.
**Asked at:** Missing-data interview explainers (a PrachHub 'Missing Data, Imputation, And Selection Bias' concept page, ydata.ai 'understanding missing data mechanisms', a Towards Data Science 'Talking About Missing Data' article, a Daily Dose of Data Science post on three types of missing values); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Before the change a missing last_login mostly meant a user who really had not been seen; after it, most missing values mean "declined tracking", which says little about churn, so the feature's meaning changed and the model has to be told which kind of missing it is looking at.

**Clarifying questions:**
- Do we have a consent flag per user that we can use as a feature or as a filter? Why: it splits the two kinds of missing exactly.
- Can last_login be rebuilt from first-party server logs for users who declined tracking? Why: that would restore the value without breaking the consent.
- Are the users who declined different from the rest (region, age, plan)? Why: the decision to decline is itself related to behaviour.
- Is the label (churn) measured the same way before and after? Why: if the label changed too, I cannot compare eras.
- Are there legal limits on using the consent status as a model feature? Why: it may need to be excluded or aggregated.

**Approach:**
1. Do the arithmetic. 8% of 2,000,000 is 160,000 missing; 30% is 600,000. So 440,000 extra users (22% of all users) went missing, and the reason is a consent choice, not inactivity.
2. State the shift: before, missing and churn were strongly linked; after, the same value is a mix of the old group and many ordinary users. The old model treats all 600,000 as the risky group.
3. Split the feature into pieces: the value, a missing flag, and the consent status. Missing with tracking allowed means "no login seen" (as before). Missing with tracking declined means "unknown".
4. Training data: do not simply pool the two eras. Options: (a) train on post-change data only, once enough exists; (b) pool both eras with an era or consent column; (c) drop last_login for users who declined and rely on other features, such as server-side activity.
5. Validate on a recent time slice, with calibration per group (consented-missing, declined-missing, present), not only AUC.
6. Monitor the share of each group; a consent change can happen again.

**Metrics:**
- Missing share by consent group = users with no last_login in the group / users in the group.
- Churn rate by group = churned users / users in the group, before and after.
- Log loss and calibration (predicted churners / actual churners) by group.
- Guardrails: calibration within a set band in every group; no drop in recall for users who declined.

**Risks:**
- The model scores 600,000 users as high risk and wastes retention offers.
- Declining users may be a biased sample, so the post-change training set differs from the earlier one.
- Using consent status as a feature may be restricted.
- Dropping the feature loses its real signal for the consented users.

**What the interviewer scores:**
- Strong: explains that the reason for missing changed, not just the amount, and does the 440,000 arithmetic.
- Strong: separates missing-with-consent from missing-because-declined.
- Strong: has a clear plan for pre- and post-change data and checks calibration per group.
- Weak: imputes the mean and moves on.
- Weak: retrains on all data with no era or consent column.

**Example:** (illustrative numbers) Overall churn is 10%. Before the change, the 8% missing users churn at 40%, so present users churn at 7.39%. After the change, the same 8% of inactive users still churn at 40%, and the other 22% of users who declined tracking churn like present users (7.39%). The missing group then churns at 16.1%. The old model still scores all 600,000 missing users at 40%: 240,000 predicted churners against about 96,522 real ones. Log loss is 0.3574 for the old model and 0.2964 once the consent flag lets it tell the groups apart. Weak answer: "impute the missing logins." Strong answer: "Use consent to separate the two meanings and check calibration per group."

**Code:**
```python
# Q45: a missing value whose meaning changed after a consent change. Illustrative numbers.
import math
U = 2_000_000
before, after = 0.08, 0.30
assert int(U * before) == 160_000 and int(U * after) == 600_000
extra = int(U * after) - int(U * before)
print(f"extra missing users: {extra:,}  ({after-before:.0%} of users)")
assert extra == 440_000

# Before: every missing last_login is a user who really has not logged in (or a tracking gap tied to inactivity).
# Illustrative churn rates: overall 10%, missing group 40%.
overall = 0.10; q_inactive = 0.40
q_present = (overall - before * q_inactive) / (1 - before)
print(f"churn among users WITH last_login (before): {q_present:.4f}")
assert round(q_present, 4) == 0.0739

# After: the same 8% truly inactive users, plus 22% who simply declined tracking and behave like present users.
consent_miss = after - before
q_missing_after = (before * q_inactive + consent_miss * q_present) / after
print(f"churn among missing (after): {q_missing_after:.4f}")
assert round(q_missing_after, 3) == 0.161
check_overall = after * q_missing_after + (1 - after) * q_present
assert abs(check_overall - overall) < 1e-12        # overall churn is unchanged by construction

# Old model is a lookup: missing -> 0.40, present -> q_present.
exp_pred_churners = after * U * q_inactive
actual_churners_missing = after * U * q_missing_after
print(f"missing users scored at 0.40: predicted churners {exp_pred_churners:,.0f} vs actual {actual_churners_missing:,.0f}")
assert round(exp_pred_churners) == 240_000 and round(actual_churners_missing) == 96_522

def logloss(groups):
    # groups: list of (share, true_rate, predicted_rate)
    return -sum(s * (t * math.log(p) + (1 - t) * math.log(1 - p)) for s, t, p in groups)

old = logloss([(after, q_missing_after, q_inactive), (1 - after, q_present, q_present)])
# fixed model uses the consent flag: [missing and consented -> inactive], [missing, declined -> like present], [present]
fixed = logloss([(before, q_inactive, q_inactive), (consent_miss, q_present, q_present), (1 - after, q_present, q_present)])
best_possible = logloss([(after, q_missing_after, q_missing_after), (1 - after, q_present, q_present)])
print(f"log loss after the change  old model: {old:.4f}   with consent flag: {fixed:.4f}")
assert fixed < old
# Note: with consent flag known, 'fixed' beats the model that only sees missing/present
print(f"log loss of a model that only sees 'missing' but is recalibrated: {best_possible:.4f}")
assert fixed < best_possible < old
```

**Output (my run):**
```text
extra missing users: 440,000  (22% of users)
churn among users WITH last_login (before): 0.0739
churn among missing (after): 0.1609
missing users scored at 0.40: predicted churners 240,000 vs actual 96,522
log loss after the change  old model: 0.3574   with consent flag: 0.2964
log loss of a model that only sees 'missing' but is recalibrated: 0.3169
```
The churn rates are assumed, and the assumption that declined users behave like present users is the strongest one; the real number must come from labels.

**Follow-ups:**
- Why not recode missing as zero days? It tells the model "just logged in" or "long ago" depending on the sign, and it hides the consent change.
- What if consent is not available as a field? Then use proxies carefully, such as the platform and the date of the change, and measure how far calibration slips.

**Common mistakes:** Treating a missing share rise as a data bug and imputing. Mixing eras with no era marker. Checking only AUC. Ignoring consent restrictions on features. Assuming missing means the same thing as before.

### Q46 ⭐ 🔴 An ad system sees 500 conversions in 50,000,000 impressions (1 in 100,000), and training on all rows is too costly, so the team keeps all conversions and 1% of non-conversions. Explain how this affects the calibration and the sampling variance of the model, how to correct the predicted probabilities for bidding, and how you would evaluate offline.
**Asked at:** Imbalanced-data and fraud-evaluation guides (techinterview.org 'Handling Imbalanced Datasets in Machine Learning', Dataford fraud-evaluation prompts such as 'how do you evaluate a fraud detection model on imbalanced data', a KDnuggets piece on SMOTE misuse, a Coresignal 'class imbalance interview trap' post); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Keeping all conversions and 1% of non-conversions loses almost no information but inflates every predicted probability about 100 times, so I correct the odds by the sampling rate before bidding.

**Clarifying questions:**
- Was the 1% sample drawn at random from non-conversions, with no other filter? Why: the correction is only valid if the sampling rate is the same for every non-conversion.
- Is the model's output used as an absolute probability (bid = value x probability) or only to rank? Why: bids need calibration, ranking does not.
- Is the model logistic or a tree ensemble? Why: logistic regression shifts only the intercept; other models distort the probabilities more and need a calibration step.
- Do conversions arrive with a delay? Why: recent impressions look like non-conversions, and that biases the base rate.
- What decision does a probability error cost in money? Why: it sets how precise the calibration must be.

**Approach:**
1. Do the arithmetic. 500 in 50,000,000 is 1 in 100,000. After sampling there are 500 positives and about 499,995 negatives, a positive rate of 0.0999% or about 1 in 1,000. The sampled rate is about 99.9 times the true one.
2. Explain the effect on the model. Sampling on the outcome leaves the effect of features on the odds alone, but multiplies the odds by 1/r (r is the sampling rate of negatives, 0.01). For logistic regression the slopes stay right and the intercept shifts by about -ln(r), 4.605.
3. Correct the probability: p = r x ps / (1 - ps + r x ps), where ps is the model output. Equivalently odds_true = r x odds_sampled.
4. Sampling variance. The log-odds variance is roughly 1/positives + 1/negatives. With all 500 positives and 499,995 negatives it is 1.0010 times what you would get using all 49,999,500 negatives. The information is in the 500 positives, so the 1% sample loses almost nothing.
5. Evaluate offline. AUC is not changed by negative sampling in expectation, but log loss, calibration and expected revenue are. Evaluate with each sampled negative weighted by 1/r = 100, or correct the probabilities first.
6. Check calibration by bins on a time-based holdout, then confirm with a small online test, because offline data cannot show how bidding changes who is seen.

**Metrics:**
- Corrected probability p = r x ps / (1 - ps + r x ps), r = 0.01.
- Weighted log loss = sum of w x (-log likelihood) / sum of w, with w = 1 for conversions and 100 for sampled non-conversions.
- Calibration = mean corrected prediction / observed rate by decile (target near 1).
- Guardrails: confidence interval on conversions (500 events means a relative error of about 1/sqrt(500) = 4.5% on a rate), and no bid more than a set multiple of the value.

**Risks:**
- Forgetting the correction: bids about 100 times too high.
- Correcting an uncalibrated tree model with the formula and still being miscalibrated.
- With only 500 conversions, bin-level calibration is noisy; use few bins and intervals.
- Offline evaluation on the sampled set without weights reports a better metric than reality.

**What the interviewer scores:**
- Strong: gives the odds correction with the sampling rate and derives the 100x inflation.
- Strong: says variance is driven by positives, so sampling negatives is cheap.
- Strong: weights the evaluation and plans for calibration checks and online testing.
- Weak: "the model is fine because AUC is the same."
- Weak: rebalances to 50/50 and never corrects.

**Example:** (illustrative numbers) Sampled rate 0.000999 corrects to 0.00001001, close to the true 1 in 100,000. In the scaled simulation (2,000,000 rows, 3,057 conversions) the sample has 22,874 rows, the fitted slope is 0.985 (truth 1.0) and the intercept shifts by 4.654 (about 4.605). The mean raw prediction on all rows is 0.11824, far above the real rate of 0.00153. The corrected mean is 0.00155. Weighted log loss on the sample is 0.01077 against 0.01071 on all rows. Weak answer: "we balanced the data so it is fine." Strong answer: "Correct the odds by 0.01 and evaluate with weights 100."

**Code:**
```python
# Q46: keep all conversions, 1% of non-conversions. Illustrative numbers + a scaled simulation.
import numpy as np
imps, conv, r = 50_000_000, 500, 0.01
neg = imps - conv
print(f"base rate: 1 in {imps/conv:,.0f}")
assert imps // conv == 100_000
kept_neg = neg * r
rate_s = conv / (conv + kept_neg)
print(f"kept rows: {conv + kept_neg:,.0f}, sampled positive rate = {rate_s:.6f} (about 1 in {1/rate_s:,.0f})")
assert 1000 < 1 / rate_s < 1002

# prior correction: p = r*ps / (1 - ps + r*ps)
def correct(ps, r): return r * ps / (1 - ps + r * ps)
print(f"sampled p 0.001 -> corrected {correct(0.001, r):.8f}")
assert abs(correct(rate_s, r) - conv / imps) / (conv / imps) < 1e-6      # recovers 1e-5 exactly
print(f"uncorrected / true inflation at base rate: {rate_s/(conv/imps):.2f}x")
assert round(rate_s / (conv / imps), 1) == 99.9

# variance of a log-odds estimate ~ 1/positives + 1/negatives
v_full = 1 / conv + 1 / neg; v_samp = 1 / conv + 1 / kept_neg
print(f"variance ratio sampled/full = {v_samp/v_full:.4f}")
assert 1.0 < v_samp / v_full < 1.01

# scaled simulation: 2,000,000 rows, one feature, logistic truth (invented)
rng = np.random.default_rng(46)
n = 2_000_000
x = rng.normal(size=n)
true_b0, true_b1 = -7.0, 1.0
p = 1 / (1 + np.exp(-(true_b0 + true_b1 * x)))
y = rng.random(n) < p
print(f"simulated positives: {y.sum()}  rate {y.mean():.5f}")
keep = y | (rng.random(n) < r)
xs, ys = x[keep], y[keep].astype(float)
print(f"kept {keep.sum()} rows")

def fit(X, t, w=None, iters=25):
    A = np.column_stack([np.ones(len(X)), X]); b = np.zeros(2)
    w = np.ones(len(t)) if w is None else w
    for _ in range(iters):
        q = 1 / (1 + np.exp(-A @ b))
        g = A.T @ (w * (q - t)); H = (A * (w * q * (1 - q))[:, None]).T @ A
        b -= np.linalg.solve(H, g)
    return b
b = fit(xs, ys)
print(f"fitted on sample: intercept {b[0]:.3f}, slope {b[1]:.3f}   (truth {true_b0}, {true_b1})")
shift = b[0] - true_b0
print(f"intercept shift = {shift:.3f}, -ln(r) = {-np.log(r):.3f}")
assert abs(b[1] - 1.0) < 0.1 and abs(shift - (-np.log(r))) < 0.5

# calibration on the FULL data: raw vs corrected vs inverse-weight evaluation
ps = 1 / (1 + np.exp(-(b[0] + b[1] * x)))
pc = correct(ps, r)
print(f"mean predicted: raw {ps.mean():.5f}  corrected {pc.mean():.5f}  actual {y.mean():.5f}")
assert ps.mean() > 50 * y.mean() and abs(pc.mean() / y.mean() - 1) < 0.15

# offline evaluation on the sampled rows with weights: negatives weigh 1/r = 100
wts = np.where(ys == 1, 1.0, 1 / r)
def wlogloss(pp, yy, ww): return -(ww * (yy * np.log(pp) + (1 - yy) * np.log(1 - pp))).sum() / ww.sum()
pc_s = correct(1 / (1 + np.exp(-(b[0] + b[1] * xs))), r)
ll_w = wlogloss(pc_s, ys, wts)
ll_full = wlogloss(pc, y.astype(float), np.ones(n))
print(f"weighted log loss on sample {ll_w:.5f} vs full-data log loss {ll_full:.5f}")
assert abs(ll_w - ll_full) / ll_full < 0.1
```

**Output (my run):**
```text
base rate: 1 in 100,000
kept rows: 500,495, sampled positive rate = 0.000999 (about 1 in 1,001)
sampled p 0.001 -> corrected 0.00001001
uncorrected / true inflation at base rate: 99.90x
variance ratio sampled/full = 1.0010
simulated positives: 3057  rate 0.00153
kept 22874 rows
fitted on sample: intercept -2.346, slope 0.985   (truth -7.0, 1.0)
intercept shift = 4.654, -ln(r) = 4.605
mean predicted: raw 0.11824  corrected 0.00155  actual 0.00153
weighted log loss on sample 0.01077 vs full-data log loss 0.01071
```
The simulation uses one feature and a logistic truth, the case where the intercept shift is exact. Real data with many features and non-linear models needs an explicit calibration check.

**Follow-ups:**
- What about the 500 conversions themselves? Their count limits precision and the stability of the model; add features only if the positives can support them (see Q28 in this part, small data).
- What if the sample rate differs by segment? Use a different r per segment and correct each by its own rate. See also Q13 in this part (a model trained with 10% of non-fraud rows).

**Common mistakes:** Bidding on uncorrected probabilities. Evaluating log loss on the sampled set with no weights. Believing sampling negatives hurts variance much. Using a fixed 50/50 rebalance. Fitting calibration bins with too few conversions.

### Q47 ⭐ 🔴 A retailer forecasts sales for 2,000 stores, of which 600 have under 30 weeks of history, and the global model does poorly on those small series. Explain how you would borrow strength across stores, what hierarchical or partial-pooling idea you would use, how you would validate on short histories, and when you would fall back to a simple rule.
**Asked at:** Small-data overfitting prompts (Dataford pages such as 'how do you handle overfitting in a model trained on small clinical datasets' and a high-dimensional few-samples prompt); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** For the 600 short stores I would shrink each store's own estimate toward the average of similar stores, with a weight that grows with its history length, and use a plain seasonal-average rule when there is almost no history.

**Clarifying questions:**
- How long is "short": 4 weeks or 29? Why: below about 8 weeks even a pooled model is mostly the group prior.
- What store attributes do we have (region, format, size, opening date)? Why: pooling is only as good as the groups it borrows from.
- Is sales seasonal and are there promotions? Why: a store with under a year of data cannot estimate its own seasonal profile; it must borrow one.
- What is the forecast horizon and the cost of an over-forecast versus under-forecast? Why: it fixes the loss to validate on.
- Are the short stores new stores or old stores with gaps? Why: a new store has a ramp-up and a gap store does not.

**Approach:**
1. Say the problem. 600 of 2,000 stores (30%) have under 30 weeks of data, so their own average is noisy.
2. Partial pooling: store level = group level + store effect, and the store effect is shrunk toward zero. For a store with n weeks, the estimate is w x (own mean) + (1 - w) x (group mean), with w = n / (n + k) and k = weekly noise variance / variance between stores.
3. Estimate the two variances from the data (method of moments, or a mixed-effects or Bayesian hierarchical model). Share seasonality and trend across the group and let stores differ only in level, and optionally in slope.
4. Add features that let the global model place a store: format, region, size, opening cohort. A global model with those plus a store embedding that is regularised is the same idea in a different form.
5. Validate on short histories: hold out the last weeks of each short store (a rolling origin), and report error by history-length bucket, short stores only, against the store-only and global-only baselines.
6. Fall back to a rule when history is under a threshold (for example under 8 weeks or a brand-new store): the group's seasonal average scaled by the store's size, until the pooled model beats it on validation.

**Metrics:**
- Forecast error on short stores: MAE or squared error over held-out weeks, by history bucket; scale-free versions (MASE or WAPE = sum of absolute errors / sum of actuals) to compare stores.
- Shrinkage weight w = n / (n + k).
- Guardrails: no worse than the simple rule in any bucket; interval coverage near the nominal level.

**Risks:**
- Shrinking toward the wrong group (a mixed-format group) pulls the estimate the wrong way.
- Over-shrinking truly unusual stores (a store near an event venue).
- Estimated variances from few stores are noisy.
- New stores have a ramp-up that a flat level does not capture.

**What the interviewer scores:**
- Strong: gives the shrinkage formula and says what it does with 8 versus 104 weeks.
- Strong: validates on short histories only, by bucket, not on the pooled average.
- Strong: names the fallback rule and the point at which the model must beat it.
- Weak: "train a bigger global model."
- Weak: validates with a random split that leaks weeks from the same store.

**Example:** (illustrative numbers) In the code, 2,000 stores have a true spread of 0.30 between stores and weekly noise of 0.80 (log scale). The true k is 0.80 squared / 0.30 squared = 7.1, and the code estimates it from the data as 7.6. A store with 8 weeks gets weight 0.51 on its own mean, a store with 29 weeks gets 0.79, and one with 104 weeks gets 0.93. The squared error for short stores falls from 0.0383 (store mean only) to 0.0266 with pooling; the global mean alone gives 0.0842. For long stores the gain is small (0.0064 to 0.0060). Weak answer: "use the store's average." Strong answer: "Shrink toward a similar-store average by n / (n + 7.6)."

**Code:**
```python
# Q47: partial pooling for short-history stores. Illustrative simulation of weekly log-sales.
import numpy as np
rng = np.random.default_rng(47)
S, SHORT = 2_000, 600
assert SHORT / S == 0.30
n_hist = np.concatenate([rng.integers(8, 30, SHORT), np.full(S - SHORT, 104)])   # weeks of history
tau, sigma, m = 0.30, 0.80, 5.0           # store-level spread, weekly noise, grand mean (log scale)
mu = rng.normal(m, tau, S)                # true store level (what we want to forecast)
means = np.array([rng.normal(mu[i], sigma, n_hist[i]).mean() for i in range(S)])

# method-of-moments estimates of the variance components, from the data only
# weekly noise: pooled within-store variance of 300 long-history stores (fresh draws stand in for their weekly data)
long_i = np.where(n_hist == 104)[0]
sig2_hat = np.mean([rng.normal(mu[i], sigma, 104).var(ddof=1) for i in long_i[:300]])
grand = np.average(means, weights=n_hist)
tau2_hat = max(np.var(means, ddof=1) - np.mean(sig2_hat / n_hist), 1e-6)
print(f"sigma_hat {np.sqrt(sig2_hat):.3f} (true {sigma})   tau_hat {np.sqrt(tau2_hat):.3f} (true {tau})")
assert abs(np.sqrt(tau2_hat) - tau) < 0.06 and abs(np.sqrt(sig2_hat) - sigma) < 0.05

w = n_hist / (n_hist + sig2_hat / tau2_hat)          # shrinkage weight on the store's own mean
pooled = w * means + (1 - w) * grand
k = sig2_hat / tau2_hat
print(f"k = sigma^2/tau^2 = {k:.2f}; weight on own mean: 8 weeks {8/(8+k):.2f}, 29 weeks {29/(29+k):.2f}, 104 weeks {104/(104+k):.2f}")
assert 6 < k < 9

def mse(est, idx): return float(np.mean((est[idx] - mu[idx]) ** 2))
sh = np.arange(SHORT); lg = np.arange(SHORT, S)
print(f"{'':22s}{'short (600)':>12s}{'long (1400)':>12s}")
for name, est in [("store mean only", means), ("global mean only", np.full(S, grand)), ("partial pooling", pooled)]:
    print(f"{name:22s}{mse(est, sh):12.4f}{mse(est, lg):12.4f}")
assert mse(pooled, sh) < mse(means, sh) and mse(pooled, sh) < mse(np.full(S, grand), sh)
assert mse(pooled, sh) <= mse(means, sh) * 0.8
# 8-week stores: standard error of own mean vs shrunk
print(f"SE of own mean at 8 weeks: {sigma/np.sqrt(8):.3f}; at 104 weeks: {sigma/np.sqrt(104):.3f}; tau = {tau}")
assert abs(sigma / np.sqrt(8) - tau) < 0.03 and sigma / np.sqrt(104) < tau / 3
```

**Output (my run):**
```text
sigma_hat 0.808 (true 0.8)   tau_hat 0.294 (true 0.3)
k = sigma^2/tau^2 = 7.58; weight on own mean: 8 weeks 0.51, 29 weeks 0.79, 104 weeks 0.93
                       short (600) long (1400)
store mean only             0.0383      0.0064
global mean only            0.0842      0.0895
partial pooling             0.0266      0.0060
SE of own mean at 8 weeks: 0.283; at 104 weeks: 0.078; tau = 0.3
```
The data are simulated with equal weekly noise and no trend or season, the simplest case. The gain depends on how big the weekly noise is compared with the spread between stores.

**Follow-ups:**
- Why does a long store barely change? Its own mean is already precise (standard error 0.078), so the weight is 0.93.
- How does this tie to a global model? A global model with store features and a regularised store embedding is a partial-pooling model; the regularisation strength plays the role of k. See Q28 in this part (small data and cross-validation).

**Common mistakes:** Validating with random rows rather than the end of each store's history. Reporting a pooled error that hides the short stores. Using the same shrinkage for every group. Having no fallback for a new store. Treating the group mean as truth.

### Q48 ⭐ 🔴 A labelling vendor changed its guidelines, and the positive rate in the newest batch of 10,000 labelled rows is 12% against 8% in each of the previous six batches. The training pipeline ingested the batch automatically. Explain how a label-drift gate should work, how you would decide whether the shift is real or a guideline change, and what you would do with the batch.
**Asked at:** Data-quality-gate material (a OneUptime 2026 data-pipeline validation post, a DesignGurus Great Expectations answer, an MLJourney post on quality checks for ML, a Pebblous Great Expectations report); practitioner posts rather than interview banks, so scenario is partly editor-designed; search snippets only, not opened
**Say this first (1 line):** A label-drift gate compares each new labelled batch with the recent batches before it is trained on; here 12% against 8% is about 14.7 standard deviations away, so the batch should be held back, and a re-label test on known items tells us whether the guideline changed.

**Clarifying questions:**
- How much do batch rates normally move, beyond sampling noise? Why: it sets the gate limit; six batches at exactly 8% suggest a very stable process.
- Does the vendor tell us the guideline version per batch? Why: the version is the first thing to check, and it should be a column.
- Are the new batch's items drawn from the same source and period as earlier ones? Why: a real change in the input mix would also move the rate.
- Do we keep gold items (previously labelled, trusted) that can be sent again? Why: they separate a guideline change from a real shift.
- What is the cost of a bad batch in training versus the cost of waiting? Why: it sets whether to block or to train with a flag.

**Approach:**
1. Gate before ingest. Compute the batch positive rate and compare it with the previous batches. Expected positives at 8% of 10,000 are 800, with standard deviation sqrt(10,000 x 0.08 x 0.92) = 27.1. We see 1,200, so z = 14.74. Add a margin for normal wobble: limit = 8% + 3 x 0.27 points + 0.5 points = 9.31%. 12% trips it.
2. Hold the batch: quarantine, do not train on it, and tell the vendor and the owner.
3. Decide real shift versus guideline change with three checks: (a) re-send gold items and see how many flip; (b) check the model's mean score on the batch (if inputs moved, scores move; if only labels moved, scores stay); (c) read the vendor's guideline change log and compare 30 or so disagreements by hand.
4. If it is a guideline change, choose one definition. Either relabel the new batch to the old guideline, or relabel old data to the new one if the new one is better, or train with a guideline-version feature. Do not mix silently.
5. If it is a real shift in the world, accept the batch, record it, and check the model for drift.
6. Fix the pipeline: the gate must run in the pipeline and block, and the vendor contract must name guideline changes.

**Metrics:**
- Batch positive rate = positive rows / rows in batch.
- z = (batch positives - expected) / sqrt(n p (1 - p)), with a gate limit using a margin.
- Gold flip rate = gold items whose label changed / gold items re-sent, split by direction.
- Sign-test p-value on the flips (neg-to-pos vs pos-to-neg).
- Guardrails: per-class rate, per-source rate, and the mean model score on the batch.

**Risks:**
- A gate with only binomial noise fires on harmless wobble, and teams learn to bypass it.
- Using the batch anyway teaches the model a different positive definition.
- Gold items that annotators recognise are not a clean test.
- A real shift and a guideline change can happen together.

**What the interviewer scores:**
- Strong: computes the z-score by hand and builds in a tolerance.
- Strong: uses gold items and model scores to tell label change from input change.
- Strong: blocks the batch and fixes the process with the vendor.
- Weak: "retrain on everything, the model will learn it."
- Weak: concludes it is a guideline change without any test.

**Example:** (illustrative numbers) 1,200 observed against 800 expected; z = 14.74. The gold test sends 500 old items back (40 positive, 8%). After relabelling there are 60 positive (12%): 24 negative-to-positive flips and 4 positive-to-negative flips. A one-sided sign test over the 28 flips gives p = 9.0e-05. The model's mean score on the new batch is 0.081 against 0.080 earlier (illustrative, not computed), so inputs look the same. Weak answer: "the rate went up, retrain." Strong answer: "Quarantine it, re-label gold items, and fix the definition before training."

**Code:**
```python
# Q48: label-drift gate on a labelling batch. Illustrative numbers.
import math
from math import comb, sqrt
n, rate_new, rate_old, prev_batches = 10_000, 0.12, 0.08, 6
pos_new, pos_exp = int(n * rate_new), int(n * rate_old)
assert (pos_new, pos_exp) == (1200, 800)

sd = sqrt(n * rate_old * (1 - rate_old))
z = (pos_new - pos_exp) / sd
print(f"expected positives {pos_exp}, sd {sd:.1f}, observed {pos_new}, z = {z:.2f}")
assert round(sd, 1) == 27.1 and round(z, 2) == 14.74
sd_rate = sqrt(rate_old * (1 - rate_old) / n)
print(f"sampling sd of a batch rate: {sd_rate*100:.2f} points; shift is {(rate_new-rate_old)/sd_rate:.1f} sd")
# gate with a margin for real batch-to-batch wobble: use 3 x binomial sd plus 0.5 point allowance
limit = rate_old + 3 * sd_rate + 0.005
print(f"gate upper limit {limit:.4f}; batch {rate_new:.4f} trips: {rate_new > limit}")
assert rate_new > limit and 0.09 < limit < 0.095

# Real shift or guideline change? Re-send 500 gold items (previously labelled, 8% positive = 40).
gold_n, gold_pos_before = 500, 40
pos_to_neg, neg_to_pos = 4, 24                     # illustrative re-labels by the new guideline
gold_pos_after = gold_pos_before - pos_to_neg + neg_to_pos
print(f"gold positives before {gold_pos_before} ({gold_pos_before/gold_n:.0%}), after {gold_pos_after} ({gold_pos_after/gold_n:.1%})")
assert gold_pos_after == 60 and gold_pos_after / gold_n == 0.12
flips = pos_to_neg + neg_to_pos
p_sign = sum(comb(flips, k) for k in range(neg_to_pos, flips + 1)) / 2 ** flips      # one-sided
print(f"flips {flips}: {neg_to_pos} neg->pos vs {pos_to_neg} pos->neg, one-sided sign-test p = {p_sign:.2e}")
assert p_sign < 1e-3

# Second check: model scores on the batch. A calibrated model's mean score tells whether the INPUTS moved.
mean_score_new, mean_score_old = 0.081, 0.080
print(f"mean model score new {mean_score_new:.3f} vs old {mean_score_old:.3f}: inputs look the same, labels moved")
# Expected size of the shift if only the guideline changed: new positives among old negatives
extra = rate_new - rate_old
print(f"label-only shift of {extra*100:.0f} points means about {extra*n:.0f} of 10,000 rows relabelled to positive")
assert round(extra * n) == 400

# Fraction of old-negative rows that the new guideline turns positive (from the gold test)
frac = neg_to_pos / (gold_n - gold_pos_before)
print(f"gold flip rate neg->pos: {frac:.3f} ({neg_to_pos}/{gold_n - gold_pos_before})")
assert round(frac, 4) == 0.0522
```

**Output (my run):**
```text
expected positives 800, sd 27.1, observed 1200, z = 14.74
sampling sd of a batch rate: 0.27 points; shift is 14.7 sd
gate upper limit 0.0931; batch 0.1200 trips: True
gold positives before 40 (8%), after 60 (12.0%)
flips 28: 24 neg->pos vs 4 pos->neg, one-sided sign-test p = 9.00e-05
mean model score new 0.081 vs old 0.080: inputs look the same, labels moved
label-only shift of 4 points means about 400 of 10,000 rows relabelled to positive
gold flip rate neg->pos: 0.052 (24/460)
```
The two model-score numbers and the flip counts are assumed inputs to show the logic, not results.

**Follow-ups:**
- What if the shift is real? Then the gold items would not flip and the model scores would rise with the labels; I would accept the batch and monitor the model.
- Should the gate be a fixed number? Use a limit set from past batch-to-batch variation plus a small margin, reviewed as more batches arrive. See Q30 in this part (a pipeline that loaded 62% of normal rows).

**Common mistakes:** No gate on labels (only on schema and nulls). Comparing the rate with one prior batch. Treating a binomial limit as the whole story. Mixing guideline versions silently. Never sending gold items back.

### Q49 ⭐ 🔴 A medical imaging data set has 1,200 patients with six scans each (7,200 scans) and only 25 positive patients, and the team wants five-fold cross-validation. Explain why a plain stratified split by scan is wrong, how you would split by patient while keeping positives balanced (about five per fold), and how you would report the uncertainty of the result.
**Asked at:** Splitting and leakage guides (an arXiv paper on panel-data misuse of ML, a LetsDataScience 'science of data splitting' post, a Towards Data Science 'seven common causes of data leakage' article, an APXML recommender-splitting lesson); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** A split by scan puts the same patient's scans on both sides, so the test is partly memorised; I would split by patient, with the 25 positive patients dealt 5 to each fold, and report an interval that treats patients, not scans, as the sample.

**Clarifying questions:**
- Is the label per patient or per scan? Why: with a patient-level label, all six scans share it and cannot be split.
- Are the scans of one patient from the same session or over time? Why: the closer they are, the stronger the leakage.
- Is there any other grouping, such as hospital or scanner? Why: a model can learn the scanner, so folds may need that group as well.
- What is the clinical decision, and what sensitivity and specificity matter? Why: it sets the headline metric and the threshold.
- Will the model run on patients it has never seen? Why: it almost certainly will, which is what the split must copy.

**Approach:**
1. Do the arithmetic. 1,200 patients x 6 scans = 7,200 scans. Five folds give 240 patients and 1,440 scans per fold. 25 positive patients over five folds gives 5 per fold (2.08% prevalence).
2. Why scan-level is wrong: scans of one patient look alike, so a model can recognise the patient and recall the label. Training and test rows are not independent.
3. Split by patient: all six scans go to one fold. Stratify at the patient level: shuffle the positives and deal them round-robin to folds (5 each), then do the same for the negatives (235 each).
4. Aggregate scan scores to one patient score (mean or max) and score patients, since the decision is per patient.
5. Uncertainty: with 25 positives the interval is wide. Report the interval from a patient-level bootstrap or a Wilson interval on patients, not on scans. Repeat the cross-validation with several seeds to show split sensitivity, but do not treat the repeats as independent evidence.
6. Keep one final holdout of patients (or an external site) if the data allow it, since 25 positives are used up by the cross-validation.

**Metrics:**
- Patient-level sensitivity = positive patients flagged / 25; specificity = negative patients not flagged / 1,175.
- Patient-level AUC from pooled out-of-fold scores.
- 95% interval by patient bootstrap, or Wilson for a proportion: with 20 of 25, (0.61, 0.91).
- Guardrails: folds have 240 patients and 5 positives each; no patient appears in two folds.

**Risks:**
- Per-fold metrics with 5 positives swing by 0.2 per miss, so do not compare folds one by one.
- Tuning the threshold or hyper-parameters inside the same folds inflates the result; use nested folds.
- A scanner or site effect hidden inside the patient groups.
- Reporting the scan-level interval, which is far too narrow.

**What the interviewer scores:**
- Strong: explains the leakage and says the unit of analysis is the patient.
- Strong: deals positives round-robin, checks 5 per fold, and states the arithmetic.
- Strong: reports an interval on patients and warns about 25 positives.
- Weak: "use stratified K-fold" with no groups.
- Weak: reports a precise-looking number such as 0.80 plus or minus 0.07 from scans.

**Example:** (illustrative numbers) The code makes 1,200 patients with a fixed signature each and labels that are random noise, so the true skill is zero. A scan-level split finds 100% of the positive scans (1-nearest-neighbour recall), because patients sit in about 3.69 folds on average. The patient-level split finds 7%. If a real model gets 20 of 25 positive patients, sensitivity is 0.80 with a Wilson interval of (0.61, 0.91) and a patient bootstrap of (0.64, 0.96). A scan-level calculation with 120 of 150 positive scans gives (0.73, 0.86), too narrow. Weak answer: "stratified five-fold, 0.80." Strong answer: "Patient-level folds with 5 positives each, and the interval is 0.61 to 0.91."

**Code:**
```python
# Q49: patient-level folds for 1,200 patients x 6 scans, 25 positive patients. Illustrative.
import numpy as np
from math import sqrt
rng = np.random.default_rng(49)
P, SC, POS, K = 1_200, 6, 25, 5
assert P * SC == 7_200 and P // K == 240 and POS // K == 5
print(f"patients per fold {P//K}, scans per fold {P*SC//K}, positives per fold {POS//K}, prevalence {POS/P:.2%}")

pat_y = np.zeros(P, int); pat_y[rng.choice(P, POS, replace=False)] = 1
# patient-level stratified folds: deal positives and negatives round-robin after shuffling
fold = np.empty(P, int)
for cls in (1, 0):
    ids = rng.permutation(np.where(pat_y == cls)[0])
    fold[ids] = np.arange(len(ids)) % K
for k in range(K):
    m = fold == k
    assert m.sum() == 240 and pat_y[m].sum() == 5
print("every fold: 240 patients, 5 positive patients -> checked")

# Scans: each patient has a fixed 'signature' (no real disease signal at all) plus scan noise.
D = 20
sig = rng.normal(size=(P, D))
Xs = np.repeat(sig, SC, axis=0) + 0.3 * rng.normal(size=(P * SC, D))
pid = np.repeat(np.arange(P), SC); ys = pat_y[pid]

def nn_pred(tr, te):           # 1-nearest-neighbour in numpy
    A, B = Xs[tr], Xs[te]
    d = (B ** 2).sum(1)[:, None] - 2 * B @ A.T + (A ** 2).sum(1)[None]
    return ys[tr][d.argmin(1)]

def cv_recall(scan_fold):
    hit = tot = 0
    for k in range(K):
        te = np.where(scan_fold == k)[0]; tr = np.where(scan_fold != k)[0]
        p = nn_pred(tr, te); pos = ys[te] == 1
        hit += (p[pos] == 1).sum(); tot += pos.sum()
    return hit / tot
# (a) plain stratified split by scan label (leaks patients)
scan_fold = np.empty(P * SC, int)
for cls in (1, 0):
    ids = rng.permutation(np.where(ys == cls)[0]); scan_fold[ids] = np.arange(len(ids)) % K
# (b) split by patient
pat_scan_fold = fold[pid]
ra, rb = cv_recall(scan_fold), cv_recall(pat_scan_fold)
print(f"recall on positive scans, labels are pure patient noise: scan split {ra:.2f}, patient split {rb:.2f}")
assert ra > 0.9 and rb < 0.2
nf_scan = np.mean([len(set(scan_fold[pid == i])) for i in range(P)])
nf_pat = np.mean([len(set(pat_scan_fold[pid == i])) for i in range(P)])
print(f"average number of folds a patient appears in: scan split {nf_scan:.2f}, patient split {nf_pat:.2f}")
assert nf_scan > 3 and nf_pat == 1

# Uncertainty: 25 positive patients. Wilson interval for sensitivity 20/25 (illustrative result).
def wilson(x, n, z=1.96):
    p = x / n; c = (p + z * z / (2 * n)) / (1 + z * z / n)
    h = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return c - h, c + h
lo, hi = wilson(20, 25)
print(f"sensitivity 20/25 = 0.80, Wilson 95% interval ({lo:.2f}, {hi:.2f})")
assert (round(lo, 2), round(hi, 2)) == (0.61, 0.91)
# the same 20/25 if the folds were evaluated one by one (5 positives each): per-fold values are just 0..5 / 5
print("per fold with 5 positives, one miss moves sensitivity by", 1 / 5)
# naive scan-level interval pretends 150 independent positive scans
lo2, hi2 = wilson(120, 150)
print(f"naive scan-level interval, 120/150: ({lo2:.2f}, {hi2:.2f})  -> too narrow, scans are not independent")
assert hi2 - lo2 < hi - lo
# patient bootstrap of the 25 positives
rng2 = np.random.default_rng(1)
res = np.array([1] * 20 + [0] * 5)
bs = [rng2.choice(res, 25).mean() for _ in range(5000)]
print("patient bootstrap 95%:", np.round(np.percentile(bs, [2.5, 97.5]), 2))
```

**Output (my run):**
```text
patients per fold 240, scans per fold 1440, positives per fold 5, prevalence 2.08%
every fold: 240 patients, 5 positive patients -> checked
recall on positive scans, labels are pure patient noise: scan split 1.00, patient split 0.07
average number of folds a patient appears in: scan split 3.69, patient split 1.00
sensitivity 20/25 = 0.80, Wilson 95% interval (0.61, 0.91)
per fold with 5 positives, one miss moves sensitivity by 0.2
naive scan-level interval, 120/150: (0.73, 0.86)  -> too narrow, scans are not independent
patient bootstrap 95%: [0.64 0.96]
```
The signature data are artificial; the point is that a no-skill model looks perfect under a scan split. The 120 of 150 scan result and 20 of 25 patient result are made-up counts for the interval calculation.

**Follow-ups:**
- Why not leave-one-patient-out? It has 1,200 fits and the same 25 positives; the folds do not add data, they only lower the bias a little.
- What if the folds cannot be exactly balanced? Use stratified group folds and report the actual positives per fold; with 25 and five folds it is exact.

**Common mistakes:** Splitting by scan. Stratifying on the scan label only. Reporting an interval based on scans. Using fold-level metrics with 5 positives each. Tuning on the same folds that are reported.

### Q50 ⭐ 🔴 Users flag 30,000 of 1,000,000 posts as harmful (3%), and a review of 500 randomly sampled flags found that 200 were fine. A model is trained on user flags as labels, and a coordinated group appears to be mass-flagging a topic. Explain how you would treat these labels, how you would detect coordinated flagging, and how you would measure the real precision of the flags.
**Asked at:** Noisy-label and annotator-disagreement material (Tanno et al., CVPR 2019 on annotator confusion matrices; a Codemia data-labelling course page); research and course pages rather than interview banks, so the scenario is partly editor-designed; search snippets only, not opened
**Say this first (1 line):** User flags are noisy, biased and can be attacked, so I would not train on them as ground truth; I would measure their precision with a stratified human review and use only reviewed or reputation-weighted flags as labels.

**Clarifying questions:**
- Who can flag, and can one account flag many posts? Why: it sets how easy mass flagging is and which signals exist.
- Do we have flagger identifiers, timestamps and account ages? Why: detection of coordination needs them.
- What does a reviewer do with a flag, and is the review sample random? Why: the 500 random flags measure precision only if the sample is random and the reviewers are right.
- What is the cost of a false flag (a post taken down) and of a miss? Why: it sets the target precision and recall.
- Is the suspect topic known to be a target of campaigns? Why: it guides the strata for the review.

**Approach:**
1. Do the arithmetic. 30,000 of 1,000,000 posts is 3%. In the review, 300 of 500 flags were harmful: precision 60%, with an interval of about plus or minus 4.3 points (95%). That implies about 18,000 harmful and 12,000 false flags among the 30,000. This measures precision only. It tells nothing about harmful posts nobody flagged (recall).
2. Treat flags as weak labels, not truth. Use them to prioritise review, and train on reviewed labels, or on flags weighted by the flagger's track record.
3. Detect coordination: build a flagger-by-post graph and look for accounts that flag the same posts (co-flag overlap), flag in short bursts, are new, or have a low rate of reviewer-confirmed flags. Compare flag volume by topic with its usual level.
4. Handle the labels: remove or down-weight flags from suspected groups, count one flag per cluster of coordinated accounts, and exclude the attacked topic from training unless reviewed.
5. Measure real precision with a stratified sample. Strata: the suspect topic, the rest, and maybe flag counts. Sample each, weight by stratum size, and report an interval.
6. Close the loop: send reviewer outcomes back to compute each flagger's reliability and update the weights.

**Metrics:**
- Flag precision = flags that reviewers confirm / flags reviewed, per stratum and overall: P = sum over strata of (flags in stratum / all flags) x (precision in stratum).
- Co-flag count between two accounts = number of posts both flagged; flagger reliability = confirmed flags / flags reviewed.
- Interval: 1.96 x sqrt of the weighted sum of p(1-p)/n per stratum.
- Guardrails: coverage of the review sample in every stratum, and no model use of flags from suspected clusters.

**Risks:**
- Training on raw flags teaches the model to flag a topic users dislike, not harm.
- A detection rule that is too loose flags honest users who flag viral posts together.
- Reviewers see only flagged posts, so recall is unknown without a sample of unflagged posts.
- Attackers adapt by spreading flags over time and accounts.

**What the interviewer scores:**
- Strong: says 60% precision is flag precision only, and that recall needs a sample of unflagged posts.
- Strong: gives a graph-based detection idea and a stratified estimate.
- Strong: weights or filters flags, and keeps reviewed labels as the truth.
- Weak: "train on flags, 60% are right so it is fine."
- Weak: deletes all flags on the topic and loses the real harm there.

**Example:** (illustrative numbers) Suppose 6,000 flags (20%) sit in the suspect topic at 20% precision and the other 24,000 at 70%. Overall precision is 0.2 x 0.20 + 0.8 x 0.70 = 60%, the same as the random review. A random 500 would hold 100 suspect and 400 other flags: 20 + 280 = 300 harmful and 200 fine, matching the finding. A stratified review of 250 per stratum finds 0.232 and 0.700 and an overall 0.606, plus or minus 0.047. In the graph demo (1,500 honest flaggers, 100 coordinated ones), a rule "at least 5 partners sharing at least 4 flagged posts" catches 100 of 100 coordinated accounts and 0 of 1,500 honest ones; sharing at least 1 or 2 posts wrongly flags 1,500 and 1,359 honest users. Weak answer: "60% precise, train on it." Strong answer: "The 60% hides 20% in one topic; weight, filter and review."

**Code:**
```python
# Q50: user flags as labels, a coordinated flagging group, and real precision. Illustrative.
import numpy as np
from math import sqrt
N, F = 1_000_000, 30_000
assert F / N == 0.03
n_rev, n_fine = 500, 200
prec = (n_rev - n_fine) / n_rev
se = sqrt(prec * (1 - prec) / n_rev)
print(f"precision of flags = {n_rev-n_fine}/{n_rev} = {prec:.0%}, 95% interval +/- {1.96*se*100:.1f} points")
assert prec == 0.60 and round(1.96 * se, 3) == 0.043
print(f"implied harmful among flagged: {prec*F:,.0f}; false flags: {(1-prec)*F:,.0f}")
assert prec * F == 18_000

# Stratified view: 20% of flags sit in the suspect topic (illustrative strata precisions)
s_share, s_prec, o_prec = 0.20, 0.20, 0.70
overall = s_share * s_prec + (1 - s_share) * o_prec
print(f"suspect stratum {s_share*F:,.0f} flags at {s_prec:.0%}, rest {(1-s_share)*F:,.0f} at {o_prec:.0%} -> overall {overall:.0%}")
assert abs(overall - 0.60) < 1e-12
# a random 500 contains 100 suspect + 400 other flags: 20 + 280 = 300 fine? (harmful)
print(f"expected harmful in a random 500: {100*s_prec + 400*o_prec:.0f} -> fine {500 - (100*s_prec + 400*o_prec):.0f}")
assert 100 * s_prec + 400 * o_prec == 300

# Stratified sample, 250 per stratum, with stratum weights
rng = np.random.default_rng(50)
a = rng.random(250) < s_prec; b = rng.random(250) < o_prec
ea, eb = a.mean(), b.mean()
est = s_share * ea + (1 - s_share) * eb
se_s = sqrt(s_share**2 * ea*(1-ea)/250 + (1-s_share)**2 * eb*(1-eb)/250)
print(f"stratified: suspect {ea:.3f}, rest {eb:.3f}, overall {est:.3f} +/- {1.96*se_s:.3f}")
assert abs(est - 0.60) < 0.08

# Detecting coordinated flaggers: co-flag overlap in a small flag graph (scaled down)
posts, honest, coord = 5_000, 1_500, 100
M = np.zeros((honest + coord, posts), np.float32)
viral = rng.choice(posts, 60, replace=False)              # genuinely harmful posts many honest users flag
for u in range(honest):                                   # honest: 3 viral + 3 random posts
    M[u, rng.choice(viral, 3, replace=False)] = 1
    M[u, rng.choice(posts, 3, replace=False)] = 1
target = rng.choice(posts, 300, replace=False)            # the topic under attack
for u in range(honest, honest + coord):                   # coordinated: 30 of the same 300 posts
    M[u, rng.choice(target, 30, replace=False)] = 1
C = M @ M.T; np.fill_diagonal(C, 0)
truth = np.arange(honest + coord) >= honest
res = {}
for t in (1, 2, 3, 4):
    suspect = (C >= t).sum(1) >= 5                        # >=5 partners sharing >=t flagged posts
    tp = int((suspect & truth).sum()); fp = int((suspect & ~truth).sum())
    res[t] = (tp, fp)
    print(f"shared posts >= {t}: caught {tp}/{coord}, false alarms {fp}/{honest}")
assert res[4][0] >= 95 and res[4][1] <= 2
assert res[1][1] > 100 and res[1][1] > res[2][1] >= res[3][1] >= res[4][1]   # a loose rule flags honest users
```

**Output (my run):**
```text
precision of flags = 300/500 = 60%, 95% interval +/- 4.3 points
implied harmful among flagged: 18,000; false flags: 12,000
suspect stratum 6,000 flags at 20%, rest 24,000 at 70% -> overall 60%
expected harmful in a random 500: 300 -> fine 200
stratified: suspect 0.232, rest 0.700, overall 0.606 +/- 0.047
shared posts >= 1: caught 100/100, false alarms 1500/1500
shared posts >= 2: caught 100/100, false alarms 1359/1500
shared posts >= 3: caught 100/100, false alarms 0/1500
shared posts >= 4: caught 100/100, false alarms 0/1500
```
The graph is simulated and easy (honest users share few posts), so the perfect detection is a property of the setup; a real system needs tuning on reviewed cases.

**Follow-ups:**
- How do I estimate recall of the flag system? Review a random sample of all posts (or of unflagged posts in strata) and count harmful posts that nobody flagged.
- Could the model replace flags? It can rank posts for review, but its labels must be checked against reviewers, and flag data remain an input signal, not a label. See Q29 in this part (labels only for rule-flagged transactions).

**Common mistakes:** Treating the review of flagged items as a measure of recall. Using raw flags as ground truth. Estimating one global precision when the strata differ. Banning a whole topic from training. Using a loose co-flag rule that hits honest users.

