### Q24 ⭐⭐ 🔴 Estimating model performance without labels. Explain the confidence-based idea (if probabilities are calibrated, expected accuracy and expected confusion matrix follow from the scores), why it fails under concept drift and miscalibration, and how it relates to the commercial NannyML CBPE method without reproducing its internals. Implement expected accuracy and expected precision from scores, test it on a calibrated simulation, a covariate shift where calibration holds, and a concept drift where it fails, and state the limits.
**Asked at:** MLOps interview question banks and guides (K21Academy '47 MLOps interview questions' PDF, Towards AI '101 ML LLM agentic AIOps interview questions', DataCamp MLOps interview questions, The Interview Guys MLOps post, wecreateproblems.com, hyring.com, dev.to vivekk101, a Medium skphd post; search snippets only, not opened; the Devinterview-io/mlops-interview-questions GitHub page WAS opened and has no dedicated monitoring or drift question, only monitoring bullets inside Q1, Q2, Q4, Q6, Q7 and Q12); editorial question lists, not verified candidate reports; MLOps, ML platform and ML engineer roles at IT-services firms, product companies and GCCs | Label-delay and estimation sources (NannyML blog 'machine learning monitoring workflow' on delayed or absent targets, CBPE and DLE, and warning that drift alerts alone can flood a team; arXiv 'Monitoring Machine Learning Systems: A Multivocal Literature Review' 2509.14294; arXiv 2403.16795 interview study 'We have no idea how models will behave in production until production' reporting alert fatigue from false positives; search snippets only, not opened); vendor blog and academic papers, not interview reports; ML engineer and MLOps roles
**Say this first (1 line):** If the scores are calibrated, each score is the chance the prediction is right, so I can add those chances up to get expected accuracy and precision with no labels; it holds under covariate shift, and it breaks under concept drift or miscalibration, so I use it as an early estimate and then confirm with real labels.

**Then explain:**
- **The idea:** a calibrated score of 0.8 means 8 in 10 such cases are positive. So for every row you know the expected true positive, false positive, false negative and true negative. Sum them over a batch, then read off accuracy, precision, recall.
- **Where it works:** covariate shift. The inputs change (new customer mix), scores move, but `P(y | x)` is the same, so the calibration still holds and the estimate tracks the truth.
- **Where it fails:** concept drift (the link from inputs to outcome changed, scores stay confident but wrong) and a model that was never calibrated. The estimate then stays flat and happily wrong. Calibration is a claim about the past; the method assumes it still holds.
- **NannyML CBPE:** this is the same family as NannyML's confidence-based performance estimation. I only describe the idea here, I do not reproduce its internals; check current docs for what the library adds (for example the calibration step).
- **Limits:** needs a threshold, needs a calibrated model checked on recent labelled data, and gives an estimate with noise at small batch sizes. It is blind to the very thing (concept drift) that hurts most. Keep a label-based metric when labels mature.

**Example:** Four predictions with scores 0.9, 0.8, 0.6, 0.3 and threshold 0.5. Predicted positive: 0.9, 0.8, 0.6. Expected TP = 0.9+0.8+0.6 = 2.3, expected FP = 0.1+0.2+0.4 = 0.7. The 0.3 row is predicted negative: expected FN = 0.3, expected TN = 0.7. Accuracy = (2.3+0.7)/4 = 0.75. Precision = 2.3/3 = 0.767. In the run below the same formulas are applied to 200,000 simulated rows.

**Code:**
Python (python3 -I in a venv with numpy, scipy, pandas, scikit-learn, PyYAML as needed):
```python
import numpy as np

def expected_metrics(scores, threshold=0.5):
    """Expected accuracy/precision/recall from calibrated P(y=1) scores. No labels used."""
    s = np.asarray(scores, dtype=float)
    pred = s >= threshold
    tp = s[pred].sum()            # expected true positives
    fp = (1 - s[pred]).sum()      # expected false positives
    fn = s[~pred].sum()           # expected false negatives
    tn = (1 - s[~pred]).sum()
    n = len(s)
    return {"acc": (tp + tn) / n,
            "precision": tp / (tp + fp) if tp + fp else float("nan"),
            "recall": tp / (tp + fn) if tp + fn else float("nan")}

def true_metrics(scores, y, threshold=0.5):
    pred = np.asarray(scores) >= threshold
    y = np.asarray(y)
    return {"acc": (pred == y).mean(),
            "precision": y[pred].mean(),
            "recall": pred[y == 1].mean()}

rng = np.random.default_rng(24)
N = 200_000

def world(name, scores, p_true):
    y = (rng.random(len(scores)) < p_true).astype(int)
    e, t = expected_metrics(scores), true_metrics(scores, y)
    print(f"{name:34s} est acc {e['acc']:.3f} true acc {t['acc']:.3f} | est prec {e['precision']:.3f} true prec {t['precision']:.3f}")

# A: reference world. Scores are calibrated: P(y=1 | score) = score.
s_ref = rng.beta(2, 3, N)
world("A calibrated, reference", s_ref, s_ref)
# B: covariate shift. Input mix changes, scores move up, but P(y|x) is unchanged, so calibration still holds.
s_cov = rng.beta(3, 2, N)
world("B covariate shift, calibration holds", s_cov, s_cov)
# C: concept drift. Same inputs and scores, but the real link between score and outcome weakens.
p_c = 0.5 + 0.4 * (s_ref - 0.5)
world("C concept drift (link weakened)", s_ref, p_c)
# D: miscalibrated from day one: model overconfident (true P is pulled toward 0.5).
world("D overconfident model", s_ref, 0.5 + 0.6 * (s_ref - 0.5))
```

**Output (my run):** (real run, Python 3.13, numpy 2.5.4, seed 24; no labels are used for the estimate, labels are only simulated to get the truth)
```text
A calibrated, reference            est acc 0.687 true acc 0.688 | est prec 0.640 true prec 0.642
B covariate shift, calibration holds est acc 0.688 true acc 0.688 | est prec 0.709 true prec 0.709
C concept drift (link weakened)    est acc 0.687 true acc 0.576 | est prec 0.640 true prec 0.561
D overconfident model              est acc 0.687 true acc 0.612 | est prec 0.640 true prec 0.584
```

**Follow-ups:**
- **What if the model is not calibrated?** Calibrate first (isotonic or Platt on a recent labelled set), then check the reliability curve. Without that, the estimate is not meaningful.
- **Can you detect that concept drift happened?** Not from this estimate. Use the label-based metric when labels mature, a canary label sample (Q25), or watch for a gap between estimated and observed performance.

**Common mistakes:**
- Trusting the estimate on a model that was never calibrated.
- Using it as proof that nothing is wrong. It cannot see concept drift.
- Using one threshold in the estimate and a different one in production.
- Reporting a point estimate from a few hundred rows without an interval.

### Q25 ⭐⭐ 🟡 Canary labels and label budgets. When true labels are expensive (human review, field checks), how do you sample for a performance estimate: random versus stratified versus score-weighted sampling, how many labels for a given confidence interval, and how to reweight. Compute the sample size needed for a 3-point margin on precision at 90 percent, run a stratified sample on simulated scores with inverse-probability weights, and compare the estimate and its interval with the full-label truth.
**Asked at:** MLOps interview question banks and guides (K21Academy '47 MLOps interview questions' PDF, Towards AI '101 ML LLM agentic AIOps interview questions', DataCamp MLOps interview questions, The Interview Guys MLOps post, wecreateproblems.com, hyring.com, dev.to vivekk101, a Medium skphd post; search snippets only, not opened; the Devinterview-io/mlops-interview-questions GitHub page WAS opened and has no dedicated monitoring or drift question, only monitoring bullets inside Q1, Q2, Q4, Q6, Q7 and Q12); editorial question lists, not verified candidate reports; MLOps, ML platform and ML engineer roles at IT-services firms, product companies and GCCs | Label-delay and estimation sources (NannyML blog 'machine learning monitoring workflow' on delayed or absent targets, CBPE and DLE, and warning that drift alerts alone can flood a team; arXiv 'Monitoring Machine Learning Systems: A Multivocal Literature Review' 2509.14294; arXiv 2403.16795 interview study 'We have no idea how models will behave in production until production' reporting alert fatigue from false positives; search snippets only, not opened); vendor blog and academic papers, not interview reports; ML engineer and MLOps roles
**Say this first (1 line):** Labels cost money, so I label a sample, not everything: stratify by score, give each case an inverse-probability weight, and size the sample from the margin I want, which for plus or minus 3 points on precision is a few hundred labels, not thousands.

**Then explain:**
- **Sampling choices:** random is simple and unbiased. Stratified by score gives lower variance and lets you put more labels where the model is least sure. Score-weighted (for example only labelling the highest scores) is cheap but biased unless you reweight.
- **Sample size:** `n = z^2 * p(1-p) / margin^2`. If you do not know `p`, use 0.5 for the worst case. If you expect precision near 0.9, you need far fewer labels.
- **Reweighting:** if a case had sampling probability `pi`, count it with weight `1/pi`. Stratified estimate is `sum(N_h * p_h) / N`. Interval uses the within-stratum variance.
- **Failure modes:** labelling only easy or convenient cases and not reweighting; reviewers who see the model score and agree with it; sample too small per stratum (one or two labels give no variance); forgetting that "90 percent" can mean the confidence level or the expected precision, so state which.
- **Scope:** this is about precision of flagged cases. Recall needs labels from the unflagged cases too, which is usually the expensive part.

**Example:** Hand check of the formula: 90% confidence, margin 0.03, expected precision 0.9. z = 1.645, so n = 2.706 x 0.09 / 0.0009 = 270.6, round up to 271. With the worst case p = 0.5 it is 752. Weighting example: 1,000 cases in a low stratum with 80% correct and 9,000 in a high stratum with 95% correct. Estimate = 0.1 x 0.80 + 0.9 x 0.95 = 0.935, not the simple mean of the two samples.

**Code:**
Python (python3 -I in a venv with numpy, scipy, pandas, scikit-learn, PyYAML as needed):
```python
import math
import numpy as np
from scipy.stats import norm

# 1. sample size for a +/-3 point margin on a proportion (normal approximation)
def n_needed(p, margin, conf):
    z = norm.ppf(0.5 + conf / 2)
    return math.ceil(z * z * p * (1 - p) / margin ** 2)
for conf in (0.90, 0.95):
    print(f"conf {conf:.2f}: p=0.90 -> n={n_needed(0.90, 0.03, conf)}   worst case p=0.50 -> n={n_needed(0.5, 0.03, conf)}")

# 2. simulated population of flagged cases (score >= 0.5 means 'flag'); true label ~ Bernoulli(p_true)
rng = np.random.default_rng(25)
N = 50_000
score = np.clip(rng.beta(5, 1.2, N) * 0.5 + 0.5, 0.5, 1.0)       # flagged cases only
p_true = np.clip(0.55 + 0.9 * (score - 0.5), 0, 0.99)           # real precision rises with score
y = (rng.random(N) < p_true).astype(int)
truth = y.mean()
print(f"flagged N={N}, full-label precision = {truth:.4f}")

bins = np.array([0.5, 0.7, 0.85, 0.95, 1.0001])
stratum = np.digitize(score, bins) - 1
Nh = np.bincount(stratum)
print("stratum sizes", Nh.tolist())

def srs(n, r):
    idx = r.choice(N, n, replace=False)
    p = y[idx].mean(); se = math.sqrt(p * (1 - p) / n * (1 - n / N))
    return p, se

def strat(nh, r):
    # inverse-probability weight = Nh / nh ; estimate = sum(Nh * ph) / N
    est, var = 0.0, 0.0
    for h, k in enumerate(nh):
        idx = r.choice(np.flatnonzero(stratum == h), k, replace=False)
        ph = y[idx].mean(); w = Nh[h] / N
        est += w * ph
        var += w * w * (1 - k / Nh[h]) * ph * (1 - ph) / (k - 1)
    return est, math.sqrt(var)

budget = 600
prop = np.maximum(10, np.round(budget * Nh / N)).astype(int)        # proportional allocation
# score-weighted: more labels where the label is least certain (low-score strata), Neyman-like using a pilot guess of p
pilot = np.array([0.6, 0.75, 0.9, 0.97])
neyman = Nh * np.sqrt(pilot * (1 - pilot)); neyman = np.maximum(10, np.round(budget * neyman / neyman.sum())).astype(int)
print("proportional alloc", prop.tolist(), " neyman-like alloc", neyman.tolist())

z = norm.ppf(0.975)
r = np.random.default_rng(250)
for name, f in (("simple random", lambda: srs(budget, r)), ("stratified proportional", lambda: strat(prop, r)), ("stratified neyman-like", lambda: strat(neyman, r))):
    est, se = f()
    print(f"{name:24s} est {est:.4f}  95% CI [{est - z * se:.4f}, {est + z * se:.4f}]  covers truth: {est - z * se <= truth <= est + z * se}")

# 3. repeat 1000 times: bias, spread, coverage
res = {k: [] for k in ("srs", "prop", "neyman")}
r2 = np.random.default_rng(251)
cov = dict.fromkeys(res, 0)
for _ in range(1000):
    for k, f in (("srs", lambda: srs(budget, r2)), ("prop", lambda: strat(prop, r2)), ("neyman", lambda: strat(neyman, r2))):
        e, se = f(); res[k].append(e); cov[k] += (abs(e - truth) <= z * se)
for k in res:
    a = np.array(res[k]); print(f"{k:7s} mean {a.mean():.4f} sd {a.std():.4f} coverage {cov[k]/1000:.3f}")

# 4. WRONG: label only the stratum that is cheapest (the top scores) and do not reweight
top = np.flatnonzero(stratum == 3)
print(f"biased (top stratum only): {y[top].mean():.4f}  vs truth {truth:.4f}")
```

**Output (my run):** (real run, numpy 2.5.4, scipy 1.18.1, seeds 25, 250, 251; labels for the whole population are simulated so we know the truth)
```text
conf 0.90: p=0.90 -> n=271   worst case p=0.50 -> n=752
conf 0.95: p=0.90 -> n=385   worst case p=0.50 -> n=1068
flagged N=50000, full-label precision = 0.9124
stratum sizes [727, 10157, 22816, 16300]
proportional alloc [10, 122, 274, 196]  neyman-like alloc [15, 184, 286, 116]
simple random            est 0.9150  95% CI [0.8928, 0.9372]  covers truth: True
stratified proportional  est 0.9274  95% CI [0.9072, 0.9476]  covers truth: True
stratified neyman-like   est 0.9013  95% CI [0.8781, 0.9245]  covers truth: True
srs     mean 0.9129 sd 0.0118 coverage 0.938
prop    mean 0.9126 sd 0.0112 coverage 0.943
neyman  mean 0.9125 sd 0.0106 coverage 0.948
biased (top stratum only): 0.9747  vs truth 0.9124
```

**Follow-ups:**
- **Why oversample low scores?** That is where the label is least predictable, so variance is highest. A Neyman-like allocation puts more labels there, and the weights fix the bias.
- **Can I label only the top scores?** You get a cheap number that is wrong (0.9747 vs 0.9124 above). Weights only help if every stratum has a non-zero chance of being sampled.

**Common mistakes:**
- Sizing the sample with the wrong meaning of "90 percent".
- Not weighting a deliberately skewed sample.
- Giving reviewers the model score, so labels copy the model.
- Reporting a number without an interval.

### Q26 ⭐⭐ 🟡 SLOs and SLIs for an ML service. Map the SRE ideas to ML: availability and latency SLIs (owned by Part 6), then ML-specific SLIs such as data validity rate, feature freshness, share of predictions with a drifted-input flag, matured-label metric, and model age. Explain error budgets and burn-rate alerting from the SRE workbook and where it does and does not fit slow labels. Implement an SLI window calculator and a two-window burn-rate check, run on simulated hourly good/bad counts, and state that the ML SLIs are an extension, not a standard.
**Asked at:** Alerting and SLO sources (Google SRE Workbook chapter 'Alerting on SLOs' on burn-rate and multiwindow alerts, Datadog burn-rate docs, openobserve alert-fatigue post; search snippets only, not opened, sre.google WebFetch failed with getaddrinfo ENOTFOUND); SRE docs, not ML-specific and not interview reports; MLOps, SRE and platform roles; no source found on SLOs defined for ML models, so the ML mapping is an expert extension
**Say this first (1 line):** An SLI is a measured good-over-total ratio, an SLO is the target, the error budget is what is left, and I alert when the budget burns fast in both a long and a short window; for ML I add data-quality SLIs, which is my extension of the SRE idea, not a standard.

**Then explain:**
- **Plain SRE part:** SLI = good events / all events over a window. SLO = target, say 99 percent. Error budget = 1 minus the SLO. Burn rate = (actual bad share) / (allowed bad share). Burn 1 means you spend the budget exactly at the pace allowed. Availability and latency SLIs are Part 6.
- **ML-specific SLIs (extension, not a standard):** data validity rate (rows passing checks), feature freshness, share of predictions with a drifted-input flag, matured-label metric (accuracy on labels that have arrived), model age.
- **Two windows:** page only when a long window shows real budget loss and a short window shows it is still happening. That avoids paging on a blip and avoids paging after the problem is already fixed. The SRE Workbook chapter on alerting on SLOs describes multiwindow, multi-burn-rate alerts; check it for the thresholds, the ones below are illustrative.
- **Where it does not fit:** slow labels. A label-based SLI is days late, so a burn rate on it is a ticket signal, not a page. Use fast proxy SLIs (data validity, null rate, score distribution) for paging.
- **Failure modes:** a window shorter than the data cadence (hourly counts and a 5 minute window); SLO set with no owner; too many SLOs.

**Example:** SLO 99 percent, so budget is 1 percent. In hour 34 the bad share is 8.6 percent, so the 1 hour burn is 8.6 / 1 = 8.6. The 6 hour window covers hours 29 to 34: bad shares 0.6, 7.9, 7.9, 8.2, 8.0, 8.6 average to about 6.9, so burn 6.9. Both are at or above 6 (my illustrative threshold), so the two-window rule fires at hour 34. At hour 38 the feed is fixed: 1 hour burn drops to 0.3, so the two-window rule stops while the long window alone would still fire.

**Code:**
Python (python3 -I in a venv with numpy, scipy, pandas, scikit-learn, PyYAML as needed):
```python
import numpy as np

SLO = 0.99                       # SLI: share of hourly requests whose feature rows pass validation
BUDGET = 1 - SLO                 # allowed bad share = 1 %

def sli(good, bad, end, hours):
    """SLI over the last `hours` hours ending at index `end` (inclusive)."""
    lo = max(0, end - hours + 1)
    g, b = good[lo:end + 1].sum(), bad[lo:end + 1].sum()
    return g / (g + b)

def burn(good, bad, end, hours):
    return (1 - sli(good, bad, end, hours)) / BUDGET     # 1.0 = spending budget exactly at the allowed pace

rng = np.random.default_rng(26)
H = 72
total = rng.integers(900, 1100, H)
bad_rate = np.full(H, 0.004)
bad_rate[30:38] = 0.08           # upstream bug: 8 bad hours, then fixed
bad = rng.binomial(total, bad_rate); good = total - bad

LONG, SHORT, THRESH = 6, 1, 6.0  # illustrative; pick thresholds from your own budget maths
print("hour  bad%  burn1h burn6h  single(6h>=6)  two-window(6h&1h>=6)")
fired_single, fired_two = [], []
for h in range(H):
    b1, b6 = burn(good, bad, h, SHORT), burn(good, bad, h, LONG)
    s = b6 >= THRESH
    t = b6 >= THRESH and b1 >= THRESH
    fired_single.append(s); fired_two.append(t)
    if 28 <= h <= 46 and (h % 1 == 0):
        print(f"{h:4d} {100*bad[h]/total[h]:5.1f} {b1:7.1f} {b6:6.1f}  {str(s):13s}  {t}")
print("single-window alert hours:", [h for h, v in enumerate(fired_single) if v])
print("two-window alert hours   :", [h for h, v in enumerate(fired_two) if v])
print(f"whole-window check: bad share over all {H}h = {bad.sum()/total.sum():.4f}, budget {BUDGET:.4f}, budget used = {bad.sum()/total.sum()/BUDGET:.0%}")
```

**Output (my run):** (real run, numpy 2.5.4, seed 26; hourly counts are simulated: a data bug from hour 30 to 37)
```text
hour  bad%  burn1h burn6h  single(6h>=6)  two-window(6h&1h>=6)
  28   0.3     0.3    0.4  False          False
  29   0.6     0.6    0.4  False          False
  30   7.9     7.9    1.7  False          False
  31   7.9     7.9    3.0  False          False
  32   8.2     8.2    4.3  False          False
  33   8.0     8.0    5.5  False          False
  34   8.6     8.6    6.9  True           True
  35   7.5     7.5    8.0  True           True
  36   7.3     7.3    7.9  True           True
  37   8.2     8.2    8.0  True           True
  38   0.3     0.3    6.7  True           False
  39   0.6     0.6    5.4  False          False
  40   0.3     0.3    3.9  False          False
  41   0.4     0.4    2.8  False          False
  42   0.3     0.3    1.6  False          False
  43   0.3     0.3    0.4  False          False
  44   0.6     0.6    0.4  False          False
  45   0.9     0.9    0.4  False          False
  46   0.6     0.6    0.5  False          False
single-window alert hours: [34, 35, 36, 37, 38]
two-window alert hours   : [34, 35, 36, 37]
whole-window check: bad share over all 72h = 0.0123, budget 0.0100, budget used = 123%
```

**Follow-ups:**
- **Why not alert on the SLO itself?** It reacts too late and too slowly. Burn rate tells you how fast you are heading to a miss.
- **What window do I use for labels?** Do not page on label metrics. Use a ticket on the matured window and keep the paging SLIs on fast signals.

**Common mistakes:**
- Presenting ML SLIs as if there is a standard.
- Paging on a single long window, which keeps firing after recovery.
- Using thresholds copied from a blog without checking your own budget maths.
- Counting bad rows without counting traffic, so quiet hours look worse.

### Q27 ⭐⭐ 🟡 Runbooks, ownership and on-call for model alerts. Who gets paged (platform, data engineering, data science), what a good runbook contains (what the alert means, how to confirm, dashboards, safe first actions such as fall back to the previous model or a rule, escalation, how to close), and how you stop alerts nobody owns. Write an alert catalogue in YAML with owner, severity, runbook link and action, validate that every alert has all fields, run the validator, and show an Alertmanager routing tree for it (not executed).
**Asked at:** Alerting and SLO sources (Google SRE Workbook chapter 'Alerting on SLOs' on burn-rate and multiwindow alerts, Datadog burn-rate docs, openobserve alert-fatigue post; search snippets only, not opened, sre.google WebFetch failed with getaddrinfo ENOTFOUND); SRE docs, not ML-specific and not interview reports; MLOps, SRE and platform roles; no source found on SLOs defined for ML models, so the ML mapping is an expert extension | Prometheus and Grafana monitoring mentions (K21Academy and Towards AI question lists naming Prometheus, Grafana and Evidently for drift and accuracy dashboards; Devinterview-io page opened, Q12 mentions inference monitoring with Grafana and Prometheus; search snippets otherwise); question lists, not verified reports; MLOps and platform roles; Prometheus, Grafana and Alertmanager servers were not available in this sandbox
**Say this first (1 line):** Every alert gets one owner, a severity, a runbook link and a first safe action, I check that with a script so an alert without those cannot merge, and Alertmanager routes by those labels so the right team gets it.

**Then explain:**
- **Who is paged:** by cause, not by model. Broken feed or null spike: data engineering. Drift or score-shape change: data science. Stale model or failed retrain job: ML platform. Anything user-visible and urgent goes to whoever is on call for the service, then they hand over.
- **A runbook has:** what the alert means, how to confirm (which dashboard, which query), safe first actions (fall back to the previous model or a rule, pause automatic decisions), who to escalate to, and how to close it (what has to be true, what to write down).
- **Orphan alerts:** keep the catalogue in git, check it in CI (every alert has owner, severity, runbook, action; owner must be a real team), and review alerts that nobody acted on every quarter. An alert with no owner gets deleted or fixed.
- **Alertmanager routing:** group by alert name and model, route by `owner` and `severity` labels, keep a default receiver so nothing is dropped. Shown below, but Alertmanager was not run here.
- **Failure modes:** owner is a person who left; runbook link is dead; "page" severity with no clear action; routing tree that sends two teams the same alert.

**Example:** `FeatureNullRateHigh` has owner `data-engineering`, severity `page`. The route matches severity=page and owner=data-engineering, so it reaches `data-eng-pager`. `ModelStale` is a ticket owned by `ml-platform`; no child route matches it, so it falls through to the default receiver `ml-platform-ticket`. The first draft of the catalogue had one alert with no action, and the validator caught it; the version below is the fixed one.

**Code:**
YAML:
```yaml
# ===== catalogue.yaml =====
alerts:
  - name: FeatureNullRateHigh
    owner: data-engineering
    severity: page
    runbook: https://wiki.example.com/runbooks/feature-null-rate
    action: "Check the upstream feed job; if the feed is broken, switch the model to the fallback rule."
  - name: DriftScoreSustained
    owner: data-science
    severity: ticket
    runbook: https://wiki.example.com/runbooks/drift-sustained
    action: "Confirm on the dashboard, compare with a known campaign or seasonal event, open a retrain review."
  - name: LabelJoinLagHigh
    owner: data-engineering
    severity: ticket
    runbook: https://wiki.example.com/runbooks/label-lag
    action: "Check the label pipeline; matured-label metrics are stale until it is fixed."
  - name: ModelStale
    owner: ml-platform
    severity: ticket
    runbook: https://wiki.example.com/runbooks/model-stale
    action: "Check the last retrain run; trigger it by hand if the scheduler skipped it."
  - name: ScoreDistributionShift
    owner: data-science
    severity: page
    runbook: https://wiki.example.com/runbooks/score-shift
    action: "Compare the score histogram with the reference; if the shape moved, fall back to the previous model."

# ===== alertmanager.yml =====
route:
  receiver: ml-platform-ticket
  group_by: [alertname, model]
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  routes:
    - matchers: ['severity="page"', 'owner="data-engineering"']
      receiver: data-eng-pager
    - matchers: ['severity="page"', 'owner="data-science"']
      receiver: data-science-pager
    - matchers: ['owner="data-engineering"']
      receiver: data-eng-ticket
    - matchers: ['owner="data-science"']
      receiver: data-science-ticket
inhibit_rules:
  - source_matchers: ['alertname="UpstreamFeedDown"']
    target_matchers: ['alertname=~"DriftScoreSustained|FeatureNullRateHigh|ScoreDistributionShift"']
    equal: [model]
receivers:
  - name: ml-platform-ticket
  - name: data-eng-pager
  - name: data-science-pager
  - name: data-eng-ticket
  - name: data-science-ticket
```

Python (python3 -I in a venv with numpy, scipy, pandas, scikit-learn, PyYAML as needed):
```python
# ===== validate_catalogue.py =====
import sys, yaml, re
REQUIRED = ("name", "owner", "severity", "runbook", "action")
OWNERS = {"data-engineering", "data-science", "ml-platform"}
SEVERITIES = {"page", "ticket"}

def validate(doc):
    errors, seen = [], set()
    for i, a in enumerate(doc.get("alerts", [])):
        tag = a.get("name", f"#{i}")
        for k in REQUIRED:
            if not a.get(k):
                errors.append(f"{tag}: missing or empty '{k}'")
        if a.get("name") in seen:
            errors.append(f"{tag}: duplicate name")
        seen.add(a.get("name"))
        if a.get("owner") and a["owner"] not in OWNERS:
            errors.append(f"{tag}: owner '{a['owner']}' is not a known team")
        if a.get("severity") and a["severity"] not in SEVERITIES:
            errors.append(f"{tag}: severity must be one of {sorted(SEVERITIES)}")
        if a.get("runbook") and not re.match(r"https://", a["runbook"]):
            errors.append(f"{tag}: runbook must be an https link")
        if a.get("severity") == "page" and a.get("action") and len(a["action"].split()) < 5:
            errors.append(f"{tag}: a paging alert needs a real first action")
    return errors

for path in sys.argv[1:]:
    doc = yaml.safe_load(open(path))
    errs = validate(doc)
    print(f"{path}: {len(doc['alerts'])} alerts, {'OK' if not errs else str(len(errs)) + ' error(s)'}")
    for e in errs:
        print("  -", e)

# ===== check_routing.py =====
import yaml
am = yaml.safe_load(open("alertmanager.yml"))
cat = yaml.safe_load(open("catalogue.yaml"))["alerts"]
receivers = {r["name"] for r in am["receivers"]}
def walk(route):
    yield route
    for r in route.get("routes", []):
        yield from walk(r)
used = {r["receiver"] for r in walk(am["route"]) if "receiver" in r}
print("receivers defined but unused:", sorted(receivers - used) or "none")
print("routes pointing to unknown receiver:", sorted(used - receivers) or "none")
# which receiver would each catalogue entry reach? (simplified first-match on owner and severity)
def pick(a):
    for r in am["route"]["routes"]:
        want = dict(m.replace('"', '').split("=", 1) for m in r["matchers"])
        if all(a.get(k) == v for k, v in want.items()):
            return r["receiver"]
    return am["route"]["receiver"]
for a in cat:
    print(f"{a['name']:24s} -> {pick(a)}")
```

**Output (my run):** not executed: Alertmanager was not available in this sandbox and the receivers have no real integrations. What did run: the Python validator on the catalogue (a good file and a deliberately bad file) and a script that parses `alertmanager.yml` with PyYAML 6.0.3 and checks that every route points to a defined receiver (python3 -I).
```text
catalogue.yaml: 5 alerts, OK
catalogue_bad.yaml: 2 alerts, 4 error(s)
  - DriftScoreSustained: owner 'nobody' is not a known team
  - DriftScoreSustained: severity must be one of ['page', 'ticket']
  - DriftScoreSustained: runbook must be an https link
  - ModelStale: missing or empty 'action'
receivers defined but unused: none
routes pointing to unknown receiver: none
FeatureNullRateHigh      -> data-eng-pager
DriftScoreSustained      -> data-science-ticket
LabelJoinLagHigh         -> data-eng-ticket
ModelStale               -> ml-platform-ticket
ScoreDistributionShift   -> data-science-pager
```

**Follow-ups:**
- **How do you stop alert sprawl?** Each alert needs an owner and an action, review which alerts led to action, delete or demote the rest.
- **Who owns a drift alert when the cause is upstream?** Data science confirms and routes to the upstream owner; the runbook says so.

**Common mistakes:**
- A runbook that says "investigate".
- Paging for things that can wait until morning.
- Routing everything to one shared channel.
- Never testing the route (send a test alert after each change).

### Q28 ⭐⭐ 🟡 Fairness monitoring in production. Explain which group metrics you can monitor without labels (selection rate, score distribution per group) and which need labels (TPR and FPR gaps, calibration by group), small-group noise and confidence intervals, and the Indian context where sensitive attributes may be unavailable or restricted so proxies and audits are used, hedged. Compute selection-rate ratio and equal-opportunity gap per window with pandas on simulated data, add Wilson intervals, and show an alert rule that avoids firing on tiny groups. Check current guidance before citing any rule.
**Asked at:** MLOps interview question banks and guides (K21Academy '47 MLOps interview questions' PDF, Towards AI '101 ML LLM agentic AIOps interview questions', DataCamp MLOps interview questions, The Interview Guys MLOps post, wecreateproblems.com, hyring.com, dev.to vivekk101, a Medium skphd post; search snippets only, not opened; the Devinterview-io/mlops-interview-questions GitHub page WAS opened and has no dedicated monitoring or drift question, only monitoring bullets inside Q1, Q2, Q4, Q6, Q7 and Q12); editorial question lists, not verified candidate reports; MLOps, ML platform and ML engineer roles at IT-services firms, product companies and GCCs | Expert extension: no source found for the exact question; the topic follows from the library behaviour tested in this sandbox and from general monitoring practice, and Wave B must verify against current docs; MLOps, ML platform and ML engineer roles, including IT-services firms, product companies and GCCs
**Say this first (1 line):** Without labels I watch selection rate and score distribution per group; with labels I add the true positive rate gap and calibration by group; I always attach an interval and a minimum group size, so a tiny group does not page anyone.

**Then explain:**
- **No labels needed:** selection rate (share approved or flagged) per group, the selection-rate ratio against a reference group, score distribution per group. These can move for legitimate reasons, so they are a signal, not a verdict.
- **Labels needed:** TPR and FPR gap by group (equal opportunity looks at the TPR gap), calibration by group. These arrive late, so they are a slower check.
- **Small groups:** a group of 100 gives a wide interval. A Wilson interval for the rate shows how wide. Alert only when the group has a minimum count and even the favourable end of the interval breaks the rule. For tiny groups, pool over longer windows.
- **Indian context (hedged, check current guidance):** sensitive attributes such as caste or religion may not be collected or may not be allowed to be used, so teams use proxies (region, language, device tier) and offline audits on a consented sample. Do not quote a legal rule from memory; check current guidance and counsel.
- **Failure modes:** the 0.8 ratio is a US-origin rule of thumb (four-fifths), not Indian law; proxies can be wrong; alerting per group per hour multiplies false alarms.

**Example:** Week 2, group C has 108 decisions and selection 0.278 against the reference 0.362: ratio 0.77, below 0.8. The naive rule fires. The Wilson interval is [0.20, 0.37], so the data are also consistent with parity; and n < 200, so the guarded rule stays quiet. In weeks 3 and 4, group B (over 1,000 rows) has ratio 0.37 and 0.44 and an interval that is clearly below, so the guarded rule fires. That is the injected problem.

**Code:**
Python (python3 -I in a venv with numpy, scipy, pandas, scikit-learn, PyYAML as needed):
```python
import numpy as np, pandas as pd

rng = np.random.default_rng(28)
GROUPS = {"A": 0.70, "B": 0.27, "C": 0.03}          # traffic share; C is tiny
rows = []
for w in range(1, 5):                                 # four weekly windows, 4000 decisions each
    n = 4000
    g = rng.choice(list(GROUPS), n, p=list(GROUPS.values()))
    skill = rng.normal(0, 1, n)
    y = (rng.random(n) < 1 / (1 + np.exp(-(skill - 0.3)))).astype(int)      # true outcome
    score = skill + rng.normal(0, 0.7, n)
    penalty = np.where((g == "B") & (w >= 3), 0.9, 0.0)                       # from week 3 the model under-scores group B
    approve = ((score - penalty) > 0.4).astype(int)
    rows.append(pd.DataFrame({"week": w, "group": g, "approve": approve, "y": y}))
df = pd.concat(rows, ignore_index=True)

def wilson(k, n, z=1.96):
    if n == 0: return (np.nan, np.nan)
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h

REF, MIN_N, RATIO = "A", 200, 0.8
out = []
for w, d in df.groupby("week"):
    ref = d[d.group == REF]
    ref_sel = ref.approve.mean()
    ref_pos = ref[ref.y == 1]; ref_tpr = ref_pos.approve.mean()
    for g, x in d.groupby("group"):
        sel = x.approve.mean(); lo, hi = wilson(x.approve.sum(), len(x))
        pos = x[x.y == 1]; tpr = pos.approve.mean()
        naive = sel / ref_sel < RATIO
        # alert only if the group is big enough AND even the upper end of its interval is below the ratio line
        guarded = len(x) >= MIN_N and (hi / ref_sel < RATIO)
        out.append(dict(week=w, group=g, n=len(x), sel=round(sel, 3), ci=f"[{lo:.2f},{hi:.2f}]",
                        ratio=round(sel / ref_sel, 2), tpr_gap=round(tpr - ref_tpr, 3), naive_alert=naive, guarded_alert=guarded))
res = pd.DataFrame(out)
print(res.to_string(index=False))
print("\nweeks where naive rule fired for C (tiny group):", res[(res.group == "C") & res.naive_alert].week.tolist())
print("weeks where guarded rule fired:", res[res.guarded_alert][["week", "group"]].values.tolist())
```

**Output (my run):** (real run, pandas 3.1.0, numpy 2.5.4, seed 28; outcomes and a drop in group B's scores from week 3 are simulated)
```text
 week group    n   sel          ci  ratio  tpr_gap  naive_alert  guarded_alert
    1     A 2763 0.381 [0.36,0.40]   1.00    0.000        False          False
    1     B 1115 0.379 [0.35,0.41]   0.99    0.009        False          False
    1     C  122 0.361 [0.28,0.45]   0.95   -0.024        False          False
    2     A 2831 0.362 [0.34,0.38]   1.00    0.000        False          False
    2     B 1061 0.368 [0.34,0.40]   1.02    0.027        False          False
    2     C  108 0.278 [0.20,0.37]   0.77   -0.173         True          False
    3     A 2801 0.371 [0.35,0.39]   1.00    0.000        False          False
    3     B 1092 0.136 [0.12,0.16]   0.37   -0.293         True           True
    3     C  107 0.374 [0.29,0.47]   1.01   -0.081        False          False
    4     A 2748 0.377 [0.36,0.39]   1.00    0.000        False          False
    4     B 1137 0.165 [0.14,0.19]   0.44   -0.263         True           True
    4     C  115 0.391 [0.31,0.48]   1.04   -0.030        False          False

weeks where naive rule fired for C (tiny group): [2]
weeks where guarded rule fired: [[3, 'B'], [4, 'B']]
```

**Follow-ups:**
- **What if C is really being harmed?** The guard hides it in a single week. Pool several weeks for small groups, and do a periodic offline audit.
- **Is a ratio under 0.8 a violation?** No. It is a convention to start an investigation. Check current guidance for your market.

**Common mistakes:**
- Alerting on a small-group rate with no interval.
- Treating selection-rate gaps as proof of bias, or as proof of none.
- Reporting group metrics only at training time.
- Using a sensitive proxy without a review of what it encodes.

### Q29 ⭐⭐ 🟡 Privacy and prediction logging. Cover what may be personal data in features and predictions, minimisation, masking or salted hashing of identifiers, retention limits, access control, deletion requests, and the tension between audit and minimisation. Implement a logging function that redacts email and phone patterns, hashes the customer id with a salt, drops fields not in an allow-list, run it on sample records, and say what it does not protect. Check the current text of India's DPDP Act and Rules, GDPR and sector rules rather than quoting from memory.
**Asked at:** Prediction-logging and privacy sources (apxml.com ML audit trails, gravitee.io PII redaction and retention, scalevise.com audit-ready logging, regolo.ai and mljar prompt pages; search snippets only, not opened; nothing found on India's DPDP Act for prediction logs, and retention figures in the snippets are vendor suggestions, not legal limits); vendor and practitioner posts, not interview reports; ML platform, security and data governance roles
**Say this first (1 line):** Log only what I need, from an allow-list, redact patterns in free text, replace the customer id with a keyed hash, set a retention limit, and be honest that none of this makes the data anonymous.

**Then explain:**
- **What can be personal data:** direct identifiers (name, email, phone, ID numbers), but also a customer id, device id, exact location, and sometimes a combination of ordinary features. Predictions about a person are personal data too.
- **Controls:** minimise (allow-list fields), mask or redact patterns in free text, pseudonymise ids with a keyed hash (HMAC) with the key in a secret manager, short retention, role-based access, a way to find and delete one person's records on request.
- **Audit vs minimisation:** audit wants enough to reproduce a decision (model version, inputs used, score, decision); minimisation wants less. Settle it with a written purpose, log the features the model used rather than the raw record, and keep access tight.
- **Legal text:** I have not quoted the India DPDP Act and Rules, GDPR or sector rules here. Check the current text and ask your privacy or legal team about retention and deletion duties.
- **What the code does not protect:** regexes miss formats; a keyed hash of a small id space can be reversed by anyone with the key; free text may hold names; combinations of fields can re-identify; it does nothing for backups or downstream copies.

**Example:** Record 1 has an email and phone in the note and a PAN number in a field that is not on the allow-list. After `safe_record`, the PAN field is gone, the note reads `caller [EMAIL] asked on [PHONE]`, and `C1001` becomes a 16-character id that is the same in every record for that customer, so you can still join and count per customer.

**Code:**
Python (python3 -I in a venv with numpy, scipy, pandas, scikit-learn, PyYAML as needed):
```python
import hashlib, hmac, json, re

SALT = b"demo-only-secret-load-from-a-secret-manager"       # never hard-code in real code
ALLOW = {"customer_id", "model_version", "score", "decision", "amount_band", "city_tier", "note", "ts"}
EMAIL = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
PHONE = re.compile(r"(?<!\d)(?:\+91[\s-]?)?[6-9]\d{4}[\s-]?\d{5}(?!\d)")   # Indian mobile style, rough

def pseudo(value):
    return hmac.new(SALT, str(value).encode(), hashlib.sha256).hexdigest()[:16]

def redact(text):
    return PHONE.sub("[PHONE]", EMAIL.sub("[EMAIL]", text))

def safe_record(rec):
    out = {}
    for k, v in rec.items():
        if k not in ALLOW:
            continue                                    # allow-list: unknown fields are dropped, not logged
        if k == "customer_id":
            out["customer_pseudo_id"] = pseudo(v)
        elif isinstance(v, str):
            out[k] = redact(v)
        else:
            out[k] = v
    return out

records = [
    {"customer_id": "C1001", "model_version": "v7", "score": 0.82, "decision": "review", "amount_band": "50-100k",
     "city_tier": 2, "ts": "2026-10-26T10:00:00Z", "email": "asha@example.com", "pan": "ABCDE1234F",
     "note": "caller asha.k@example.com asked on 98765 43210"},
    {"customer_id": "C1001", "model_version": "v7", "score": 0.31, "decision": "approve", "amount_band": "10-50k",
     "city_tier": 2, "ts": "2026-10-26T10:05:00Z", "full_name": "Asha K", "note": "alt +91-9123456789"},
    {"customer_id": "C2002", "model_version": "v7", "score": 0.55, "decision": "review", "amount_band": "10-50k",
     "city_tier": 3, "ts": "2026-10-26T10:07:00Z", "note": "no pii here"},
]
for r in records:
    print(json.dumps(safe_record(r), sort_keys=True))
same = safe_record(records[0])["customer_pseudo_id"] == safe_record(records[1])["customer_pseudo_id"]
print("same customer -> same pseudo id (joins still work):", same)
# the limit: a small id space can be brute-forced by anyone who has the salt
ids = [f"C{n}" for n in range(1000, 1100)]
target = safe_record(records[0])["customer_pseudo_id"]
print("brute force with salt recovers id:", [i for i in ids if pseudo(i) == target])
```

**Output (my run):** (real run, Python 3.13, standard library only; the salt in the file is a demo value)
```text
{"amount_band": "50-100k", "city_tier": 2, "customer_pseudo_id": "2efd8c92e7dfc971", "decision": "review", "model_version": "v7", "note": "caller [EMAIL] asked on [PHONE]", "score": 0.82, "ts": "2026-10-26T10:00:00Z"}
{"amount_band": "10-50k", "city_tier": 2, "customer_pseudo_id": "2efd8c92e7dfc971", "decision": "approve", "model_version": "v7", "note": "alt [PHONE]", "score": 0.31, "ts": "2026-10-26T10:05:00Z"}
{"amount_band": "10-50k", "city_tier": 3, "customer_pseudo_id": "1b17d2867daccc7b", "decision": "review", "model_version": "v7", "note": "no pii here", "score": 0.55, "ts": "2026-10-26T10:07:00Z"}
same customer -> same pseudo id (joins still work): True
brute force with salt recovers id: ['C1001']
```

**Follow-ups:**
- **Why HMAC and not a plain hash?** A plain hash of a guessable id can be reversed by trying all ids. A keyed hash needs the key, but is still pseudonymous, not anonymous.
- **How do you handle a deletion request?** Keep an index from the pseudonymous id to storage locations, or store logs partitioned so one person's records can be found, and delete or tombstone them.

**Common mistakes:**
- Logging the full request body "for debugging".
- Hard-coding the salt in the repo.
- Calling hashed data anonymous.
- Keeping logs forever because storage is cheap.

### Q30 ⭐⭐ 🔴 Prometheus alerting rules and Alertmanager for ML: write rules for sustained high drift score, high null rate, label-join lag and stale model, with for durations, and an Alertmanager route with grouping, inhibition (do not page on drift when the upstream feed is down) and silences. Validate the rule and config files structurally with pyyaml, run a small Python re-implementation of the for-duration logic on a series, and say clearly that promtool, Prometheus and Alertmanager were not run.
**Asked at:** Prometheus and Grafana monitoring mentions (K21Academy and Towards AI question lists naming Prometheus, Grafana and Evidently for drift and accuracy dashboards; Devinterview-io page opened, Q12 mentions inference monitoring with Grafana and Prometheus; search snippets otherwise); question lists, not verified reports; MLOps and platform roles; Prometheus, Grafana and Alertmanager servers were not available in this sandbox | Alerting and SLO sources (Google SRE Workbook chapter 'Alerting on SLOs' on burn-rate and multiwindow alerts, Datadog burn-rate docs, openobserve alert-fatigue post; search snippets only, not opened, sre.google WebFetch failed with getaddrinfo ENOTFOUND); SRE docs, not ML-specific and not interview reports; MLOps, SRE and platform roles; no source found on SLOs defined for ML models, so the ML mapping is an expert extension
**Say this first (1 line):** I write alerts that must hold for a duration before they fire, keep Alertmanager routing and inhibition separate from the rules, and say honestly that here I only checked the YAML structure and re-implemented the for-logic, because Prometheus, Alertmanager and promtool were not available.

**Then explain:**
- **Rules:** sustained high drift score for 2h, null rate above a limit for 15m, label-join lag, model older than a set age. The `for:` clause makes the alert pending first and firing only if the expression stays true for the whole time; one good sample resets it.
- **Alertmanager route:** group by alertname and model so ten features do not make ten pages; `group_wait`, `group_interval` and `repeat_interval` control batching and repeats.
- **Inhibition:** if `UpstreamFeedDown` is firing for a model, mute the drift, null-rate and score-shift alerts for the same model (`equal: [model]`), since they are consequences. Silences are manual and time-boxed, for planned work.
- **Failure modes:** `for` shorter than the scrape or scoring cadence; a metric that disappears (stale series) so the alert never fires, so also alert on absence; high-cardinality labels; metric names in this answer are my own.
- **Not run:** promtool, Prometheus, Alertmanager.

**Example:** Drift is scored every 30 minutes; the rule is score above 0.3 for 2 hours, which is 4 samples in a row. In the series below, two high samples then a dip to 0.2 resets the clock. Four high samples in a row (t=120 to 210) make it fire at t=210. One spike never fires.

**Code:**
YAML:
```yaml
# ===== ml_rules.yml =====
groups:
  - name: ml-monitoring
    rules:
      - alert: UpstreamFeedDown
        expr: time() - feature_feed_last_success_timestamp_seconds{model="credit"} > 3600
        for: 10m
        labels: {severity: page, owner: data-engineering}
        annotations:
          summary: "Feature feed for {{ $labels.model }} has not updated for over an hour"
          runbook_url: https://wiki.example.com/runbooks/feed-down
      - alert: DriftScoreSustained
        expr: max by (model) (feature_drift_score{model="credit"}) > 0.3
        for: 2h
        labels: {severity: ticket, owner: data-science}
        annotations:
          summary: "Drift score above threshold for 2h on {{ $labels.model }}"
          runbook_url: https://wiki.example.com/runbooks/drift-sustained
      - alert: FeatureNullRateHigh
        expr: feature_null_ratio{model="credit"} > 0.05
        for: 15m
        labels: {severity: page, owner: data-engineering}
        annotations:
          summary: "Null rate above 5% for {{ $labels.feature }}"
          runbook_url: https://wiki.example.com/runbooks/feature-null-rate
      - alert: LabelJoinLagHigh
        expr: label_join_lag_seconds{model="credit"} > 172800
        for: 1h
        labels: {severity: ticket, owner: data-engineering}
        annotations:
          summary: "Labels are more than 2 days behind"
          runbook_url: https://wiki.example.com/runbooks/label-lag
      - alert: ModelStale
        expr: time() - model_last_trained_timestamp_seconds{model="credit"} > 30 * 86400
        for: 30m
        labels: {severity: ticket, owner: ml-platform}
        annotations:
          summary: "Model older than 30 days"
          runbook_url: https://wiki.example.com/runbooks/model-stale

# ===== alertmanager.yml =====
route:
  receiver: ml-platform-ticket
  group_by: [alertname, model]
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  routes:
    - matchers: ['severity="page"', 'owner="data-engineering"']
      receiver: data-eng-pager
    - matchers: ['severity="page"', 'owner="data-science"']
      receiver: data-science-pager
    - matchers: ['owner="data-engineering"']
      receiver: data-eng-ticket
    - matchers: ['owner="data-science"']
      receiver: data-science-ticket
inhibit_rules:
  - source_matchers: ['alertname="UpstreamFeedDown"']
    target_matchers: ['alertname=~"DriftScoreSustained|FeatureNullRateHigh|ScoreDistributionShift"']
    equal: [model]
receivers:
  - name: ml-platform-ticket
  - name: data-eng-pager
  - name: data-science-pager
  - name: data-eng-ticket
  - name: data-science-ticket
```

Python (python3 -I in a venv with numpy, scipy, pandas, scikit-learn, PyYAML as needed):
```python
# ===== check_files.py =====
import re, yaml
DUR = re.compile(r"^(\d+(ms|s|m|h|d|w|y))+$")
rules = yaml.safe_load(open("ml_rules.yml"))
errs, names = [], []
for g in rules["groups"]:
    for r in g["rules"]:
        n = r.get("alert", "?"); names.append(n)
        for k in ("alert", "expr", "for"):
            if k not in r: errs.append(f"{n}: no '{k}'")
        if "for" in r and not DUR.match(str(r["for"])): errs.append(f"{n}: bad duration {r['for']!r}")
        if r.get("expr", "").count("(") != r.get("expr", "").count(")"): errs.append(f"{n}: unbalanced brackets in expr")
        for k in ("severity", "owner"):
            if k not in r.get("labels", {}): errs.append(f"{n}: label '{k}' missing")
        if "runbook_url" not in r.get("annotations", {}): errs.append(f"{n}: no runbook_url")
am = yaml.safe_load(open("alertmanager.yml"))
recv = {x["name"] for x in am["receivers"]}
def walk(r):
    yield r
    for c in r.get("routes", []): yield from walk(c)
for r in walk(am["route"]):
    if r["receiver"] not in recv: errs.append(f"route to unknown receiver {r['receiver']}")
for i in am["inhibit_rules"]:
    for k in ("source_matchers", "target_matchers", "equal"):
        if k not in i: errs.append(f"inhibit rule missing {k}")
    src = re.findall(r'alertname="(\w+)"', " ".join(i["source_matchers"]))
    for s in src:
        if s not in names: errs.append(f"inhibit source {s} is not a defined alert")
print("alerts:", names)
print("route keys ok:", all(k in am["route"] for k in ("receiver", "group_by", "group_wait", "group_interval", "repeat_interval")))
print("errors:", errs or "none")
print("structural check only: promtool and Alertmanager were NOT run")

# ===== for_logic.py =====
# Re-implementation of the `for:` idea: inactive -> pending -> firing; one good sample resets.
def evaluate(values, threshold, for_steps):
    state, pending, log = "inactive", 0, []
    for v in values:
        if v > threshold:
            pending += 1
            state = "firing" if pending >= for_steps else "pending"
        else:
            pending, state = 0, "inactive"
        log.append(state)
    return log

# one sample per 30 minutes, drift score, rule: > 0.3 for 2h  (= 4 consecutive samples)
series = [0.1, 0.35, 0.4, 0.2, 0.31, 0.33, 0.36, 0.34, 0.35, 0.1]
log = evaluate(series, 0.3, 4)
for i, (v, s) in enumerate(zip(series, log)):
    print(f"t={i*30:3d}min value={v:.2f} {s}")
print("first firing at sample:", log.index("firing"), "| a single spike never fires:", "firing" not in evaluate([0.1, 0.9, 0.1, 0.1], 0.3, 4))
```

**Output (my run):** not executed: promtool, Prometheus and Alertmanager were not installed here, so the rules and routing were not evaluated by the real tools. What did run: PyYAML structural checks (alert, expr, for format, labels, runbook link, receivers exist, inhibit fields) and the pure-Python `for` logic below. Passing this check does not prove the PromQL is valid.
```text
alerts: ['UpstreamFeedDown', 'DriftScoreSustained', 'FeatureNullRateHigh', 'LabelJoinLagHigh', 'ModelStale']
route keys ok: True
errors: none
structural check only: promtool and Alertmanager were NOT run
t=  0min value=0.10 inactive
t= 30min value=0.35 pending
t= 60min value=0.40 pending
t= 90min value=0.20 inactive
t=120min value=0.31 pending
t=150min value=0.33 pending
t=180min value=0.36 pending
t=210min value=0.34 firing
t=240min value=0.35 firing
t=270min value=0.10 inactive
first firing at sample: 7 | a single spike never fires: True
```

**Follow-ups:**
- **Does `for` cause late pages?** Yes, by design: you trade speed for fewer false alarms. Use a short `for` for page-worthy data faults and a long one for drift.
- **How do you alert on a metric that stops?** Alert on absence (for example `absent()` or a last-success timestamp), as in `UpstreamFeedDown`.

**Common mistakes:**
- Alerting on a raw drift score with no duration.
- Forgetting inhibition, so one feed outage sends five pages.
- Calling a YAML parse "validated alerting".
- Silences with no expiry.

### Q31 ⭐⭐ 🟡 Managed monitors at concept level: SageMaker Model Monitor (data quality, model quality, bias drift, feature attribution drift with baselines, constraints and schedules) and Vertex AI Model Monitoring (training-serving skew versus prediction drift, thresholds per feature, logging to BigQuery), plus a one-line Azure ML mention. Explain the baseline-and-constraints workflow, what they need from you (data capture, training data, labels), and what they do not do. Write a constraints-style JSON of your own, validate it with a small Python checker, and label every managed service not executed. Parts 10 and 11 own the cloud services.
**Asked at:** Managed-monitor docs (Google Cloud Vertex AI Model Monitoring overview and 'monitor feature skew and drift' pages, AWS SageMaker Model Monitor FAQ and DriftCheckBaselines API pages; search snippets only, not opened; docs.cloud.google.com WebFetch failed with getaddrinfo ENOTFOUND; nothing official found on label shift in either service; the Azure ML monitoring pages were not searched); official docs, not interview reports; MLOps roles on GCP and AWS
**Say this first (1 line):** Both managed monitors work the same way at concept level: take a baseline from training data, turn it into constraints or thresholds, capture live requests, compare on a schedule and report violations; they need your data capture and, for quality metrics, your labels, and they do not decide what to do about a violation.

**Then explain:**
- **SageMaker Model Monitor (check current docs):** monitoring types for data quality, model quality, bias drift and feature attribution drift. A baseline job profiles training data and suggests statistics and constraints; scheduled jobs compare captured endpoint data against them. Model quality needs ground-truth labels you supply.
- **Vertex AI Model Monitoring (check current docs):** skew compares serving data with training data; drift compares serving data over time. Thresholds per feature, and request data can be logged to BigQuery. Attribution-based monitoring uses Explainable AI.
- **Azure ML:** has its own model monitoring; not covered here, check current docs. Parts 10 and 11 own the cloud services.
- **They do not:** fix the cause, retrain, page the right person unless you wire it, or tell you whether a flagged drift matters for accuracy. Labels, thresholds and ownership are still your job.
- **Failure modes:** baseline from a bad sample; thresholds left at defaults; alert noise; capture sampling rate too low for rare classes.

**Example:** A training set has `income` between 7,906 and 169,360, a null share of 2 percent, and `channel` in {app, web, branch}. A baseline step writes those as constraints (with slack on nulls). A serving sample with 20 percent null `age`, income mean 38 percent above reference and 14.8 percent unseen `channel` values fails three checks. This mirrors the workflow, not any vendor's schema.

**Code:**
Python (python3 -I in a venv with numpy, scipy, pandas, scikit-learn, PyYAML as needed):
```python
import json
import numpy as np, pandas as pd

rng = np.random.default_rng(31)
train = pd.DataFrame({"age": rng.integers(21, 66, 3000), "income": rng.lognormal(10.5, 0.4, 3000).round(),
                      "channel": rng.choice(["app", "web", "branch"], 3000, p=[.5, .3, .2])})
train.loc[rng.choice(3000, 60, replace=False), "income"] = np.nan

def baseline(df):
    """Own constraints-style file: a baseline summary plus allowed bounds. Field names are mine, not any vendor schema."""
    c = {}
    for col in df:
        e = {"type": "numeric" if pd.api.types.is_numeric_dtype(df[col]) else "string",
             "max_null_ratio": round(float(df[col].isna().mean()) * 2 + 0.01, 3)}
        if e["type"] == "numeric":
            e["min"], e["max"] = float(df[col].min()), float(df[col].max())
            e["mean_ref"], e["mean_tolerance_pct"] = round(float(df[col].mean()), 1), 15
        else:
            e["allowed_values"] = sorted(df[col].dropna().unique().tolist())
            e["max_new_value_ratio"] = 0.01
        c[col] = e
    return {"version": 1, "row_count_min": int(len(df) * 0.1), "columns": c}

def check(df, cons):
    v = []
    if len(df) < cons["row_count_min"]: v.append(f"row count {len(df)} below {cons['row_count_min']}")
    for col, e in cons["columns"].items():
        if col not in df: v.append(f"{col}: column missing"); continue
        nr = df[col].isna().mean()
        if nr > e["max_null_ratio"]: v.append(f"{col}: null ratio {nr:.3f} > {e['max_null_ratio']}")
        if e["type"] == "numeric":
            s = df[col].dropna()
            if s.min() < e["min"] or s.max() > e["max"]: v.append(f"{col}: range [{s.min():.0f}, {s.max():.0f}] outside [{e['min']:.0f}, {e['max']:.0f}]")
            dev = abs(s.mean() - e["mean_ref"]) / e["mean_ref"] * 100
            if dev > e["mean_tolerance_pct"]: v.append(f"{col}: mean moved {dev:.0f}% (> {e['mean_tolerance_pct']}%)")
        else:
            bad = (~df[col].dropna().isin(e["allowed_values"])).mean()
            if bad > e["max_new_value_ratio"]: v.append(f"{col}: {bad:.1%} unseen values")
    return v

cons = baseline(train)
open("constraints.json", "w").write(json.dumps(cons, indent=1))
print(json.dumps(cons["columns"]["income"]), "\n")

ok = train.sample(500, random_state=1)
bad = pd.DataFrame({"age": rng.integers(21, 66, 500), "income": (rng.lognormal(10.5, 0.4, 500) * 1.4).round(),
                    "channel": rng.choice(["app", "web", "branch", "agent"], 500, p=[.4, .3, .15, .15])})
bad.loc[rng.choice(500, 100, replace=False), "age"] = np.nan
for name, d in (("clean serving sample", ok), ("bad serving sample", bad)):
    v = check(d, cons)
    print(name, "->", "PASS" if not v else "FAIL")
    for x in v: print("   -", x)
```

**Output (my run):** not executed for SageMaker Model Monitor, Vertex AI Model Monitoring and Azure ML: no cloud account or access here. What did run: my own constraints-style baseline and checker (pandas 3.1.0, numpy 2.5.4, seed 31); the field names are mine and are not any vendor's format. The JSON it wrote is code/q31/constraints.json.
```text
{"type": "numeric", "max_null_ratio": 0.05, "min": 7906.0, "max": 169360.0, "mean_ref": 39412.2, "mean_tolerance_pct": 15} 

clean serving sample -> PASS
bad serving sample -> FAIL
   - age: null ratio 0.200 > 0.01
   - income: mean moved 38% (> 15%)
   - channel: 14.8% unseen values
```

**Follow-ups:**
- **Skew vs drift?** Skew: serving differs from training. Drift: serving changes over time. You need training data for skew.
- **Why build your own anyway?** Cross-cloud needs, custom checks, and control of alert routing. A managed monitor is a good start.

**Common mistakes:**
- Thinking a managed monitor means monitoring is done.
- Leaving default thresholds.
- Forgetting to give it labels for model quality.
- Quoting service limits from memory.

### Q32 ⭐⭐ 🟡 Monitoring batch inference versus real-time. Compare the checks per batch run (input volume and schema, null rate, score distribution versus last run, output row count versus input, runtime), the cadence of drift tests, and how late labels join. Implement a run-level validator that compares a batch with the previous run and the reference, run it on three nightly batches (normal, truncated input, shifted scores), and print pass or fail with reasons. Part 5 owns the scheduler and Part 6 the batch serving mechanics.
**Asked at:** MLOps interview question banks and guides (K21Academy '47 MLOps interview questions' PDF, Towards AI '101 ML LLM agentic AIOps interview questions', DataCamp MLOps interview questions, The Interview Guys MLOps post, wecreateproblems.com, hyring.com, dev.to vivekk101, a Medium skphd post; search snippets only, not opened; the Devinterview-io/mlops-interview-questions GitHub page WAS opened and has no dedicated monitoring or drift question, only monitoring bullets inside Q1, Q2, Q4, Q6, Q7 and Q12); editorial question lists, not verified candidate reports; MLOps, ML platform and ML engineer roles at IT-services firms, product companies and GCCs | Expert extension: no source found for the exact question; the topic follows from the library behaviour tested in this sandbox and from general monitoring practice, and Wave B must verify against current docs; MLOps, ML platform and ML engineer roles, including IT-services firms, product companies and GCCs
**Say this first (1 line):** For a batch run I validate the run itself, not each row: input volume and schema, nulls, output row count equals input, runtime, and score distribution against the last run and the reference, and I fail the run before results are published.

**Then explain:**
- **Per run checks:** input rows versus last run, schema, null rate, output rows equal input rows, runtime versus normal, score distribution versus last run and the reference set.
- **Cadence:** a drift test per run is cheap for a daily batch; labels join later (days or weeks), so a performance check is a lagged job, not part of the run gate.
- **Real-time difference:** real-time uses rolling windows and alerts with `for` durations; batch has a natural unit (the run) so you can block publishing. Part 5 owns the scheduler and Part 6 batch serving mechanics.
- **Failure modes:** comparing only with the last run so a slow drift is never caught (also compare with the reference); a truncated input that still produces a matching output; a threshold on row count that breaks on holidays; blocking forever with nobody on call.
- **Action on failure:** keep yesterday's output, alert the owner, do not publish.

**Example:** Three nights. Night 1: 10,200 rows against 10,000 last time, passes. Night 2: 4,100 rows is 41 percent of last night, fails on volume (a truncated extract). Night 3: row count fine but scores moved (KS D = 0.58 against last run and reference), fails on score distribution.

**Code:**
Python (python3 -I in a venv with numpy, scipy, pandas, scikit-learn, PyYAML as needed):
```python
import numpy as np, pandas as pd
from scipy.stats import ks_2samp

rng = np.random.default_rng(32)
def make(n, shift=0.0, null_rate=0.01):
    df = pd.DataFrame({"id": np.arange(n), "amount": rng.lognormal(8, 0.5, n), "tenure": rng.integers(1, 120, n)})
    df.loc[rng.random(n) < null_rate, "tenure"] = np.nan
    df["score"] = np.clip(rng.beta(2, 5, n) + shift, 0, 1)
    return df

ref = make(10_000)
prev = {"rows_in": 10_000, "rows_out": 10_000, "runtime_s": 610, "scores": make(10_000)["score"].to_numpy()}
batches = {
    "night-1 normal":    dict(inp=make(10_200), out_rows=10_200, runtime=640),
    "night-2 truncated": dict(inp=make(4_100), out_rows=4_100, runtime=250),
    "night-3 shifted":   dict(inp=make(10_050, shift=0.25), out_rows=10_050, runtime=620),
}

def validate(inp, scores, out_rows, runtime):
    why = []
    if not 0.7 <= len(inp) / prev["rows_in"] <= 1.3: why.append(f"input rows {len(inp)} vs last run {prev['rows_in']}")
    if set(ref.columns) - set(inp.columns): why.append("schema: missing columns")
    nulls = inp.isna().mean()
    if (nulls > 0.05).any(): why.append(f"null rate high in {nulls[nulls > 0.05].index.tolist()}")
    if out_rows != len(inp): why.append(f"output rows {out_rows} != input rows {len(inp)}")
    if runtime > 2 * prev["runtime_s"]: why.append(f"runtime {runtime}s more than 2x last run")
    d = ks_2samp(scores, prev["scores"])
    if d.statistic > 0.1: why.append(f"score distribution moved vs last run (KS D={d.statistic:.2f})")
    d_ref = ks_2samp(scores, ref["score"])
    if d_ref.statistic > 0.1: why.append(f"score distribution moved vs reference (KS D={d_ref.statistic:.2f})")
    return why

for name, b in batches.items():
    inp = b["inp"]
    scores = inp["score"].to_numpy()
    why = validate(inp, scores, b["out_rows"], b["runtime"])
    print(f"{name:20s} {'PASS' if not why else 'FAIL'}")
    for w in why: print("    -", w)
```

**Output (my run):** (real run, numpy 2.5.4, scipy 1.18.1, pandas 3.1.0, seed 32; the batches are simulated. The 0.7 to 1.3 row ratio, 2x runtime and KS 0.1 limits are my illustrative choices, tune them on your history.)
```text
night-1 normal       PASS
night-2 truncated    FAIL
    - input rows 4100 vs last run 10000
night-3 shifted      FAIL
    - score distribution moved vs last run (KS D=0.58)
    - score distribution moved vs reference (KS D=0.58)
```

**Follow-ups:**
- **Why did night 2 not fail on runtime?** A short run is not checked here; add a lower bound if truncation matters to you.
- **Last run or reference?** Both: last run catches sudden changes, reference catches slow drift.

**Common mistakes:**
- Letting a failed validation still publish scores.
- Comparing only with yesterday.
- KS on a huge batch with no minimum effect size.
- Not storing the per-run metrics, so there is no history to set limits from.

### Q33 ⭐⭐ 🟡 Retraining pitfalls and feedback loops. Explain selection bias when the model decides which cases get a label (loan approved or rejected, fraud blocked), training on drifted or corrupted data, retraining too often so a bad week is learned, and a recommender learning from its own exposures. Simulate a selection-bias loop where only approved cases get labels, show the retrained model's measured metric versus true metric, and give mitigations (exploration, holdout, reject inference at concept level, recency weights and data gates).
**Asked at:** MLOps interview question banks and guides (K21Academy '47 MLOps interview questions' PDF, Towards AI '101 ML LLM agentic AIOps interview questions', DataCamp MLOps interview questions, The Interview Guys MLOps post, wecreateproblems.com, hyring.com, dev.to vivekk101, a Medium skphd post; search snippets only, not opened; the Devinterview-io/mlops-interview-questions GitHub page WAS opened and has no dedicated monitoring or drift question, only monitoring bullets inside Q1, Q2, Q4, Q6, Q7 and Q12); editorial question lists, not verified candidate reports; MLOps, ML platform and ML engineer roles at IT-services firms, product companies and GCCs | Retraining and champion-challenger sources (apxml.com 'retraining triggers', DataRobot docs on retraining settings and challengers, a pertamapartners glossary on shadow comparison windows, an ifactoryapp retraining-cadence guide; search snippets only, not opened; numeric windows and percentages in them are vendor suggestions and are not used); vendor docs and blogs, not interview reports; MLOps and ML platform roles
**Say this first (1 line):** If the model decides which cases get a label, retraining on those labels learns a biased picture: the measured metric looks fine while the true metric on everyone is worse, so I keep an exploration holdout, weight it, and gate retrains.

**Then explain:**
- **Selection bias:** loans are approved by the old policy and only approved loans get repayment labels; fraud blocked is never confirmed. The new model is trained and measured only on the cases the old model liked.
- **Other pitfalls:** retraining on drifted or corrupted data (gate the data first), retraining so often that a bad week is learned, a recommender learning from what it chose to show (exposure feedback loop).
- **Mitigations:** an exploration holdout (approve or show a small random share, weight by 1 over its probability), reject inference at concept level (careful, it adds its own assumptions), recency weights, data gates and a champion-challenger check before swap.
- **Costs:** exploration means knowingly taking some risk, so it needs business sign-off and a cap.
- **Failure modes:** reporting the AUC on approved cases only; weights that are huge for a few cases; using the holdout for tuning and for evaluation.

**Example:** Policy rejects applicants whose bureau-like score is below a cutoff (30 percent). In the simulation, thin-file applicants behave the opposite way on a second feature. A model trained on approved cases gets measured AUC 0.774 on approved cases but true AUC 0.735 on all, and 0.467 inside the rejected region. With 916 exploration labels (5 percent of rejected) weighted by 20, true AUC is 0.814 and 0.803 in the rejected region. The measured AUC on approved cases barely changes (0.773), which is why it cannot tell you.

**Code:**
Python (python3 -I in a venv with numpy, scipy, pandas, scikit-learn, PyYAML as needed):
```python
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import roc_auc_score

rng = np.random.default_rng(33)
def applicants(n):
    x1 = rng.normal(0, 1, n)                 # bureau-like score (higher is safer)
    x2 = rng.normal(0, 1, n)                 # other signal
    # truth: for normal applicants x1 and x2 both matter; for thin-file (x1 low) x2 matters in the OPPOSITE way
    logit = -0.5 - 1.2 * x1 + np.where(x1 > -0.5, 0.9 * x2, -1.5 * x2)
    y = (rng.random(n) < 1 / (1 + np.exp(-logit))).astype(int)      # 1 = defaults
    return np.c_[x1, x2], y

X, y = applicants(60_000)
X_new, y_new = applicants(60_000)             # fresh applicants, ALL labelled: this is the truth we can only see in a simulation

# old policy: reject x1 < -0.5; labels exist only for approved
approved = X[:, 0] >= -0.5
print(f"approved {approved.mean():.0%} of applicants; labels observed for {approved.sum()} of {len(y)}")

def fit(Xt, yt, w=None):
    return GradientBoostingClassifier(n_estimators=100, max_depth=3, random_state=0).fit(Xt, yt, sample_weight=w)

m = fit(X[approved], y[approved])
ap_new = X_new[:, 0] >= -0.5
print("--- retrain on approved-only labels")
print(f"measured AUC (approved applicants only) {roc_auc_score(y_new[ap_new], m.predict_proba(X_new[ap_new])[:, 1]):.3f}")
print(f"true AUC (all applicants)               {roc_auc_score(y_new, m.predict_proba(X_new)[:, 1]):.3f}")
print(f"true AUC inside rejected region         {roc_auc_score(y_new[~ap_new], m.predict_proba(X_new[~ap_new])[:, 1]):.3f}")

# mitigation: approve a random 5 % of the would-be rejected (exploration holdout), weight them 1/0.05
EPS = 0.05
explore = (~approved) & (rng.random(len(y)) < EPS)
use = approved | explore
w = np.where(explore, 1 / EPS, 1.0)
m2 = fit(X[use], y[use], w[use])
print(f"--- retrain with {explore.sum()} exploration labels (cost: we knowingly approve some risky cases)")
print(f"true AUC (all applicants)               {roc_auc_score(y_new, m2.predict_proba(X_new)[:, 1]):.3f}")
print(f"true AUC inside rejected region         {roc_auc_score(y_new[~ap_new], m2.predict_proba(X_new[~ap_new])[:, 1]):.3f}")
print(f"measured AUC (approved applicants only) {roc_auc_score(y_new[ap_new], m2.predict_proba(X_new[ap_new])[:, 1]):.3f}")
```

**Output (my run):** (real run, numpy 2.5.4, scikit-learn 1.9.1, seed 33; the data and the rejected-region behaviour are simulated by me, real data will not be so tidy)
```text
approved 70% of applicants; labels observed for 41713 of 60000
--- retrain on approved-only labels
measured AUC (approved applicants only) 0.774
true AUC (all applicants)               0.735
true AUC inside rejected region         0.467
--- retrain with 916 exploration labels (cost: we knowingly approve some risky cases)
true AUC (all applicants)               0.814
true AUC inside rejected region         0.803
measured AUC (approved applicants only) 0.773
```

**Follow-ups:**
- **Why not just use reject inference?** It needs assumptions about rejected cases that you cannot check; an exploration holdout gives real labels.
- **How big should the holdout be?** Big enough to give stable labels in the rejected region, small enough for the risk budget; this is a business choice.

**Common mistakes:**
- Evaluating the new model only on cases the old model approved.
- Retraining automatically with no gate on the data.
- Weights applied to the holdout but not to the metric.
- Asking for exploration without a loss cap.

### Q34 ⭐⭐ 🟡 Incident handling for a model failure. A model gave bad predictions for three days before anyone noticed. Explain detect, triage, mitigate (roll back, fallback rule, pause decisions), communicate, root cause, and the blameless post-mortem with a trigger, an amplifier and a concealer (what hid it). Write a post-mortem template, fill it for a simulated unit-change incident, compute time to detect and time to mitigate from an event log with pandas, and list three monitoring gaps and action items with owners.
**Asked at:** Silent-failure and post-mortem sources (arXiv 2608.02786 'Evaluation Blindness', arXiv 2606.14589 taxonomy of silent failures, tianpan.co AI incident post-mortem post with a trigger/amplifier/concealer split, jacar.es AI incident post-mortems, a towardsdatascience upstream-mentality post with an anecdotal vendor-schema-change story; search snippets only, not opened; the 40 percent figure in that anecdote is not used); papers and blogs, not company post-mortems; MLOps, ML engineer and SRE roles | Scenario question write-ups (a Glassdoor EPAM Systems interview page whose snippet lists 'why does production differ from training' with feature, preprocessing and version mismatch as causes, and an end-to-end design prompt; one candidate's review, search snippet only, not opened, unverified; The Interview Guys post saying drift is asked in almost every MLOps interview, snippet only); anecdotal, not company-verified reports; MLOps and ML engineer roles
**Say this first (1 line):** First stop the damage (roll back or use the fallback), then communicate, find the cause, and write a blameless post-mortem that names the trigger, the amplifier and the concealer, with numbers for time to detect and time to mitigate and action items with owners.

**Then explain:**
- **Order:** detect, triage (how bad, who is affected, which decisions), mitigate (roll back, fallback rule, pause decisions), communicate (a named owner sends updates), find the root cause, then learn. Mitigation comes before understanding.
- **Blameless:** write about systems and decisions, not people. The question is why the system let it happen.
- **Trigger, amplifier, concealer:** trigger started it (unit change upstream), amplifier made it bigger (no input check, so bad rows flowed on), concealer hid it (only a dashboard, no alert, an average that moved slowly, labels days late).
- **Times:** time to notice (any human), time to detect (ML team), time to mitigate, time to resolve. A long gap before detection is usually a gap in monitoring or handoff, not in the fix.
- **Failure modes:** fixing the data but not the missing check; action items with no owner or date; a dashboard that nobody looks at counted as monitoring.

**Example:** Upstream switches income from rupees to thousands of rupees on 2 March 02:00. Approval rate falls; an ops analyst notices on 4 March (55 hours), the ML ticket opens a day later, the dashboard confirms 81 hours after the fault started, the fallback rule is on 0.8 hours after that. The log below is simulated; there is no real company incident behind it.

**Code:**
Python (python3 -I in a venv with numpy, scipy, pandas, scikit-learn, PyYAML as needed):
```python
import io
import pandas as pd

# Simulated incident: on 2026-03-02 the upstream income feed switched from rupees to thousands of rupees.
LOG = """ts,event,who
2026-03-02 02:00,fault_start: upstream feed changes income unit,upstream-team
2026-03-02 02:30,first bad scores served,model-service
2026-03-04 09:15,business user notices approval rate fell,ops-analyst
2026-03-05 10:40,ticket opened to ml team,ops-analyst
2026-03-05 11:20,drift dashboard confirms income mean 1000x lower,ml-engineer
2026-03-05 12:05,mitigation: model switched to fallback rule,ml-engineer
2026-03-05 16:30,feed fixed upstream and unit converted,upstream-team
2026-03-06 09:00,model switched back after check,ml-engineer
"""
ev = pd.read_csv(io.StringIO(LOG), parse_dates=["ts"])
t = {k: ev.loc[ev.event.str.startswith(k), "ts"].iloc[0] for k in ("fault_start", "first bad", "business user", "ticket", "drift dashboard", "mitigation", "feed fixed", "model switched back")}
h = lambda a, b: round((t[b] - t[a]).total_seconds() / 3600, 1)
rows = [("time to first human notice (from fault start)", h("fault_start", "business user")),
        ("time to detect by ML team (from fault start)", h("fault_start", "drift dashboard")),
        ("time to mitigate (detect to fallback)", h("drift dashboard", "mitigation")),
        ("time to mitigate (from fault start)", h("fault_start", "mitigation")),
        ("time to resolve (fault start to switched back)", h("fault_start", "model switched back")),
        ("handoff delay (notice to ML ticket)", h("business user", "ticket"))]
for k, v in rows: print(f"{k:50s} {v:6.1f} h  ({v/24:.1f} d)")
print("bad predictions served for", round((t["mitigation"] - t["first bad"]).total_seconds() / 3600, 1), "hours")

gaps = pd.DataFrame([
    ("No input range or unit check on income", "Add a range and null check at feature ingestion; page on failure", "data-engineering", "2026-03-20"),
    ("Drift alert was not wired to a page or a ticket; dashboard only", "Alert on income mean and PSI-style score with a runbook (Q27, Q30)", "ml-platform", "2026-03-27"),
    ("No contract or change notice with the upstream team", "Schema and unit contract test in the feed's CI; change announcements", "upstream-team", "2026-04-10"),
], columns=["gap", "action", "owner", "due"])
print()
print(gaps.to_string(index=False))
```

Post-mortem template:
```markdown
# Post-mortem: <short title>            (blameless: describe systems and decisions, not people)
Date of incident: <start - end>   Severity: <S1-S3>   Author: <name>   Status: <draft/final>

## Summary (3 lines)
What broke, who was affected, how it ended.

## Impact
Decisions affected (count, value), customers or teams, how long, what we could not undo.

## Timeline (from the event log, in UTC or IST, say which)
| time | event | source |

## Key times
Time to notice (any human) / time to detect (ML team) / time to mitigate / time to resolve.

## Root cause
- Trigger: the change that started it.
- Amplifier: what made it worse or bigger (for example no input check, auto-retrain used the bad data).
- Concealer: what hid it (for example the dashboard averaged it away, labels arrive in 30 days).

## What went well / what was lucky

## Monitoring gaps and action items
| gap | action | owner | due | how we will know it works |

## Lessons for the runbook
```

**Output (my run):** (real run, pandas 3.1.0, seed not needed (fixed log); the timeline and the owners are invented for the exercise)
```text
time to first human notice (from fault start)        55.2 h  (2.3 d)
time to detect by ML team (from fault start)         81.3 h  (3.4 d)
time to mitigate (detect to fallback)                 0.8 h  (0.0 d)
time to mitigate (from fault start)                  82.1 h  (3.4 d)
time to resolve (fault start to switched back)      103.0 h  (4.3 d)
handoff delay (notice to ML ticket)                  25.4 h  (1.1 d)
bad predictions served for 81.6 hours

                                                            gap                                                               action            owner        due
                         No input range or unit check on income     Add a range and null check at feature ingestion; page on failure data-engineering 2026-03-20
Drift alert was not wired to a page or a ticket; dashboard only   Alert on income mean and PSI-style score with a runbook (Q27, Q30)      ml-platform 2026-03-27
            No contract or change notice with the upstream team Schema and unit contract test in the feed's CI; change announcements    upstream-team 2026-04-10
```

**Follow-ups:**
- **Roll back or fix forward?** Roll back (or use the fallback) when it is quick and safe; fix forward only when rollback is not possible and the fix is simple.
- **How do you stop the next one?** Input checks at ingestion, alerts with owners and runbooks (Q27, Q30), contracts with upstream, and a drill.

**Common mistakes:**
- Naming a person as the cause.
- Counting time to detect from when the ticket opened.
- Action items like "be more careful".
- Closing the incident with no check that the new alert would really have fired.
