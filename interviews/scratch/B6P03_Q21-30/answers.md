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
1. Explain the spread: each fold has 8 positives and 72 negatives, so each fold AUC rests on 8 x 72 = 576 positive-negative pairs, and a single positive shifts it by about 0.014.
2. Quantify uncertainty: pooled out-of-fold AUC over all 400 rows, with a bootstrap confidence interval (resampling rows, or patients if grouped).
3. Repeated stratified cross-validation (for example 5-fold, repeated 10 times) smooths the split noise, but it does not remove the noise of having only 40 positives; say so.
4. Select models with nested cross-validation (inner loop picks, outer loop scores) or a very small search space; keep the final model simple and regularised.
5. Compare with a baseline (a simple model or the current rule) using the same folds and a paired comparison; a model must beat the baseline by more than the noise.
6. Be honest in the answer: "The best guess is an AUC near 0.76 and the plausible range is about 0.65 to 0.85; that is not enough to promise a gain."
7. Suggest what would help: more positives, a pilot or shadow run, or a decision rule that is robust to this uncertainty.

**Metrics:**
- AUC = probability a random positive is scored above a random negative.
- Pooled out-of-fold AUC with a 95% bootstrap interval; fold range as a diagnostic only.
- Hanley-McNeil style standard error depends on the positive count (about 0.04 for 40 positives at AUC near 0.76, in my simulation 0.039).
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
