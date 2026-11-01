# Book 4 Part 8, Q1-Q12 answers (Wave B)

### Q1 ⭐⭐⭐ 🟢 Why do ML models degrade after deployment? Define data drift (covariate shift), concept drift, label or prior shift and an upstream data change, and separate all four from training-serving skew, which is a bug and not a world change. For each say what changes (P(x), P(y|x), P(y)), what you can see without labels and what needs labels. Simulate the four on synthetic data with numpy and a simple scikit-learn classifier, report the feature-drift statistic, the prediction-rate change and the accuracy for each, and show which cases a feature-only monitor misses. Book 1 owns the theory, so keep to what a monitor needs.
**Asked at:** MLOps interview question banks and guides (K21Academy '47 MLOps interview questions' PDF, Towards AI '101 ML LLM agentic AIOps interview questions', DataCamp MLOps interview questions, The Interview Guys MLOps post, wecreateproblems.com, hyring.com, dev.to vivekk101, a Medium skphd post; search snippets only, not opened; the Devinterview-io/mlops-interview-questions GitHub page WAS opened and has no dedicated monitoring or drift question, only monitoring bullets inside Q1, Q2, Q4, Q6, Q7 and Q12); editorial question lists, not verified candidate reports; MLOps, ML platform and ML engineer roles at IT-services firms, product companies and GCCs | Scenario question write-ups (a Glassdoor EPAM Systems interview page whose snippet lists 'why does production differ from training' with feature, preprocessing and version mismatch as causes, and an end-to-end design prompt; one candidate's review, search snippet only, not opened, unverified; The Interview Guys post saying drift is asked in almost every MLOps interview, snippet only); anecdotal, not company-verified reports; MLOps and ML engineer roles
**Say this first (1 line):** Models degrade because the world, the data pipeline or the labels change after training, and a feature-only monitor sees only some of those changes. Four are real changes (covariate, concept, prior, upstream data) and one is a bug (training-serving skew).

**Then explain:**
- **Data drift (covariate shift):** P(x) moves, P(y|x) is the same. Visible without labels. Often harmless if the model still covers that region (see the accuracy in my run).
- **Concept drift:** P(y|x) moves, inputs look the same. Invisible to feature tests. Needs labels, or at least a proxy for them.
- **Label (prior) shift:** P(y) moves, P(x|y) is the same. You see it as a change in the prediction rate. Confirming it needs labels.
- **Upstream data change:** a source renames a column, changes a unit, or starts sending nulls. It is a real change in the data, usually sudden, and a data-quality check should catch it first.
- **Training-serving skew:** same world, but the serving code builds features differently from the training code. It looks like drift on a dashboard. The test that separates it: replay the same raw rows through both code paths. If the outputs differ, it is a bug, not the world.
- Failure mode: a feature-only monitor gives false comfort on concept drift (D stays near 0.01 while accuracy falls) and false alarms on harmless covariate shift. Accuracy also depends on class mix, so compare it across prevalence changes with care.

**Example:** Loan model, income feature. Customers get richer (covariate shift, inputs move). Defaults rise at the same income (concept drift, inputs look the same). A bank sends income in thousands instead of rupees (upstream change). The scoring service divides by 12 where training did not (skew). All four can look like "income distribution moved"; the response is different for each.

**Code:**
```python
import numpy as np
from scipy.stats import ks_2samp
from sklearn.linear_model import LogisticRegression

rng = np.random.default_rng(1)
N = 20000

def make(n, w=(2.0, 1.0, 0.0), mean1=0.0):
    X = rng.normal(0, 1, (n, 3)); X[:, 0] += mean1
    p = 1 / (1 + np.exp(-(X @ np.array(w) - 0.2)))
    return X, (rng.random(n) < p).astype(int)

Xtr, ytr = make(N)
model = LogisticRegression().fit(Xtr, ytr)

def report(name, X, y, note):
    d = max(ks_2samp(Xtr[:, j], X[:, j]).statistic for j in range(3))
    pred = model.predict(X)
    print(f"{name:<22} maxKS_D={d:5.3f}  pos_rate={pred.mean():5.3f}  acc={(pred == y).mean():5.3f}  {note}")

print(f"{'train (reference)':<22} pos_rate={model.predict(Xtr).mean():5.3f}  acc={model.score(Xtr, ytr):5.3f}")
X, y = make(N);                      report("no change", X, y, "control")
X, y = make(N, mean1=1.0);           report("covariate shift", X, y, "P(x) moved, P(y|x) same")
X, y = make(N, w=(2.0, -1.0, 0.0));  report("concept drift", X, y, "x same, P(y|x) changed")
# label/prior shift: keep P(x|y), resample so positives are rarer
Xp, yp = make(4 * N)
keep = (yp == 0) | (rng.random(len(yp)) < 0.2)
report("label (prior) shift", Xp[keep][:N], yp[keep][:N], "P(y) 0.5 -> about 0.17")
# upstream change: feature 2 now arrives as 0 (null filled with 0)
X, y = make(N); X[:, 1] = 0.0;       report("upstream change", X, y, "feature 2 filled with 0")
# skew: serving code scales feature 1 differently from training code
X, y = make(N); Xs = X.copy(); Xs[:, 0] *= 100
d = max(ks_2samp(Xtr[:, j], Xs[:, j]).statistic for j in range(3))
pred = model.predict(Xs)
print(f"{'train-serve skew':<22} maxKS_D={d:5.3f}  pos_rate={pred.mean():5.3f}  acc={(pred == y).mean():5.3f}  bug: unit scale")
# the skew check: replay the same raw rows through both code paths
print("parity max abs diff, same raw rows:", float(np.abs(Xs - X).max()).__round__(1), "(world data identical, pipeline differs)")
```

**Output (my run):**
```text
train (reference)      pos_rate=0.455  acc=0.792
no change              maxKS_D=0.011  pos_rate=0.462  acc=0.793  control
covariate shift        maxKS_D=0.385  pos_rate=0.786  acc=0.836  P(x) moved, P(y|x) same
concept drift          maxKS_D=0.015  pos_rate=0.457  acc=0.653  x same, P(y|x) changed
label (prior) shift    maxKS_D=0.167  pos_rate=0.269  acc=0.811  P(y) 0.5 -> about 0.17
upstream change        maxKS_D=0.504  pos_rate=0.451  acc=0.745  feature 2 filled with 0
train-serve skew       maxKS_D=0.493  pos_rate=0.506  acc=0.747  bug: unit scale
parity max abs diff, same raw rows: 478.9 (world data identical, pipeline differs)
```
Ran with `python3 -I`, Python 3.13, numpy 2.5.4, scipy 1.18.1, scikit-learn 1.9.1, seeded.

How to read it:
| Case | Feature KS (max D) | Prediction rate | Accuracy | What a feature-only monitor does |
|---|---|---|---|---|
| Covariate shift | 0.385, loud | up a lot | did not fall (0.836) | alarm, though no harm here |
| Concept drift | 0.015, quiet | flat | fell 0.793 to 0.653 | **misses it** |
| Prior shift | 0.167 | fell to 0.269 | similar (0.811, but class mix changed) | alarm; the prediction-rate check is the cleaner signal |
| Upstream change | 0.504 | flat | fell to 0.745 | alarm; a null/constant check names the cause |
| Skew | 0.493 | up | fell to 0.747 | alarm; only the parity replay says "bug" |

**Follow-ups:**
- *Which of these can you see without labels?* Covariate, upstream and skew show in inputs; prior shows in the prediction rate. Concept drift needs labels or proxies.
- *Does covariate shift always hurt?* No. Here accuracy stayed fine. It hurts when data moves where the model extrapolates badly.
- *First thing you do on a drift alert?* Check data quality and the pipeline for a change before you blame the world.

**Common mistakes:**
- Calling skew "drift" and retraining. You then train on the bug.
- Trusting feature drift as a stand-in for performance.
- Comparing accuracy across a prevalence change without noting the class mix changed.

---

### Q2 ⭐⭐⭐ 🟢 What exactly do you monitor for a model in production, and who owns each layer? Lay out the layers (infrastructure and serving health, data quality, feature drift, prediction drift, model performance, fairness, business outcome), what each one catches, the cadence, the needed labels and the owner. Be explicit about the boundary: Part 6 owns serving latency, errors and probes, and Part 8 starts at the data and the model. Write the layer map as YAML, parse it with pyyaml and print which layers need labels and which can run in real time.
**Asked at:** MLOps interview question banks and guides (K21Academy '47 MLOps interview questions' PDF, Towards AI '101 ML LLM agentic AIOps interview questions', DataCamp MLOps interview questions, The Interview Guys MLOps post, wecreateproblems.com, hyring.com, dev.to vivekk101, a Medium skphd post; search snippets only, not opened; the Devinterview-io/mlops-interview-questions GitHub page WAS opened and has no dedicated monitoring or drift question, only monitoring bullets inside Q1, Q2, Q4, Q6, Q7 and Q12); editorial question lists, not verified candidate reports; MLOps, ML platform and ML engineer roles at IT-services firms, product companies and GCCs | Prometheus and Grafana monitoring mentions (K21Academy and Towards AI question lists naming Prometheus, Grafana and Evidently for drift and accuracy dashboards; Devinterview-io page opened, Q12 mentions inference monitoring with Grafana and Prometheus; search snippets otherwise); question lists, not verified reports; MLOps and platform roles; Prometheus, Grafana and Alertmanager servers were not available in this sandbox
**Say this first (1 line):** I monitor in layers, each with an owner and a cadence: serving health, data quality, feature drift, prediction drift, model performance, fairness and business outcome. Only the last three need labels.

**Then explain:**
- Earlier layers are cheap and fast but only hint at harm. Later layers measure real harm but are slow because labels are late.
- Boundary: Part 6 owns latency, errors, saturation and probes. I start at the data and the model.
- Each layer needs a named owner and an action. An alert nobody owns is just noise.
- Failure modes: only watching infra (a model can be fast and wrong); only watching drift (it can be harmless); only watching accuracy (you learn weeks late).

| Layer | Catches | Cadence | Needs labels | Owner |
|---|---|---|---|---|
| Serving health | latency, errors, saturation (Part 6) | real time | no | platform/SRE |
| Data quality | nulls, schema, range, freshness, volume | per batch | no | data eng |
| Feature drift | input distribution change | daily | no | ML eng |
| Prediction drift | score or positive-rate change | hourly | no | ML eng |
| Performance | real accuracy, AUC, calibration | weekly | yes | DS / ML eng |
| Fairness | gap between groups | monthly | yes (and group data) | DS + risk |
| Business outcome | conversion, loss, revenue | weekly | yes | product |

(The cadences are my example, not a standard; set them from how fast the data moves and how costly a miss is.)

**Example:** Fraud model. Data quality says "merchant_id null rate jumped" within the hour. Prediction drift says the flag rate halved the same day. Chargeback labels, 30 days later, confirm the loss. Each layer gave an earlier or later piece of the story.

**Code:**
```python
import yaml

LAYERS = """
layers:
  - {name: serving_health,  owner: platform/SRE,  cadence: realtime,  needs_labels: false, catches: latency, errors, saturation (Part 6)}
  - {name: data_quality,    owner: data eng,      cadence: per batch, needs_labels: false, catches: nulls, schema, range, freshness, volume}
  - {name: feature_drift,   owner: ML eng,        cadence: daily,     needs_labels: false, catches: input distribution change}
  - {name: prediction_drift,owner: ML eng,        cadence: hourly,    needs_labels: false, catches: score or positive-rate change}
  - {name: performance,     owner: DS / ML eng,   cadence: weekly,    needs_labels: true,  catches: real accuracy, AUC, calibration loss}
  - {name: fairness,        owner: DS + risk,     cadence: monthly,   needs_labels: true,  catches: gap between groups}
  - {name: business_outcome,owner: product,       cadence: weekly,    needs_labels: true,  catches: conversion, loss, revenue effect}
"""
cfg = yaml.safe_load(LAYERS)
rows = cfg["layers"]
print("layers parsed:", len(rows))
print("need labels :", [r["name"] for r in rows if r["needs_labels"]])
print("no labels   :", [r["name"] for r in rows if not r["needs_labels"]])
print("realtime or per-batch or hourly (no labels):",
      [r["name"] for r in rows if not r["needs_labels"] and r["cadence"] in ("realtime", "per batch", "hourly")])
for r in rows:
    print(f"{r['name']:<17} {r['cadence']:<10} owner={r['owner']}")
```

**Output (my run):**
```text
layers parsed: 7
need labels : ['performance', 'fairness', 'business_outcome']
no labels   : ['serving_health', 'data_quality', 'feature_drift', 'prediction_drift']
realtime or per-batch or hourly (no labels): ['serving_health', 'data_quality', 'prediction_drift']
serving_health    realtime   owner=platform/SRE
data_quality      per batch  owner=data eng
feature_drift     daily      owner=ML eng
prediction_drift  hourly     owner=ML eng
performance       weekly     owner=DS / ML eng
fairness          monthly    owner=DS + risk
business_outcome  weekly     owner=product
```
Ran with `python3 -I`, PyYAML 6.0.3. This is a config check only; it proves the map parses and answers the label question, not that the layers are healthy.

**Follow-ups:**
- *Which layers can page someone at night?* Serving health and hard data-quality failures. Drift and performance usually open tickets.
- *Where do you start with one engineer and no budget?* Data quality plus prediction drift plus a labelled audit sample.
- *Who owns fairness?* A shared owner with risk or compliance; the data scientist alone should not decide the threshold.

**Common mistakes:**
- One dashboard with no owner per panel.
- Listing tools instead of layers.
- Putting a label-dependent metric on a real-time alert (it cannot fire in real time).

---

### Q3 ⭐⭐⭐ 🟡 Population Stability Index from scratch. Explain how PSI is computed, why reference quantile bins are the usual choice, what to do with empty bins (epsilon or smoothing), how PSI treats categorical features, and why the 0.1 and 0.25 rules of thumb are conventions, not laws. Implement it with numpy, run it on no shift, a mean shift, a variance-only shift and a tail-only shift, and show how the value moves with the number of bins (5, 10, 20) and with sample size at no true shift.
**Asked at:** MLOps interview question banks and guides (K21Academy '47 MLOps interview questions' PDF, Towards AI '101 ML LLM agentic AIOps interview questions', DataCamp MLOps interview questions, The Interview Guys MLOps post, wecreateproblems.com, hyring.com, dev.to vivekk101, a Medium skphd post; search snippets only, not opened; the Devinterview-io/mlops-interview-questions GitHub page WAS opened and has no dedicated monitoring or drift question, only monitoring bullets inside Q1, Q2, Q4, Q6, Q7 and Q12); editorial question lists, not verified candidate reports; MLOps, ML platform and ML engineer roles at IT-services firms, product companies and GCCs | Drift-test pitfall sources (Evidently blog 'data drift detection on large datasets' saying KS is too sensitive on large data, an Arize docs monitors page saying PSI is less sample-sensitive, an ICLR 2026 virtual-page submission 'When drift detectors cry wolf' on false-alarm rates with PSI unstable below about 200 samples and Bonferroni lowering power, a wikidocs PSI and KS guide; search snippets only, not opened; WebFetch of evidentlyai.com failed with getaddrinfo ENOTFOUND; sources partly conflict on PSI versus KS sensitivity); vendor docs and one conference submission, not interview reports; MLOps and data science roles
**Say this first (1 line):** PSI bins the reference data, compares the share of data in each bin now versus then, and sums (current% minus reference%) times ln(current% / reference%). A bigger number means a bigger shift, and 0.1 and 0.25 are conventions, not laws.

**Then explain:**
- **Bins:** cut at reference quantiles, so each reference bin holds equal data. Make the first and last edge minus and plus infinity so new out-of-range values are counted.
- **Empty bins:** the log of zero blows up. Clip shares to a small epsilon (I used 1e-4). The value then depends on epsilon, so fix it and keep it.
- **Categoricals:** each category is a bin. A new category (not in the reference) gets the epsilon in the reference share and makes PSI large.
- **Noise floor:** with no real shift PSI is still above zero. A rough floor is (bins minus 1) times (1/n_ref + 1/n_cur). With 10 bins, n_ref 5000, n_cur 100 that is 0.092, and I measured about 0.099 on average. So small current windows give false alarms.
- **Blind spot:** PSI is smeared over bins. A tail-only shift (3 percent of points far out) gave PSI 0.011, which no rule of thumb would flag.
- **Thresholds:** 0.1 and 0.25 come from credit-scoring practice. Calibrate on your own history of normal weeks. Sources disagree on sample-size behaviour (a vendor says PSI is less sample-sensitive than KS; a conference submission reports it is unstable under a few hundred points); my run is on the small-n side.

**Example (hand-checkable):** Shares A/B/C go 50/30/20 to 40/30/30. PSI = (0.4-0.5)·ln(0.4/0.5) + 0 + (0.3-0.2)·ln(0.3/0.2) = 0.0223 + 0.0405 = 0.0629. The code prints the same.

**Code:**
```python
import numpy as np

def psi(ref, cur, bins=10, eps=1e-4):
    edges = np.quantile(ref, np.linspace(0, 1, bins + 1))
    edges[0], edges[-1] = -np.inf, np.inf          # catch values outside the reference range
    r = np.histogram(ref, edges)[0] / len(ref)
    c = np.histogram(cur, edges)[0] / len(cur)
    r, c = np.clip(r, eps, None), np.clip(c, eps, None)   # epsilon for empty bins
    return float(np.sum((c - r) * np.log(c / r)))

def psi_cat(ref, cur, eps=1e-4):
    cats = sorted(set(ref) | set(cur))
    r = np.array([np.mean(np.asarray(ref) == k) for k in cats]).clip(eps)
    c = np.array([np.mean(np.asarray(cur) == k) for k in cats]).clip(eps)
    return float(np.sum((c - r) * np.log(c / r)))

rng = np.random.default_rng(7)
ref = rng.normal(0, 1, 20000)
cases = {
    "no shift":      rng.normal(0, 1, 20000),
    "mean +0.5":     rng.normal(0.5, 1, 20000),
    "variance x1.5": rng.normal(0, 1.5, 20000),
    "tail only":     np.where(rng.random(20000) < 0.03, rng.normal(5, 0.5, 20000), rng.normal(0, 1, 20000)),
}
print("PSI by scenario (10 quantile bins)")
for k, v in cases.items():
    print(f"  {k:<14}", round(psi(ref, v), 4))
print("\nPSI vs number of bins")
print("  bins        " + "".join(f"{b:>8}" for b in (5, 10, 20)))
for k, v in cases.items():
    print(f"  {k:<12}" + "".join(f"{psi(ref, v, b):8.4f}" for b in (5, 10, 20)))

print("\nNo true shift, mean PSI over 200 repeats (10 bins, reference n=5000)")
refs = rng.normal(0, 1, 5000)
for n in (100, 500, 5000, 50000):
    vals = [psi(refs, rng.normal(0, 1, n)) for _ in range(200)]
    print(f"  current n={n:<6} mean={np.mean(vals):.4f}  max={np.max(vals):.4f}")

print("\nCategorical PSI (A/B/C share 50/30/20 -> 40/30/30), with a new category D")
a = ["A"] * 50 + ["B"] * 30 + ["C"] * 20
b = ["A"] * 40 + ["B"] * 30 + ["C"] * 30
d = ["A"] * 40 + ["B"] * 30 + ["C"] * 25 + ["D"] * 5
print("  shares move :", round(psi_cat(a, b), 4))
print("  new category:", round(psi_cat(a, d), 4))
# hand check of the first number
print("  hand check  :", round((0.4-0.5)*np.log(0.4/0.5) + 0 + (0.3-0.2)*np.log(0.3/0.2), 4))
```

**Output (my run):**
```text
PSI by scenario (10 quantile bins)
  no shift       0.0005
  mean +0.5      0.2494
  variance x1.5  0.2029
  tail only      0.0111

PSI vs number of bins
  bins               5      10      20
  no shift      0.0001  0.0005  0.0018
  mean +0.5     0.2297  0.2494  0.2560
  variance x1.5  0.1243  0.2029  0.2494
  tail only     0.0048  0.0111  0.0197

No true shift, mean PSI over 200 repeats (10 bins, reference n=5000)
  current n=100    mean=0.0994  max=0.2922
  current n=500    mean=0.0210  max=0.0514
  current n=5000   mean=0.0033  max=0.0083
  current n=50000  mean=0.0019  max=0.0032

Categorical PSI (A/B/C share 50/30/20 -> 40/30/30), with a new category D
  shares move : 0.0629
  new category: 0.3436
  hand check  : 0.0629
```
Ran with `python3 -I`, numpy 2.5.4, seeded.

**Follow-ups:**
- *Bins 5, 10 or 20?* The value grows with bins (variance x1.5: 0.124, 0.203, 0.249). Pick one, keep it, and set thresholds for that choice.
- *Is PSI symmetric?* Yes, the formula is symmetric in current and reference.
- *Alternative for a tail shift?* A KS test or a quantile check on the 99th percentile.

**Common mistakes:**
- Using equal-width bins on skewed data, so most bins are empty.
- Quoting 0.25 as a standard in the interview.
- Computing PSI on 100 rows a day and paging on it.

---

### Q4 ⭐⭐⭐ 🟡 The Kolmogorov-Smirnov test as a drift detector, and why it screams at large samples. Explain the statistic D, the p-value, why a huge n turns a trivial shift into p < 0.001, and why small n misses real shift. Run scipy ks_2samp for n = 200, 2000 and 200000 on a tiny and a real shift, and propose an alert rule that uses D (effect size) together with the p-value or a minimum-D floor. Say which parts of this are vendor advice and which are statistics.
**Asked at:** MLOps interview question banks and guides (K21Academy '47 MLOps interview questions' PDF, Towards AI '101 ML LLM agentic AIOps interview questions', DataCamp MLOps interview questions, The Interview Guys MLOps post, wecreateproblems.com, hyring.com, dev.to vivekk101, a Medium skphd post; search snippets only, not opened; the Devinterview-io/mlops-interview-questions GitHub page WAS opened and has no dedicated monitoring or drift question, only monitoring bullets inside Q1, Q2, Q4, Q6, Q7 and Q12); editorial question lists, not verified candidate reports; MLOps, ML platform and ML engineer roles at IT-services firms, product companies and GCCs | Drift-test pitfall sources (Evidently blog 'data drift detection on large datasets' saying KS is too sensitive on large data, an Arize docs monitors page saying PSI is less sample-sensitive, an ICLR 2026 virtual-page submission 'When drift detectors cry wolf' on false-alarm rates with PSI unstable below about 200 samples and Bonferroni lowering power, a wikidocs PSI and KS guide; search snippets only, not opened; WebFetch of evidentlyai.com failed with getaddrinfo ENOTFOUND; sources partly conflict on PSI versus KS sensitivity); vendor docs and one conference submission, not interview reports; MLOps and data science roles
**Say this first (1 line):** KS measures the largest gap between two cumulative distributions (D). The p-value only says whether a gap exists, not whether it matters, so with a big n even a trivial shift gets p near zero. Alert on D (size) together with p.

**Then explain:**
- D is between 0 and 1: the largest vertical gap between the two empirical CDFs. It is the effect size.
- The p-value shrinks as n grows. At n = 200000 a 0.02-sd shift (D = 0.010) was already tiny in p. Nobody should act on it.
- The reverse: at n = 200 a real 0.3-sd shift (D = 0.150) gave p = 0.022. Under a strict p < 0.001 rule it is missed. Small n lacks power.
- Alert rule I propose: p below 0.001 and D at or above a floor (0.1 here, an assumption). Tune the floor on history of harmless weeks.
- Also, running many tests means false alarms: 21 of 500 no-shift daily checks fired at p < 0.05 (about 4 percent, near the 5 percent expected by construction). More features means more false alarms, so correct for it or rank by D.
- **Statistics versus advice:** that p falls with n, that D is an effect size and that multiple tests inflate false alarms are statistics. The idea of reporting D beside p is from a vendor blog; specific floors like 0.1 are conventions you calibrate, not facts.

**Example:** n = 200000 per side, 0.02-sd shift. D = 0.010, p is tiny, the naive test fires, and the D-floor rule stays silent. That is the point of the rule.

**Code:**
```python
import numpy as np
from scipy.stats import ks_2samp

rng = np.random.default_rng(3)
print(f"{'shift (sd)':<11}{'n':>8}{'D':>8}{'p':>10}   naive(p<.05) rule(p<.001 and D>=0.1)")
for shift in (0.02, 0.30):
    for n in (200, 2000, 200000):
        a = rng.normal(0, 1, n); b = rng.normal(shift, 1, n)
        r = ks_2samp(a, b)
        naive = r.pvalue < 0.05
        rule = r.pvalue < 0.001 and r.statistic >= 0.1
        print(f"{shift:<11}{n:>8}{r.statistic:8.3f}{r.pvalue:10.4f}   {str(naive):<12} {rule}")

print("\nFalse alarms with no shift: 500 daily checks at p<0.05, n=2000 each")
fa = sum(ks_2samp(rng.normal(0, 1, 2000), rng.normal(0, 1, 2000)).pvalue < 0.05 for _ in range(500))
print("  naive alarms:", fa, "of 500 (about 5 percent is expected by construction)")
```

**Output (my run):**
```text
shift (sd)        n       D         p   naive(p<.05) rule(p<.001 and D>=0.1)
0.02            200   0.060    0.8655   False        False
0.02           2000   0.032    0.2742   False        False
0.02         200000   0.010    0.0000   True         False
0.3             200   0.150    0.0221   True         False
0.3            2000   0.146    0.0000   True         True
0.3          200000   0.119    0.0000   True         True

False alarms with no shift: 500 daily checks at p<0.05, n=2000 each
  naive alarms: 21 of 500 (about 5 percent is expected by construction)
```
Ran with `python3 -I`, scipy 1.18.1, seeded. (p prints 0.0000 when it is below 5e-5.)

**Follow-ups:**
- *Can you fix small n?* Pool several days, or use a bootstrap or a bigger window. Accept slower detection.
- *KS on discrete data?* The p-value is not exact with ties; use chi-square or PSI for categoricals (Q5).
- *Why not just lower the p threshold?* It does not fix the effect-size problem; at n large any shift passes.

**Common mistakes:**
- Treating p < 0.05 as "drift happened and we must retrain".
- Running KS on 500 features and alerting on each one.
- Reading "no alert at n = 200" as "no drift".

---

### Q5 ⭐⭐⭐ 🟡 Which drift test for which feature? Build the decision table for numeric, categorical, binary, high-cardinality categorical, count, text-length and timestamp features: KS, Wasserstein, PSI, chi-square, Jensen-Shannon, and simple rate or mean checks. Explain units and scale (Wasserstein in feature units, JS bounded, chi-square sensitive to n and to small expected counts). Implement a function that picks a test by dtype, run it on a mixed DataFrame with one shifted column of each kind, and print the result table.
**Asked at:** MLOps interview question banks and guides (K21Academy '47 MLOps interview questions' PDF, Towards AI '101 ML LLM agentic AIOps interview questions', DataCamp MLOps interview questions, The Interview Guys MLOps post, wecreateproblems.com, hyring.com, dev.to vivekk101, a Medium skphd post; search snippets only, not opened; the Devinterview-io/mlops-interview-questions GitHub page WAS opened and has no dedicated monitoring or drift question, only monitoring bullets inside Q1, Q2, Q4, Q6, Q7 and Q12); editorial question lists, not verified candidate reports; MLOps, ML platform and ML engineer roles at IT-services firms, product companies and GCCs | Drift-test pitfall sources (Evidently blog 'data drift detection on large datasets' saying KS is too sensitive on large data, an Arize docs monitors page saying PSI is less sample-sensitive, an ICLR 2026 virtual-page submission 'When drift detectors cry wolf' on false-alarm rates with PSI unstable below about 200 samples and Bonferroni lowering power, a wikidocs PSI and KS guide; search snippets only, not opened; WebFetch of evidentlyai.com failed with getaddrinfo ENOTFOUND; sources partly conflict on PSI versus KS sensitivity); vendor docs and one conference submission, not interview reports; MLOps and data science roles
**Say this first (1 line):** Pick the test from the feature type and say what the number means: KS and Wasserstein for numeric, Jensen-Shannon or chi-square for categorical, a rate difference for binary, top-k plus an "other" bucket for high cardinality, and simple freshness and hour-of-day checks for timestamps.

**Then explain:**
| Feature | Test I use | Why | Watch out |
|---|---|---|---|
| Numeric | KS (D, p) plus Wasserstein | D is bounded; Wasserstein is in feature units, so it is easy to explain | divide by the reference sd to compare across features |
| Binary | rate difference, chi-square | one number, easy to read | p alone at big n (Q4) |
| Categorical | Jensen-Shannon (bounded 0 to 1 with base 2), or PSI | symmetric, handles zeros | chi-square is sensitive to n and to small expected counts |
| High-cardinality | JS on top-k plus OTHER | most categories have almost no data | unseen IDs fall in OTHER; also track the new-category rate |
| Count | Wasserstein, or KS with ties noted | discrete and skewed | many ties |
| Text length | numeric tests on the length | cheap proxy for text drift | length hides content change |
| Timestamp | newest-timestamp lag and hour-of-day JS | a raw timestamp always "drifts" as time moves | never run KS on the raw value |
- The thresholds in my function (D 0.1 with p, JS 0.1, W 0.1 sd, lag 6 hours) are my conventions. Calibrate them.
- Failure mode: one global test for every column. A timestamp or an ID column then screams every day.

**Example:** `merchant` has 200 values. Top-10 merchants went from 5 percent to 25 percent of volume in the shifted frame. JS on top-10 plus OTHER shows it; chi-square on 200 mostly-empty cells would be unstable.

**Code:**
```python
import numpy as np, pandas as pd
from scipy.stats import ks_2samp, chi2_contingency, wasserstein_distance
from scipy.spatial.distance import jensenshannon

def kind_of(s, hint=None):
    if hint: return hint
    if pd.api.types.is_datetime64_any_dtype(s): return "timestamp"
    if s.dtype == bool or s.nunique() <= 2: return "binary"
    if s.dtype == object or str(s.dtype) in ("category", "str", "string"):
        return "high_card" if s.nunique() > 20 else "categorical"
    if pd.api.types.is_integer_dtype(s) and s.nunique() <= 30: return "count"
    return "numeric"

def shares(ref, cur, top=10):
    keep = ref.value_counts().index[:top]
    r = ref.where(ref.isin(keep), "OTHER").value_counts(normalize=True)
    c = cur.where(cur.isin(keep), "OTHER").value_counts(normalize=True)
    cats = r.index.union(c.index)
    return r.reindex(cats, fill_value=0).values, c.reindex(cats, fill_value=0).values

def drift(ref, cur, hint=None):
    k = kind_of(ref, hint)
    if k == "numeric":
        ks = ks_2samp(ref, cur)
        w = wasserstein_distance(ref, cur) / ref.std()        # in reference-sd units
        return k, "KS + Wasserstein/sd", f"D={ks.statistic:.3f} W={w:.3f}", ks.pvalue < 0.001 and ks.statistic >= 0.1
    if k == "count":
        w = wasserstein_distance(ref, cur) / ref.std()
        return k, "Wasserstein/sd", f"W={w:.3f}", w >= 0.1
    if k == "binary":
        t = pd.crosstab(np.r_[np.zeros(len(ref)), np.ones(len(cur))], np.r_[ref.astype(int), cur.astype(int)])
        p = chi2_contingency(t)[1]; d = abs(cur.astype(int).mean() - ref.astype(int).mean())
        return k, "rate diff + chi2", f"diff={d:.3f}", p < 0.001 and d >= 0.03
    if k == "categorical":
        r, c = shares(ref, cur)
        js = jensenshannon(r, c, base=2)
        return k, "Jensen-Shannon", f"JS={js:.3f}", js >= 0.1
    if k == "high_card":
        r, c = shares(ref, cur, top=10)
        js = jensenshannon(r, c, base=2)
        return k, "JS on top-10+OTHER", f"JS={js:.3f}", js >= 0.1
    if k == "timestamp":
        hr = lambda s: np.bincount(s.dt.hour, minlength=24) / len(s)
        js = jensenshannon(hr(ref), hr(cur), base=2)
        lag = (ref.max() - cur.max()).total_seconds() / 3600
        return k, "JS hour-of-day + max-lag", f"JS={js:.3f} lag_h={lag:.0f}", js >= 0.1 or abs(lag) >= 6

rng = np.random.default_rng(11); n = 5000
def frame(shift):
    ids = np.array([f"m{i}" for i in range(200)])
    p = np.ones(200) / 200
    if shift: p = np.r_[np.full(10, 0.05), np.full(190, 0.5 / 190)]; p /= p.sum()
    base = pd.Timestamp("2026-01-01")
    return pd.DataFrame({
        "income":    rng.lognormal(10, 0.5, n) * (1.25 if shift else 1.0),
        "channel":   rng.choice(["web", "app", "branch", "call"], n, p=[.2, .4, .2, .2] if shift else [.4, .3, .2, .1]),
        "is_new":    rng.random(n) < (0.5 if shift else 0.3),
        "merchant":  rng.choice(ids, n, p=p),
        "n_txn_7d":  rng.poisson(8 if shift else 5, n),
        "text_len":  rng.normal(120, 30, n).round() + (0 if not shift else 40),
        "event_ts":  base + pd.to_timedelta(rng.integers(0, 24 * 3600 * 7, n) + (3600 * 12 if shift else 0), unit="s")
                     - (pd.Timedelta(hours=30) if shift else pd.Timedelta(0)),
    })
ref, cur = frame(False), frame(True)
hints = {"n_txn_7d": "count", "text_len": "numeric"}
rows = []
for col in ref.columns:
    k, test, stat, flag = drift(ref[col], cur[col], hints.get(col))
    rows.append((col, k, test, stat, "DRIFT" if flag else "ok"))
print(pd.DataFrame(rows, columns=["column", "kind", "test", "statistic", "flag"]).to_string(index=False))
# control: same data compared with a fresh unshifted sample
c0 = frame(False)
print("\ncontrol (no shift) flags:", [bool(drift(ref[c], c0[c], hints.get(c))[3]) for c in ref.columns])
```

**Output (my run):**
```text
  column        kind                     test         statistic  flag
  income     numeric      KS + Wasserstein/sd   D=0.182 W=0.477 DRIFT
 channel categorical           Jensen-Shannon          JS=0.227 DRIFT
  is_new      binary         rate diff + chi2        diff=0.204 DRIFT
merchant   high_card       JS on top-10+OTHER          JS=0.124 DRIFT
n_txn_7d       count           Wasserstein/sd           W=1.332 DRIFT
text_len     numeric      KS + Wasserstein/sd   D=0.491 W=1.329 DRIFT
event_ts   timestamp JS hour-of-day + max-lag JS=0.038 lag_h=18 DRIFT

control (no shift) flags: [False, False, False, False, False, False, False]
```
Ran with `python3 -I`, numpy 2.5.4, scipy 1.18.1, pandas 3.1.0, seeded. The control line compares the reference with a second no-shift sample and flags nothing.

**Follow-ups:**
- *Why not PSI everywhere?* It works, but the bins and epsilon become another thing to tune; per-type tests are easier to explain.
- *Multivariate drift?* Train a classifier to tell reference from current; its AUC is the drift score. Mention only.
- *Text?* Embedding distance is a different topic (Book 2).

**Common mistakes:**
- KS on a categorical encoded as integers.
- Chi-square on a high-cardinality column.
- Drift on timestamps or IDs.

---

### Q6 ⭐⭐⭐ 🟢 Data quality checks for an ML input table: nulls and null-rate change, schema and dtype, ranges and allowed values, uniqueness, freshness, volume, and referential or unit sanity. Say which are cheap per-batch checks and which need a baseline. Implement them in plain pandas and again as a pandera schema (with lazy=True so all failures are reported), run on a good and a corrupted batch, and show both reports. Say where these checks run: ingestion, before training, and at serving.
**Asked at:** MLOps interview question banks and guides (K21Academy '47 MLOps interview questions' PDF, Towards AI '101 ML LLM agentic AIOps interview questions', DataCamp MLOps interview questions, The Interview Guys MLOps post, wecreateproblems.com, hyring.com, dev.to vivekk101, a Medium skphd post; search snippets only, not opened; the Devinterview-io/mlops-interview-questions GitHub page WAS opened and has no dedicated monitoring or drift question, only monitoring bullets inside Q1, Q2, Q4, Q6, Q7 and Q12); editorial question lists, not verified candidate reports; MLOps, ML platform and ML engineer roles at IT-services firms, product companies and GCCs | Data-validation tool comparisons (pandera GitHub discussion 'Great Expectations vs Pandera #598', endjin.com comparison, a conventions page suggesting a freshness check at 2x expected cadence; search snippets only, not opened; nothing found on volume or freshness checks in Great Expectations itself); community comparisons, not interview reports; data and ML engineer roles
**Say this first (1 line):** Data quality checks are cheap rules on every batch: nulls, schema and types, ranges and allowed values, uniqueness, freshness and volume. Some need a baseline from training (null rate, volume), most do not.

**Then explain:**
| Check | Needs baseline? | Example |
|---|---|---|
| Schema, dtype | no | `age` is an integer |
| Range, allowed values | no (or from a data contract) | age 18 to 80, country in IN/US/UK |
| Uniqueness | no | `user_id` unique |
| Null rate | yes, usually | null rate near the training rate |
| Freshness | the expected cadence | newest row under 2 hours old |
| Volume | yes | at least 70 percent of normal rows |
| Referential and unit sanity | rules from the owner | currency code exists, metres not centimetres |
- Where they run: at ingestion (stop bad data early), before training (the veto in Q12) and at serving (cheap row checks only; batch checks run on the logged window).
- pandera is light and lives in code. Great Expectations (GE) is broader with docs and result stores; teams often combine them. Check current docs for both.
- Pandera detail I hit: column checks skip null values by default, so a null-rate check on a nullable column silently passed on my first run until I set `ignore_na=False`.
- Failure mode: a check that is only logged. Decide: block, quarantine, or warn.

**Example:** 1000-row good batch passes. The corrupted batch (400 rows kept) has 150 null incomes (the plain check prints a 0.38 null rate), 5 bad ages, one bad country, a duplicate id, a 9-hour-old feed and only 400 rows. Both implementations report all six problems.

**Code:**
```python
import numpy as np, pandas as pd
import pandera.pandas as pa

NOW = pd.Timestamp("2026-10-26 12:00")
rng = np.random.default_rng(2)

def batch(n=1000, bad=False):
    df = pd.DataFrame({
        "user_id": np.arange(n),
        "age": rng.integers(18, 80, n),
        "income": rng.lognormal(10, 0.4, n),
        "country": rng.choice(["IN", "US", "UK"], n),
        "event_ts": NOW - pd.to_timedelta(rng.integers(0, 3600, n), unit="s"),
    })
    if bad:
        df.loc[:149, "income"] = np.nan                  # 15 percent nulls
        df.loc[10:14, "age"] = [-1, 200, 150, 17, 999]   # out of range
        df.loc[20, "country"] = "XX"                     # not in allowed set
        df.loc[31, "user_id"] = 30                       # duplicate id
        df["event_ts"] = df["event_ts"] - pd.Timedelta(hours=9)   # stale feed
        df = df.iloc[:400]                               # volume drop
    return df

BASE_ROWS, BASE_NULL = 1000, 0.00

def plain_checks(df):
    f = []
    if df["income"].isna().mean() > BASE_NULL + 0.02: f.append(f"null rate income {df['income'].isna().mean():.2f}")
    if not df["age"].between(18, 80).all():           f.append(f"age out of 18-80: {(~df['age'].between(18, 80)).sum()} rows")
    if not df["country"].isin(["IN", "US", "UK"]).all(): f.append(f"bad country values: {sorted(set(df['country']) - {'IN','US','UK'})}")
    if df["user_id"].duplicated().any():              f.append(f"duplicate user_id: {df['user_id'].duplicated().sum()}")
    if (NOW - df["event_ts"].max()) > pd.Timedelta(hours=2): f.append(f"stale: newest row {(NOW - df['event_ts'].max())} old")
    if len(df) < 0.7 * BASE_ROWS:                     f.append(f"volume {len(df)} vs baseline {BASE_ROWS}")
    return f

schema = pa.DataFrameSchema({
    "user_id": pa.Column(int, unique=True),
    "age": pa.Column(int, pa.Check.in_range(18, 80)),
    "income": pa.Column(float, nullable=True, checks=pa.Check(lambda s: s.isna().mean() <= 0.02, element_wise=False, ignore_na=False, error="null rate above 2 percent")),
    "country": pa.Column(str, pa.Check.isin(["IN", "US", "UK"])),
    "event_ts": pa.Column("datetime64[ns]", pa.Check(lambda s: (NOW - s.max()) <= pd.Timedelta(hours=2), error="stale: newest row older than 2h")),
}, checks=pa.Check(lambda d: len(d) >= 0.7 * BASE_ROWS, error="volume below 70 percent of baseline"))

for name, df in (("good", batch()), ("corrupted", batch(bad=True))):
    print(f"--- {name} batch, plain pandas: {plain_checks(df) or 'no failures'}")
    try:
        schema.validate(df, lazy=True)
        print(f"--- {name} batch, pandera: passed")
    except pa.errors.SchemaErrors as e:
        fc = e.failure_cases[["column", "check", "failure_case"]].copy()
        fc["failure_case"] = fc["failure_case"].astype(str).str.slice(0, 28)
        print(f"--- {name} batch, pandera: {len(fc)} failure rows")
        print(fc.head(12).to_string(index=False))
```

**Output (my run):**
```text
--- good batch, plain pandas: no failures
--- good batch, pandera: passed
--- corrupted batch, plain pandas: ['null rate income 0.38', 'age out of 18-80: 5 rows', "bad country values: ['XX']", 'duplicate user_id: 1', 'stale: newest row 0 days 09:00:17 old', 'volume 400 vs baseline 1000']
--- corrupted batch, pandera: 11 failure rows
  column                               check failure_case
     NaN volume below 70 percent of baseline        False
 user_id                    field_uniqueness           30
 user_id                    field_uniqueness           30
     age                    in_range(18, 80)           -1
     age                    in_range(18, 80)          200
     age                    in_range(18, 80)          150
     age                    in_range(18, 80)           17
     age                    in_range(18, 80)          999
 country            isin(['IN', 'US', 'UK'])           XX
  income           null rate above 2 percent        False
event_ts     stale: newest row older than 2h        False
```
Ran with `python3 -I` in a venv with pandas 3.1.0, numpy 2.5.4 and pandera 0.35.0 (installed as pandera[pandas]); seeded. With `lazy=True` pandera collects all failures, not just the first. Great Expectations: I did not run it for this question.

**Follow-ups:**
- *Block or warn?* Block for schema and unit errors; warn for small null-rate moves.
- *Who owns the contract?* The data producer, with ML as a consumer that writes down its needs.
- *Volume check on a holiday?* Compare with the same weekday, not yesterday.

**Common mistakes:**
- Checking only the schema, not the values.
- No freshness check, so a dead upstream job looks like "no drift".
- Fixed null thresholds that nobody revisits.

---

### Q7 ⭐⭐⭐ 🟡 Training-serving skew: what it is, the usual causes (different preprocessing code, a feature computed from different sources or with different time windows, unit or encoding changes, missing values handled differently, stale lookups), and how to detect it. Simulate a model trained on a feature in metres and served in centimetres plus a categorical encoding mismatch, log serving features, compare with training, and show the check that catches each. Give the structural fixes (one shared transform, logged features reused for training, parity tests). Part 9 owns feature stores, so mention them only as one fix.
**Asked at:** MLOps interview question banks and guides (K21Academy '47 MLOps interview questions' PDF, Towards AI '101 ML LLM agentic AIOps interview questions', DataCamp MLOps interview questions, The Interview Guys MLOps post, wecreateproblems.com, hyring.com, dev.to vivekk101, a Medium skphd post; search snippets only, not opened; the Devinterview-io/mlops-interview-questions GitHub page WAS opened and has no dedicated monitoring or drift question, only monitoring bullets inside Q1, Q2, Q4, Q6, Q7 and Q12); editorial question lists, not verified candidate reports; MLOps, ML platform and ML engineer roles at IT-services firms, product companies and GCCs | Scenario question write-ups (a Glassdoor EPAM Systems interview page whose snippet lists 'why does production differ from training' with feature, preprocessing and version mismatch as causes, and an end-to-end design prompt; one candidate's review, search snippet only, not opened, unverified; The Interview Guys post saying drift is asked in almost every MLOps interview, snippet only); anecdotal, not company-verified reports; MLOps and ML engineer roles
**Say this first (1 line):** Training-serving skew is when the same raw data becomes different features in training and in serving, because of different code, units, encodings, windows or missing-value handling. It is a bug, and the fix is one shared transform plus parity tests.

**Then explain:**
- Common causes: two code paths (notebook versus service), a unit change, categories encoded in a different order, nulls filled differently, a feature computed over a different time window, stale lookups.
- Detect it three ways: compare logged serving features with training features; replay the same raw rows through both paths (parity test); check categorical code mappings are equal.
- Structural fixes: one transform package used by both paths; log the served features and train on those logs; run parity tests in CI (Part 7); a feature store is one way to enforce this (Part 9 owns it).
- Failure mode: treating it as drift and retraining. The new model learns the bug.

**Example:** Height trained in metres (mean 1.70), served in centimetres (mean 170). Plan encoded as basic=0, plus=1, pro=2 in training but pro=0, plus=1, basic=2 in serving. Accuracy fell from 0.702 to 0.470, which is worse than a coin flip, because the encoding reversal flips the sign of the plan effect.

**Code:**
```python
import numpy as np
from scipy.stats import ks_2samp
from sklearn.linear_model import LogisticRegression

rng = np.random.default_rng(5)
n = 10000
PLANS = ["basic", "plus", "pro"]
# raw rows
height_m = rng.normal(1.7, 0.1, n)
plan = rng.choice(PLANS, n, p=[.5, .3, .2])
y = (rng.random(n) < 1 / (1 + np.exp(-(8 * (height_m - 1.7) + (plan == "pro") * 1.5 - (plan == "basic") * 0.8)))).astype(int)

def train_transform(h, p):          # training code: metres, plan codes by position in PLANS
    return np.c_[h, [PLANS.index(x) for x in p]]
def serve_transform(h, p):          # serving code, written separately: centimetres, codes by sorted() order
    order = sorted(PLANS)           # a different convention: codes assigned from the reversed sorted list
    return np.c_[h * 100, [order[::-1].index(x) for x in p]]

Xtr = train_transform(height_m, plan)
m = LogisticRegression(max_iter=1000).fit(Xtr, y)
h2 = rng.normal(1.7, 0.1, n); p2 = rng.choice(PLANS, n, p=[.5, .3, .2])
y2 = (rng.random(n) < 1 / (1 + np.exp(-(8 * (h2 - 1.7) + (p2 == "pro") * 1.5 - (p2 == "basic") * 0.8)))).astype(int)
good, bad = train_transform(h2, p2), serve_transform(h2, p2)
print("accuracy, correct pipeline:", round(m.score(good, y2), 3))
print("accuracy, skewed pipeline :", round(m.score(bad, y2), 3))

print("\nCheck 1: compare logged serving features with training features")
for j, name in enumerate(["height", "plan_code"]):
    d = ks_2samp(Xtr[:, j], bad[:, j]).statistic
    print(f"  {name:<10} train mean={Xtr[:, j].mean():8.2f}  serve mean={bad[:, j].mean():8.2f}  KS D={d:.3f}  ratio={bad[:, j].mean() / Xtr[:, j].mean():.2f}")
print("\nCheck 2: parity test, same raw rows through both code paths")
a, b = train_transform(h2[:5], p2[:5]), serve_transform(h2[:5], p2[:5])
print("  max abs diff per column:", np.abs(a - b).max(axis=0).round(2).tolist(), "(expect 0, 0)")
print("\nCheck 3: categorical code mapping must be identical")
print("  train mapping:", {p: PLANS.index(p) for p in PLANS})
print("  serve mapping:", {p: sorted(PLANS)[::-1].index(p) for p in PLANS})
```

**Output (my run):**
```text
accuracy, correct pipeline: 0.702
accuracy, skewed pipeline : 0.47

Check 1: compare logged serving features with training features
  height     train mean=    1.70  serve mean=  170.05  KS D=1.000  ratio=99.90
  plan_code  train mean=    0.70  serve mean=    1.30  KS D=0.305  ratio=1.85

Check 2: parity test, same raw rows through both code paths
  max abs diff per column: [178.7, 2.0] (expect 0, 0)

Check 3: categorical code mapping must be identical
  train mapping: {'basic': 0, 'plus': 1, 'pro': 2}
  serve mapping: {'basic': 2, 'plus': 1, 'pro': 0}
```
Ran with `python3 -I`, numpy 2.5.4, scipy 1.18.1, scikit-learn 1.9.1, seeded.

How each check helped: the mean ratio (99.9) names the unit error; KS D = 1.000 says "no overlap at all", not a gentle drift; the parity test shows a nonzero difference on identical raw rows (expected 0, 0); the mapping print shows the reversed codes.

**Follow-ups:**
- *Why not just retrain on serving data?* Only after you fix the transform; otherwise the labels and features were built differently.
- *Time-window skew?* Compute the offline feature "as of" the prediction time (point-in-time correct), not the latest value.
- *Cheapest guard?* Log features at serving and compare summaries with training daily.

**Common mistakes:**
- Re-implementing preprocessing in a second language.
- Checking only means; also check categories and null rates.
- Skipping the parity test because "the unit tests pass".

---

### Q8 ⭐⭐⭐ 🟡 Monitoring performance when labels arrive late or never. Explain label delay (days for fraud chargebacks, months for loan default) and the toolbox: input and prediction drift as early warning, proxy metrics, a labelled canary or audit sample, delayed true performance on matured cohorts, and estimated performance from calibrated probabilities. Simulate predictions with a 30-day label lag, join labels when they arrive, and show the rolling matured-cohort accuracy against what you would have seen by prediction date. Say what you can and cannot claim in the meantime.
**Asked at:** MLOps interview question banks and guides (K21Academy '47 MLOps interview questions' PDF, Towards AI '101 ML LLM agentic AIOps interview questions', DataCamp MLOps interview questions, The Interview Guys MLOps post, wecreateproblems.com, hyring.com, dev.to vivekk101, a Medium skphd post; search snippets only, not opened; the Devinterview-io/mlops-interview-questions GitHub page WAS opened and has no dedicated monitoring or drift question, only monitoring bullets inside Q1, Q2, Q4, Q6, Q7 and Q12); editorial question lists, not verified candidate reports; MLOps, ML platform and ML engineer roles at IT-services firms, product companies and GCCs | Label-delay and estimation sources (NannyML blog 'machine learning monitoring workflow' on delayed or absent targets, CBPE and DLE, and warning that drift alerts alone can flood a team; arXiv 'Monitoring Machine Learning Systems: A Multivocal Literature Review' 2509.14294; arXiv 2403.16795 interview study 'We have no idea how models will behave in production until production' reporting alert fatigue from false positives; search snippets only, not opened); vendor blog and academic papers, not interview reports; ML engineer and MLOps roles
**Say this first (1 line):** When labels are late, I use inputs and score drift as an early warning, a labelled audit sample for a quick read, and performance on matured cohorts as the real number, and I say clearly that the newest weeks are unverified.

**Then explain:**
- Toolbox: input and prediction drift (Q10); proxy metrics (for example the share of cases that later get escalated); a small labelled audit sample; matured-cohort metrics (only predictions whose label has arrived); estimated performance from calibrated probabilities.
- Matured-cohort accuracy is honest but old. With a 30-day lag it describes predictions from over a month ago.
- Score-based estimates assume the model is still calibrated. That holds for covariate shift and fails for concept drift (see my run: estimate stays 0.77 while truth is 0.51).
- What I can claim in the meantime: "inputs and scores look stable; performance is unverified for the last 30 days". I cannot claim "the model is fine".
- Failure mode: joining labels to the prediction date and reporting a rolling number that silently mixes complete and incomplete cohorts.

**Example:** The world changes on day 60. On day 89 the matured weekly accuracy is still 0.795. The drop only shows on day 91, 31 days after the change, while true accuracy had been about 0.52 for a month.

**Code:**
```python
import numpy as np

rng = np.random.default_rng(21)
DAYS, PER_DAY, LAG, DRIFT_DAY = 120, 300, 30, 60
day = np.repeat(np.arange(DAYS), PER_DAY)
# model confidence and truth: before DRIFT_DAY the model is calibrated; after, labels flip more often
conf = rng.uniform(0.6, 0.95, len(day))                 # model's stated probability of being right
p_right = np.where(day < DRIFT_DAY, conf, conf - 0.25)   # real accuracy drops after the world changes
correct = rng.random(len(day)) < p_right
label_arrives = day + LAG

print("prediction-day accuracy (truth, nobody can see this yet) vs what is visible")
print(f"{'seen on day':>11} {'true acc, last 7 pred days':>27} {'matured acc (labels in hand)':>30} {'score-based estimate':>21}")
for t in (50, 70, 85, 89, 95, 110, 119):
    recent = (day > t - 7) & (day <= t)
    true_acc = correct[recent].mean()
    mature = (label_arrives <= t) & (day > t - LAG - 7)           # last 7 days of matured predictions
    mat = correct[mature].mean()
    est = conf[recent].mean()                                      # expected accuracy if calibrated
    print(f"{t:>11} {true_acc:27.3f} {mat:30.3f} {est:21.3f}")
# first day the matured weekly accuracy is clearly below the pre-drift level
base = correct[day < DRIFT_DAY].mean()
for t in range(DRIFT_DAY, DAYS):
    mature = (label_arrives <= t) & (day > t - LAG - 7)
    if mature.sum() and correct[mature].mean() < base - 0.05:
        print(f"\nbaseline acc {base:.3f}; drift began day {DRIFT_DAY}; matured accuracy first shows a 5-point drop on day {t} (lag {t - DRIFT_DAY} days)")
        break
```

**Output (my run):**
```text
prediction-day accuracy (truth, nobody can see this yet) vs what is visible
seen on day  true acc, last 7 pred days   matured acc (labels in hand)  score-based estimate
         50                       0.766                          0.772                 0.774
         70                       0.509                          0.775                 0.774
         85                       0.528                          0.788                 0.775
         89                       0.516                          0.795                 0.777
         95                       0.511                          0.555                 0.778
        110                       0.523                          0.518                 0.774
        119                       0.543                          0.516                 0.777

baseline acc 0.781; drift began day 60; matured accuracy first shows a 5-point drop on day 91 (lag 31 days)
```
Ran with `python3 -I`, numpy 2.5.4, seeded. All data are simulated: 300 predictions per day, label lag 30 days, the model's accuracy drops by 0.25 after day 60.

**Follow-ups:**
- *How do you shorten the blind spot?* Label a random sample of recent predictions early (audit), at a cost.
- *When is the score-based estimate safe?* Only when you believe the relationship P(y|x) is stable.
- *Which cohort to report?* The latest fully matured one, labelled with its date range.

**Common mistakes:**
- Reporting accuracy on whatever labels exist today (selection bias: easy cases mature first).
- Saying "no alerts, so no problem" during the lag.
- Using a delayed metric as the only alarm.

---

### Q9 ⭐⭐⭐ 🟡 Detecting concept drift. Why feature drift tests cannot see P(y|x) change; what you monitor instead (rolling metric on matured labels, error-rate and calibration trend, residual patterns, a window comparison on the performance metric). Simulate a sudden and a gradual concept change where input features stay identical, show the KS test on features stays quiet while rolling AUC falls, and implement a simple detector on the error stream. Say how long detection takes with a label lag.
**Asked at:** MLOps interview question banks and guides (K21Academy '47 MLOps interview questions' PDF, Towards AI '101 ML LLM agentic AIOps interview questions', DataCamp MLOps interview questions, The Interview Guys MLOps post, wecreateproblems.com, hyring.com, dev.to vivekk101, a Medium skphd post; search snippets only, not opened; the Devinterview-io/mlops-interview-questions GitHub page WAS opened and has no dedicated monitoring or drift question, only monitoring bullets inside Q1, Q2, Q4, Q6, Q7 and Q12); editorial question lists, not verified candidate reports; MLOps, ML platform and ML engineer roles at IT-services firms, product companies and GCCs | Label-delay and estimation sources (NannyML blog 'machine learning monitoring workflow' on delayed or absent targets, CBPE and DLE, and warning that drift alerts alone can flood a team; arXiv 'Monitoring Machine Learning Systems: A Multivocal Literature Review' 2509.14294; arXiv 2403.16795 interview study 'We have no idea how models will behave in production until production' reporting alert fatigue from false positives; search snippets only, not opened); vendor blog and academic papers, not interview reports; ML engineer and MLOps roles
**Say this first (1 line):** Concept drift is a change in P(y|x), so feature tests cannot see it. I watch error-based signals: rolling metric on matured labels, error rate and calibration trend, plus a change detector on the error stream. Detection is only as fast as the labels.

**Then explain:**
- If the inputs are the same, any test on inputs stays quiet. In my run KS on both features after the change gave D 0.012 and 0.017 with p 0.44 and 0.10.
- Rolling AUC on matured labels is clear: 0.969 before, 0.357 after a sudden flip (below 0.5 means the rule inverted).
- Error-stream detector: Page-Hinkley adds up how far errors exceed a baseline error rate (minus an allowance) and fires when the running sum rises far above its minimum. My settings (baseline from first 10 days, allowance 0.02, limit 20) were hand-picked for this simulation; tune them on history and test the false-alarm rate.
- Gradual drift is slower to detect: here day 55 versus day 50 for the sudden change, and the early rolling AUC (0.673) is only a partial drop.
- Delay: detector delay plus label lag. With a 30-day lag the sudden change is known on day 80 and the gradual one on day 85.
- Failure mode: a detector tuned to catch gradual drift fires on every weekly seasonality.

**Example:** A spam model: attackers change wording, features like length look the same, the error rate climbs. Rolling AUC on reviewed samples falls first.

**Code:**
```python
import numpy as np
from scipy.stats import ks_2samp
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

rng = np.random.default_rng(9)
PER_DAY, DAYS, LAG, T0 = 200, 100, 30, 50
N = PER_DAY * DAYS
X = rng.normal(0, 1, (N, 2))                       # inputs never change
day = np.arange(N) // PER_DAY
def labels(w1, w2):
    z = X[:, 0] * w1 + X[:, 1] * w2
    return z + rng.normal(0, 0.7, N)
base = labels(2.0, 1.0)
sudden = np.where(day >= T0, labels(-1.0, 1.0), base)             # rule flips at day 50
alpha = np.clip((day - T0) / 30, 0, 1)                            # gradual: blend over 30 days
gradual = np.where(rng.random(N) < alpha, labels(-1.0, 1.0), base)
pre = day < T0
model = LogisticRegression().fit(X[pre], (base[pre] > 0).astype(int))
score = model.decision_function(X)

def page_hinkley(err, base, delta=0.02, lam=20.0):
    cum, ph_min = 0.0, 0.0
    for i, e in enumerate(err):
        cum += e - base - delta          # error above the baseline error rate, minus a small allowance
        ph_min = min(ph_min, cum)
        if cum - ph_min > lam: return i
    return None

for name, y in (("sudden", (sudden > 0).astype(int)), ("gradual", (gradual > 0).astype(int))):
    print(f"== {name} concept change starting day {T0}")
    ks_pre = ks_2samp(X[pre][:, 0], X[~pre][:, 0]); ks_pre2 = ks_2samp(X[pre][:, 1], X[~pre][:, 1])
    print(f"  feature KS before vs after: x0 D={ks_pre.statistic:.3f} p={ks_pre.pvalue:.2f} | x1 D={ks_pre2.statistic:.3f} p={ks_pre2.pvalue:.2f}  (quiet)")
    for a, b in ((10, 20), (40, 50), (60, 70), (80, 90)):
        s = (day >= a) & (day < b)
        print(f"  AUC days {a:>2}-{b:<2}: {roc_auc_score(y[s], score[s]):.3f}", end="")
    print()
    err = (model.predict(X) != y).astype(float)
    # detector sees errors only in the order labels arrive (day + LAG); order is the same as prediction order
    warm = 10 * PER_DAY                              # first 10 days set the baseline error rate
    i = warm + page_hinkley(err[warm:], err[:warm].mean())
    d = i // PER_DAY
    print(f"  Page-Hinkley fires at sample {i} = prediction day {d} -> detection delay {d - T0} days of data; with {LAG}-day label lag you learn on day {d + LAG}")
```

**Output (my run):**
```text
== sudden concept change starting day 50
  feature KS before vs after: x0 D=0.012 p=0.44 | x1 D=0.017 p=0.10  (quiet)
  AUC days 10-20: 0.975  AUC days 40-50: 0.969  AUC days 60-70: 0.357  AUC days 80-90: 0.386
  Page-Hinkley fires at sample 10045 = prediction day 50 -> detection delay 0 days of data; with 30-day label lag you learn on day 80
== gradual concept change starting day 50
  feature KS before vs after: x0 D=0.012 p=0.44 | x1 D=0.017 p=0.10  (quiet)
  AUC days 10-20: 0.975  AUC days 40-50: 0.969  AUC days 60-70: 0.673  AUC days 80-90: 0.377
  Page-Hinkley fires at sample 11165 = prediction day 55 -> detection delay 5 days of data; with 30-day label lag you learn on day 85
```
Ran with `python3 -I`, numpy 2.5.4, scipy 1.18.1, scikit-learn 1.9.1, seeded. The detector here runs in prediction order, as if labels were instant; the label lag is added on top.

**Follow-ups:**
- *Is retraining the fix?* Usually, on data after the change; first check it is not a labelling change.
- *Other detectors?* DDM, ADWIN. I would name them, not claim I ran them; the library alibi-detect did not install here.
- *Cheaper proxy?* Calibration check on the labelled audit sample.

**Common mistakes:**
- Using feature drift as the concept drift alarm.
- Forgetting the label lag in the detection time.
- One fixed threshold for sudden and gradual change.

---

### Q10 ⭐⭐⭐ 🟡 Monitoring the prediction (score) distribution. Why it is the first cheap signal when labels lag: score histogram, mean and quantiles, positive rate at the production threshold, confidence or entropy, calibration where labels exist. Explain what a shift in scores does and does not mean (input drift, a bug, a real prevalence change, a threshold or model change). Simulate three events, a feature outage, a prevalence rise and a model swap, run PSI and the positive-rate check on the scores, and show how to tell them apart with a second signal.
**Asked at:** MLOps interview question banks and guides (K21Academy '47 MLOps interview questions' PDF, Towards AI '101 ML LLM agentic AIOps interview questions', DataCamp MLOps interview questions, The Interview Guys MLOps post, wecreateproblems.com, hyring.com, dev.to vivekk101, a Medium skphd post; search snippets only, not opened; the Devinterview-io/mlops-interview-questions GitHub page WAS opened and has no dedicated monitoring or drift question, only monitoring bullets inside Q1, Q2, Q4, Q6, Q7 and Q12); editorial question lists, not verified candidate reports; MLOps, ML platform and ML engineer roles at IT-services firms, product companies and GCCs | Scenario question write-ups (a Glassdoor EPAM Systems interview page whose snippet lists 'why does production differ from training' with feature, preprocessing and version mismatch as causes, and an end-to-end design prompt; one candidate's review, search snippet only, not opened, unverified; The Interview Guys post saying drift is asked in almost every MLOps interview, snippet only); anecdotal, not company-verified reports; MLOps and ML engineer roles
**Say this first (1 line):** The score distribution is the first cheap signal when labels are late, but a shift only says "something changed". I confirm the cause with a second signal: feature drift, a replay of the old model on today's inputs, and the model version tag.

**Then explain:**
- What to track: score histogram, mean and quantiles, positive rate at the production threshold, confidence or entropy, and calibration where labels exist.
- A score shift can mean input drift, a bug or outage, a real prevalence change, or a changed threshold or model.
- Separate them: (1) per-feature drift names an outage; (2) replaying the old model on today's inputs shows whether the inputs moved; (3) the model version tag shows a swap.
- Failure mode: a stable score does not mean stable performance (concept drift keeps scores the same).

| Event | Score PSI | Positive rate | Max feature PSI | Replay of v1 on live inputs | Model tag | Read |
|---|---|---|---|---|---|---|
| none | 0.001 | 0.198 | 0.002 | 0.001 | v1 | baseline |
| A feature outage | 0.411 | 0.078 | 8.283 | 0.411 | v1 | one feature gone |
| B prevalence rise | 0.083 | 0.299 | 0.057 | 0.083 | v1 | inputs moved a little; confirm with labels |
| C model swap | 0.271 | 0.375 | 0.002 | 0.001 | v2 | model changed, inputs same |

**Example:** Positive rate jumps from 0.198 to 0.375 with no input drift and a new version tag: it is the new model, not the world. Rolling back would confirm.

**Code:**
```python
import numpy as np
from sklearn.linear_model import LogisticRegression

rng = np.random.default_rng(4)

def psi(ref, cur, bins=10, eps=1e-4):
    e = np.quantile(ref, np.linspace(0, 1, bins + 1)); e[0], e[-1] = -np.inf, np.inf
    r = np.clip(np.histogram(ref, e)[0] / len(ref), eps, None)
    c = np.clip(np.histogram(cur, e)[0] / len(cur), eps, None)
    return float(np.sum((c - r) * np.log(c / r)))

def make(n):
    X = rng.normal(0, 1, (n, 3))
    p = 1 / (1 + np.exp(-(1.5 * X[:, 0] + 1.0 * X[:, 1] + 0.5 * X[:, 2] - 1.6)))
    return X, (rng.random(n) < p).astype(int)

Xtr, ytr = make(30000)
v1 = LogisticRegression().fit(Xtr, ytr)
v2 = LogisticRegression(class_weight="balanced").fit(Xtr, ytr)       # the "new model" in event C
Xref, yref = make(20000)
ref_score = v1.predict_proba(Xref)[:, 1]
print(f"reference: positive rate at 0.5 = {(ref_score >= 0.5).mean():.3f}, true prevalence = {yref.mean():.3f}")

Xn, yn = make(20000)
Xa = Xn.copy(); Xa[:, 0] = 0.0                                        # A: feature 0 outage, filled with 0
Xp, yp = make(80000)
keep = (yp == 1) | (rng.random(len(yp)) < 0.35)                       # B: positives become more common
Xb = Xp[keep][:20000]
events = {
    "no event":            dict(X=Xn, live=v1.predict_proba(Xn)[:, 1], tag="v1"),
    "A feature outage":    dict(X=Xa, live=v1.predict_proba(Xa)[:, 1], tag="v1"),
    "B prevalence rise":   dict(X=Xb, live=v1.predict_proba(Xb)[:, 1], tag="v1"),
    "C model swap to v2":  dict(X=Xn, live=v2.predict_proba(Xn)[:, 1], tag="v2"),
}
print(f"{'event':<20}{'score PSI':>10}{'pos rate':>10}{'max feat PSI':>14}{'replay-v1 PSI':>15}{'model tag':>11}")
for name, e in events.items():
    s_psi = psi(ref_score, e["live"])
    pos = (e["live"] >= 0.5).mean()
    f_psi = max(psi(Xref[:, j], e["X"][:, j]) for j in range(3))
    replay = psi(ref_score, v1.predict_proba(e["X"])[:, 1])     # old model on today's inputs
    print(f"{name:<20}{s_psi:10.3f}{pos:10.3f}{f_psi:14.3f}{replay:15.3f}{e['tag']:>11}")
```

**Output (my run):**
```text
reference: positive rate at 0.5 = 0.197, true prevalence = 0.262
event                score PSI  pos rate  max feat PSI  replay-v1 PSI  model tag
no event                 0.001     0.198         0.002          0.001         v1
A feature outage         0.411     0.078         8.283          0.411         v1
B prevalence rise        0.083     0.299         0.057          0.083         v1
C model swap to v2       0.271     0.375         0.002          0.001         v2
```
Ran with `python3 -I`, numpy 2.5.4, scikit-learn 1.9.1, seeded. Feature PSI 8.283 is huge because the outage feature becomes constant and empty bins use epsilon; read it as "broken", not as a size.

**Follow-ups:**
- *Why a positive rate and not just PSI?* It is tied to the decision and the business cost.
- *Prevalence rise: real or bug?* Check the labelled audit sample and segments; wait for matured labels.
- *Set the threshold by?* Cost of the two error types, not by the reference positive rate.

**Common mistakes:**
- Alerting on the score shift with no way to diagnose it.
- Ignoring the model version in the dashboard.
- Reading "score unchanged" as "model fine".

---

### Q11 ⭐⭐⭐ 🟡 Alerting design for ML monitoring. Cover static thresholds versus baselines, alert on a sustained condition (a for-duration or N-of-M windows) rather than one point, hysteresis, severity (page versus ticket versus dashboard), grouping, and what makes alert fatigue. Implement an alert evaluator with a persistence rule and hysteresis, run it on a simulated noisy drift-score series with one real shift, and compare the number of alerts for a naive threshold and the designed rule.
**Asked at:** MLOps interview question banks and guides (K21Academy '47 MLOps interview questions' PDF, Towards AI '101 ML LLM agentic AIOps interview questions', DataCamp MLOps interview questions, The Interview Guys MLOps post, wecreateproblems.com, hyring.com, dev.to vivekk101, a Medium skphd post; search snippets only, not opened; the Devinterview-io/mlops-interview-questions GitHub page WAS opened and has no dedicated monitoring or drift question, only monitoring bullets inside Q1, Q2, Q4, Q6, Q7 and Q12); editorial question lists, not verified candidate reports; MLOps, ML platform and ML engineer roles at IT-services firms, product companies and GCCs | Alerting and SLO sources (Google SRE Workbook chapter 'Alerting on SLOs' on burn-rate and multiwindow alerts, Datadog burn-rate docs, openobserve alert-fatigue post; search snippets only, not opened, sre.google WebFetch failed with getaddrinfo ENOTFOUND); SRE docs, not ML-specific and not interview reports; MLOps, SRE and platform roles; no source found on SLOs defined for ML models, so the ML mapping is an expert extension | Label-delay and estimation sources (NannyML blog 'machine learning monitoring workflow' on delayed or absent targets, CBPE and DLE, and warning that drift alerts alone can flood a team; arXiv 'Monitoring Machine Learning Systems: A Multivocal Literature Review' 2509.14294; arXiv 2403.16795 interview study 'We have no idea how models will behave in production until production' reporting alert fatigue from false positives; search snippets only, not opened); vendor blog and academic papers, not interview reports; ML engineer and MLOps roles
**Say this first (1 line):** I alert on a sustained condition with a way to clear it, not on a single point: N-of-M breaches to fire, a lower threshold to resolve (hysteresis), a severity per alert and grouping, so one real shift becomes one incident.

**Then explain:**
- **Threshold type:** static limits for hard rules (null rate, freshness); baseline-relative limits for drift (compare with a normal week), since "normal" differs per feature.
- **Persistence:** fire only if the condition holds for a duration (Prometheus `for:`) or in N of the last M windows. One noisy point should not page.
- **Hysteresis:** fire above 0.15, resolve only after 5 points below 0.10. Without it the alert flaps around the line.
- **Severity:** page for harm now (feed dead, positive rate collapsed), ticket for drift that needs a look, dashboard only for the rest. Every alert links a runbook.
- **Alert fatigue:** many false or duplicate alerts teach people to mute. Silenced alerts are worse than none.
- **Cost:** persistence delays detection by the window. Here the designed rule fired one point after the naive rule.

**Example:** Drift score noisy around 0.06, 8 one-off spikes before t=120, a real shift at t=120. Naive threshold: 74 points above the line (8 before the shift, 66 during it). Designed rule: 1 alert at t=121, 0 false alerts.

**Code:**
```python
import numpy as np, yaml

rng = np.random.default_rng(12)
T = 200
score = 0.06 + rng.normal(0, 0.03, T).clip(-0.05)           # daily drift score, noisy baseline
for i in rng.choice(np.arange(0, 120), 8, replace=False): score[i] += 0.14   # 8 one-off spikes
score[120:] += 0.12                                         # the real, sustained shift starts at t=120

HI, LO = 0.15, 0.10

def naive(s):
    return [i for i, v in enumerate(s) if v > HI]            # one alert per breaching point

def designed(s, n=3, m=4, clear_after=5):
    """fire when n of the last m points breach HI; resolve only after clear_after points below LO"""
    firing, alerts, below = False, [], 0
    for i in range(len(s)):
        window = s[max(0, i - m + 1): i + 1]
        if not firing:
            if sum(v > HI for v in window) >= n: firing = True; alerts.append(i); below = 0
        else:
            below = below + 1 if s[i] < LO else 0
            if below >= clear_after: firing = False
    return alerts

na, de = naive(score), designed(score)
print("points above threshold (naive alerts):", len(na), "| first 10 at t =", na[:10])
print("designed-rule alerts:", len(de), "| fired at t =", de)
print("real shift starts t=120; naive first alert at/after 120:", min(i for i in na if i >= 120),
      "| designed first alert at/after 120:", min(i for i in de if i >= 120))
print("false alerts before t=120: naive", sum(i < 120 for i in na), "| designed", sum(i < 120 for i in de))

RULE = """
groups:
- name: ml-drift
  rules:
  - alert: FeatureDriftSustained
    expr: max(model_feature_drift_score{model="churn"}) > 0.15
    for: 30m
    labels: {severity: ticket}
    annotations: {summary: "Drift score above 0.15 for 30m", runbook: "https://wiki.example/runbooks/drift"}
  - alert: PositiveRateCollapse
    expr: abs(model_positive_rate{model="churn"} - model_positive_rate_baseline) > 0.1
    for: 15m
    labels: {severity: page}
    annotations: {summary: "Positive rate moved more than 0.1 for 15m"}
"""
doc = yaml.safe_load(RULE)
for r in doc["groups"][0]["rules"]:
    assert {"alert", "expr", "for", "labels"} <= set(r), r
    assert r["labels"]["severity"] in {"page", "ticket"}
print("alert-rule YAML parsed; rules checked:", [r["alert"] for r in doc["groups"][0]["rules"]], "(promtool not installed, not executed)")
```

**Output (my run):**
```text
points above threshold (naive alerts): 74 | first 10 at t = [3, 28, 50, 54, 58, 59, 102, 119, 120, 121]
designed-rule alerts: 1 | fired at t = [121]
real shift starts t=120; naive first alert at/after 120: 120 | designed first alert at/after 120: 121
false alerts before t=120: naive 8 | designed 0
alert-rule YAML parsed; rules checked: ['FeatureDriftSustained', 'PositiveRateCollapse'] (promtool not installed, not executed)
```
Ran with `python3 -I`, numpy 2.5.4, PyYAML 6.0.3, seeded. The Prometheus-style rules are **not executed**: promtool, Prometheus and Alertmanager are not installed here. The validation that did run is a pyyaml parse plus a structural check that each rule has `alert`, `expr`, `for` and `labels` with an allowed severity. Metric names (`model_feature_drift_score` and so on) are examples; the `for:` behaviour and any N-of-M or hysteresis pattern need checking in current Prometheus docs.

**Follow-ups:**
- *Why not average over the window?* One extreme point can hide in an average; N-of-M is easier to explain.
- *Burn-rate alerting?* The SRE idea of alerting on the speed of error-budget use with two windows carries over to model SLOs (my mapping, not a standard).
- *Duplicates across 200 features?* Group by model and send one summary with the top features.

**Common mistakes:**
- Paging on each feature's drift test.
- No resolve condition, so alerts flap.
- Setting thresholds once and never reviewing the false-alarm count.

---

### Q12 ⭐⭐⭐ 🟡 Retraining triggers and policy: scheduled, data-volume, drift-triggered, performance-triggered and hybrid. Say what each costs, what can go wrong (retraining on corrupted data, retrain loops, trigger flapping) and the guardrails (data quality gate before training, minimum interval, evaluation against the champion before promotion, a human approval for high-risk models). Write a retraining-decision function with cooldown and a data-quality veto, run it on a simulated month of signals, and show the decisions. Part 5 owns the pipeline mechanics and Part 7 the CI gates.
**Asked at:** MLOps interview question banks and guides (K21Academy '47 MLOps interview questions' PDF, Towards AI '101 ML LLM agentic AIOps interview questions', DataCamp MLOps interview questions, The Interview Guys MLOps post, wecreateproblems.com, hyring.com, dev.to vivekk101, a Medium skphd post; search snippets only, not opened; the Devinterview-io/mlops-interview-questions GitHub page WAS opened and has no dedicated monitoring or drift question, only monitoring bullets inside Q1, Q2, Q4, Q6, Q7 and Q12); editorial question lists, not verified candidate reports; MLOps, ML platform and ML engineer roles at IT-services firms, product companies and GCCs | Retraining and champion-challenger sources (apxml.com 'retraining triggers', DataRobot docs on retraining settings and challengers, a pertamapartners glossary on shadow comparison windows, an ifactoryapp retraining-cadence guide; search snippets only, not opened; numeric windows and percentages in them are vendor suggestions and are not used); vendor docs and blogs, not interview reports; MLOps and ML platform roles
**Say this first (1 line):** I use a hybrid: retrain on a performance or sustained-drift trigger, with a scheduled fallback, behind guardrails: a data-quality veto, a cooldown, a minimum new data size, a champion-challenger evaluation and human approval for high-risk models.

**Then explain:**
| Trigger | Cost | Risk |
|---|---|---|
| Scheduled | predictable, may waste runs | misses a fast change |
| Data volume | simple | volume is not change |
| Drift-triggered | needs no labels | retrain on harmless drift; noisy |
| Performance-triggered | the real signal | late (label lag) |
| Hybrid | most to design | best coverage |
- Failure modes: retraining on corrupted data (so the data-quality gate comes first); retrain loops (a retrain triggers the next one); trigger flapping (a cooldown); an automatic promotion that is worse than the champion.
- Guardrails: data-quality veto, minimum interval, minimum new rows, evaluate against the champion before promotion (Part 7 owns the CI gate), approval for high-risk models.
- Part 5 owns how the pipeline runs; this answer is the decision logic.

**Example (from my run):** World changes on day 12. Day 14: performance is below the floor, but the data-quality gate fails, so the decision is VETO. Day 15: data is clean, so a retrain is requested for approval. Day 45: the scheduled trigger asks for a retrain when the model is 30 days old.

**Code:**
```python
from dataclasses import dataclass
import numpy as np

@dataclass
class Day:
    d: int; drift: float; acc: float | None; dq_ok: bool; new_rows: int

COOLDOWN, MAX_AGE, MIN_ROWS, DRIFT_HI, ACC_FLOOR = 7, 30, 20000, 0.2, 0.75

def decide(day, hist, last_train, high_risk=True):
    since = day.d - last_train
    drift_run = len(hist) >= 3 and all(h.drift > DRIFT_HI for h in hist[-3:])   # 3 days in a row
    reason = None
    if day.acc is not None and day.acc < ACC_FLOOR: reason = f"performance {day.acc:.2f} < {ACC_FLOOR}"
    elif drift_run:                                 reason = "drift above limit 3 days running"
    elif since >= MAX_AGE:                          reason = f"scheduled: model is {since}d old"
    if reason is None:                     return "none"
    if not day.dq_ok:                      return f"VETO ({reason}): data-quality gate failed"
    if since < COOLDOWN:                   return f"hold: cooldown ({since}d < {COOLDOWN}d)"
    if day.new_rows < MIN_ROWS:            return "hold: not enough new rows"
    return ("RETRAIN needs human approval: " if high_risk else "RETRAIN: ") + reason

rng = np.random.default_rng(30)
WORLD_CHANGE = 12          # the world shifts on day 12; a retrain after that fixes drift and, later, accuracy
last_train, hist, rows_since = 0, [], 0
print(f"{'day':>3} {'drift':>6} {'acc':>6} {'dq':>3} {'rows':>6}  decision")
for d in range(1, 51):
    rows_since += int(rng.integers(4000, 9000))
    stale = d >= WORLD_CHANGE and last_train < WORLD_CHANGE          # model still trained on the old world
    drift = 0.08 + rng.normal(0, 0.02) + (0.18 if stale else 0)
    acc = None if d < 8 else round(0.82 - (0.09 if stale and d >= 14 else 0) + rng.normal(0, 0.01), 3)
    day = Day(d, round(drift, 3), acc, dq_ok=not (13 <= d <= 14), new_rows=rows_since)
    hist.append(day)
    out = decide(day, hist, last_train)
    if out.startswith("RETRAIN"):          # assume the approval comes and training finishes the same day
        last_train, rows_since = d, 0
    if out != "none" and not out.startswith("hold: cooldown"):
        print(f"{d:>3} {day.drift:6.3f} {str(day.acc):>6} {'ok' if day.dq_ok else 'BAD':>3} {day.new_rows:>6}  {out}")
print("last training day:", last_train, "| days 1-50 with 'none' or cooldown holds are not printed")
```

**Output (my run):**
```text
day  drift    acc  dq   rows  decision
 14  0.256  0.735 BAD  87161  VETO (performance 0.73 < 0.75): data-quality gate failed
 15  0.242  0.724  ok  94325  RETRAIN needs human approval: performance 0.72 < 0.75
 45  0.084  0.837  ok 205813  RETRAIN needs human approval: scheduled: model is 30d old
last training day: 45 | days 1-50 with 'none' or cooldown holds are not printed
```
Ran with `python3 -I`, numpy 2.5.4, seeded. The simulation assumes approval and training finish on the same day and that a retrain removes the drift; that is a simplification. The thresholds (7-day cooldown, 30-day max age, 20000 rows, drift limit 0.2, accuracy floor 0.75) are my example values. Cooldown holds and "none" days are not printed.

**Follow-ups:**
- *Who approves?* The model owner, with the evaluation report; for low-risk models, auto-promote after the challenger beats the champion.
- *Retrain on a window or all data?* Test both on a holdout from after the change.
- *Retrain loop?* Cooldown plus a cap on retrains per period and an alert when the cap is hit.

**Common mistakes:**
- Triggering on drift alone and retraining on harmless shift.
- No data-quality veto, so a broken feed trains the next model.
- Promoting without comparing to the current model.

---
