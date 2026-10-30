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
