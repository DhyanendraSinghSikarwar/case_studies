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
