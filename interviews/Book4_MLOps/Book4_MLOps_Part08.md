# Book 4 — Part 8: Monitoring ML in production: drift, data quality, alerting, retraining

**Topic:** Monitoring ML in production: data drift, concept drift, label and prior shift, covariate shift, training-serving skew, drift tests (PSI, KS, chi-square, Jensen-Shannon, Wasserstein) and their pitfalls (sample size, multiple testing, seasonality), data quality checks (nulls, schema, ranges, freshness, volume), model performance monitoring with delayed or missing labels (proxy metrics, canary labels, estimated performance), prediction and score distribution monitoring, fairness monitoring, the operational-metrics boundary with Part 6, alerting design (thresholds, alert fatigue, SLOs and SLIs for ML, runbooks, on-call), retraining triggers and policies (scheduled versus triggered, champion-challenger, shadow), monitoring tools at concept level (Evidently, whylogs and WhyLabs, Arize, Fiddler, Prometheus and Grafana, Great Expectations, SageMaker Model Monitor, Vertex AI Model Monitoring), logging prediction and feature payloads and privacy, the LLM monitoring boundary with Book 2, and incident handling and post-mortems for model failures
**Target:** 45  |  **Actual:** 45 (⭐⭐⭐ 17, ⭐⭐ 17, ⭐ 11)  |  **Date:** 2026-10-26  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

Scope note: Part 1 owns Git, pre-commit and pytest for ML code; Part 2 owns Docker; Part 3 owns Kubernetes and Helm; Part 4 owns DVC, MLflow and registry basics; Part 5 owns pipelines, scheduling and orchestration; Part 6 owns serving mechanics, latency and error metrics, probes, shadow, canary and rollout; Part 7 owns CI workflows and promotion gates; Part 9 owns feature stores, Kafka and Spark; Parts 10 and 11 own AWS, Azure and GCP services; Part 12 owns cost and system design in depth; Book 1 owns statistics and ML theory (drift-test theory here is only what a monitor needs); Book 2 owns LLM internals, RAG and LLM evaluation; Book 3 owns SQL; Book 6 owns product and business. This part owns what happens after deploy: watching data, predictions and performance, alerting, retraining decisions and incident handling.

Evidence limits: WebFetch worked for one page only (github.com Devinterview-io/mlops-interview-questions, opened) and failed with getaddrinfo ENOTFOUND for evidentlyai.com, docs.cloud.google.com, sre.google and datacamp.com; every other source is a search snippet only (see research_notes/Book4_Part08_sources.md). No page was found that reports exact monitoring questions asked by a named company at an India or global ML role; 'Asked at' tags therefore name source types (question banks, vendor and cloud docs, SRE docs, papers), not verified company reports. Execution limit: pip install worked through the proxy in fresh venvs under /tmp/claude-0/b8p08, so Wave B can really run on Python 3.13.17: numpy 2.5.4, scipy 1.18.1, pandas 3.1.0, scikit-learn 1.9.1, pytest 9.1.1, prometheus-client 0.26.0, pandera 0.35.0 (needs the pandera[pandas] extra), great-expectations 1.24.1 (ephemeral context with a pandas dataframe asset validated offline), whylogs 1.6.4 (needs the whylogs[viz] extra for drift scores; profiles and KS drift scores work offline), and evidently 0.7.23, which fails to import under pandas 3.1.0 (infer_dtype_from_object) but runs with pandas 2.3.3 and writes a local HTML report plus a dict of drift results (Wasserstein for numeric and Jensen-Shannon for categorical by default in that version). alibi-detect 0.13.0 could not be used: the full install failed building scikit-image, and a --no-deps install pins numpy below 2 and pandas below 3 and needs more packages, so alibi-detect is labelled not executed. Simulated delayed-label estimation, PSI, KS, chi-square, Jensen-Shannon and Wasserstein maths ran with numpy and scipy. Prometheus, Grafana, Alertmanager and promtool are not installed, so server-side behaviour is 'not executed' (alert rules and routing can only be checked structurally with pyyaml); cloud monitors (SageMaker Model Monitor, Vertex AI Model Monitoring, Azure ML), Arize, Fiddler and WhyLabs SaaS were not available and must be labelled 'not executed'. Wave B must use pandas below 3 in any Evidently example and say so.

---

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

### Q13 ⭐⭐⭐ 🟡 Champion-challenger and shadow evaluation for a retrained model. Explain what is compared (same live traffic, matured labels or proxy), how long to run, what the statistical question is (is the challenger really better, with a confidence interval, not a one-point difference), and what you do when labels are delayed. Part 6 owns the shadow and canary mechanics and Part 7 the promotion gate, so keep to the evaluation logic. Simulate champion and challenger predictions on the same 5000 labelled cases, compute a paired bootstrap interval on the AUC difference, and write a promote or hold decision.
**Asked at:** MLOps interview question banks and guides (K21Academy '47 MLOps interview questions' PDF, Towards AI '101 ML LLM agentic AIOps interview questions', DataCamp MLOps interview questions, The Interview Guys MLOps post, wecreateproblems.com, hyring.com, dev.to vivekk101, a Medium skphd post; search snippets only, not opened; the Devinterview-io/mlops-interview-questions GitHub page WAS opened and has no dedicated monitoring or drift question, only monitoring bullets inside Q1, Q2, Q4, Q6, Q7 and Q12); editorial question lists, not verified candidate reports; MLOps, ML platform and ML engineer roles at IT-services firms, product companies and GCCs | Retraining and champion-challenger sources (apxml.com 'retraining triggers', DataRobot docs on retraining settings and challengers, a pertamapartners glossary on shadow comparison windows, an ifactoryapp retraining-cadence guide; search snippets only, not opened; numeric windows and percentages in them are vendor suggestions and are not used); vendor docs and blogs, not interview reports; MLOps and ML platform roles
**Say this first (1 line):** I score the champion and the challenger on the same cases, take the paired difference in the metric with a bootstrap confidence interval, and promote only if the whole interval is above a gain floor the business agreed, otherwise I hold and wait for more matured labels.

**Then explain:**
- Same cases for both models. Shadow mode sends live traffic to both and logs both predictions, so any difference comes from the model, not from different users. (Part 6 owns the shadow mechanics, Part 7 owns the promotion gate.)
- What is compared: matured labels when they exist. If labels are late, compare on a proxy (an early label, a click, a rule-based outcome), and use label-free estimates only as a hint, never as the gate.
- The question is statistical: is the difference really above zero? A one-point AUC gap on a few thousand cases can be noise. Because both models see the same rows, use a paired test or paired bootstrap. Resample rows once, score both models on that sample, take the difference, repeat.
- How long to run: until enough labels have matured for the interval to be narrower than the gain you care about, and at least one full business cycle (week, month end, festival week). Do not peek daily and stop on the first good-looking day, that inflates false wins.
- Failure modes: the champion's predictions changed the data you labelled (selection bias, for example only approved loans get outcomes); label delay differs by segment; the challenger wins on average but loses on one important segment; a win in AUC but a worse calibrated score.

**Example:** 1000 shared cases. Champion right on 800, challenger right on 810. Suppose 40 cases only the champion got right and 50 only the challenger got right (b=40, c=50, so the net is +10 cases, +1.0 point). The standard error of the net count is about sqrt(b+c) = sqrt(90) = 9.5, so z = 10 / 9.5 = 1.05. That is well under 2, so the +1 point is not proven. Hold.

**Code:**
```python
import numpy as np
from sklearn.metrics import roc_auc_score
rng = np.random.default_rng(13)
n = 5000
y = (rng.random(n) < 0.2).astype(int)
# both models see the same cases; part of their error is shared (common features), part is their own
shared = rng.normal(0, 1, n)
champ = shared + 1.0 * y + 0.8 * rng.normal(0, 1, n)
chall_small = shared + 1.1 * y + 0.8 * rng.normal(0, 1, n)   # small real gain
chall_noise = shared + 1.0 * y + 0.8 * rng.normal(0, 1, n)   # no real gain, different noise
def auc_diff(chall, idx):
    return roc_auc_score(y[idx], chall[idx]) - roc_auc_score(y[idx], champ[idx])
MIN_GAIN = 0.005   # business floor chosen by the team, an assumption here
B = 1000
print(f"AUC champion {roc_auc_score(y, champ):.4f}")
for name, chall in [("challenger_small_gain", chall_small), ("challenger_noise_only", chall_noise)]:
    obs = auc_diff(chall, np.arange(n))
    diffs = np.empty(B)
    for b in range(B):
        idx = rng.integers(0, n, n)          # paired: same resampled rows for both models
        diffs[b] = auc_diff(chall, idx)
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    if lo > 0 and obs >= MIN_GAIN:
        decision = "PROMOTE (CI above zero and gain above the floor)"
    elif hi < 0:
        decision = "REJECT (challenger is worse)"
    else:
        decision = "HOLD (CI includes zero or gain below floor; collect more labels)"
    print(f"{name}: AUC {roc_auc_score(y, chall):.4f} diff {obs:+.4f} 95% CI [{lo:+.4f}, {hi:+.4f}] -> {decision}")
```

**Output (my run):**
```text
AUC champion 0.7065
challenger_small_gain: AUC 0.7398 diff +0.0333 95% CI [+0.0178, +0.0508] -> PROMOTE (CI above zero and gain above the floor)
challenger_noise_only: AUC 0.7130 diff +0.0064 95% CI [-0.0106, +0.0239] -> HOLD (CI includes zero or gain below floor; collect more labels)
```
Run with python3 -I in the numpy/scipy/scikit-learn venv (numpy 2.5.4, scikit-learn 1.9.1), seed 13. The data is simulated. The "noise only" challenger shows a +0.0064 point gap that would look like a win on a dashboard, but its interval crosses zero. The 0.005 floor is my assumption for the demo, not a standard. In the output, a model that is truly better is promoted and the noisy one is held.

**Follow-ups:**
- *Labels take 60 days, what do you do?* Run on proxy labels and on estimated performance for early signal, keep the champion live, and make the promotion decision on matured labels for a smaller early cohort.
- *Why paired and not two separate intervals?* The two models are strongly correlated on the same rows. The paired difference has a much smaller variance than two independent intervals suggest.
- *Challenger better overall, worse on one segment?* Check the segment interval, and decide with the business whether that segment can be routed to the champion.

**Common mistakes:**
- Comparing a point difference with no interval.
- Different traffic windows for the two models.
- Stopping the test the first day the challenger leads.
- Using only the metric the new model was tuned on.
- Ignoring that the champion's decisions shaped which cases got labels.

### Q14 ⭐⭐⭐ 🟡 Scenario: your drift dashboard fires an alert for feature X. What do you do, in order? Cover checking the pipeline and data quality first (a bug is more likely than the world), whether the shifted feature matters to the model, seasonality or a known event, the effect on predictions and on matured-label performance, and then decide among no action, recalibrate, retrain or roll back. Implement a small triage function that takes the evidence and returns an action with a reason, run it on four cases, and say where the order can be wrong.
**Asked at:** MLOps interview question banks and guides (K21Academy '47 MLOps interview questions' PDF, Towards AI '101 ML LLM agentic AIOps interview questions', DataCamp MLOps interview questions, The Interview Guys MLOps post, wecreateproblems.com, hyring.com, dev.to vivekk101, a Medium skphd post; search snippets only, not opened; the Devinterview-io/mlops-interview-questions GitHub page WAS opened and has no dedicated monitoring or drift question, only monitoring bullets inside Q1, Q2, Q4, Q6, Q7 and Q12); editorial question lists, not verified candidate reports; MLOps, ML platform and ML engineer roles at IT-services firms, product companies and GCCs | Scenario question write-ups (a Glassdoor EPAM Systems interview page whose snippet lists 'why does production differ from training' with feature, preprocessing and version mismatch as causes, and an end-to-end design prompt; one candidate's review, search snippet only, not opened, unverified; The Interview Guys post saying drift is asked in almost every MLOps interview, snippet only); anecdotal, not company-verified reports; MLOps and ML engineer roles
**Say this first (1 line):** I assume a bug before I assume the world changed: check the pipeline and data quality, then whether the feature matters, then known events, then the effect on predictions and matured labels, and only then choose no action, recalibrate, retrain or roll back.

**Then explain:**
- Step 1, data and pipeline. Null spike, unit or schema change, a late or partial load, a feature-pipeline version change. A bug is more likely than a real shift, and retraining on a bug bakes the bug in.
- Step 2, is it a known event? Festival, sale, month end, a campaign, a product change. Compare with a baseline from the same period before calling it drift.
- Step 3, does the model care? Look at the feature's importance or attribution share. A drifting low-importance feature is usually a tuning problem for the alert, not for the model.
- Step 4, effect: did the score distribution or positive rate move, and do matured labels show a drop? Drift alone is not harm. Labels that have not matured yet mean you can only estimate.
- Step 5, decide: fix the pipeline, no action, recalibrate (if scores shifted but ranking is fine), retrain, or roll back (if a recent release is the cause).
- Where the order can be wrong: a partial bug hides inside a real shift, so fixing it does not close the case. A known event can mask a real change that happens at the same time. A feature that looks unimportant alone can matter in an interaction. Stable outputs can hide two shifts that cancel out.

**Example:** Income drift alert on Monday. Null rate for income went from 0 to 30 percent after a Friday deploy. Step 1 stops you: fix the upstream join. Compare the same alert in Diwali week, where null rate is normal and the average basket is up: known event, watch, compare with last year's same week. A third case: a minor feature drifts, nothing else moves: no action, raise the alert threshold.

**Code:**
```python
from dataclasses import dataclass

@dataclass
class Evidence:
    pipeline_bug: bool            # null spike, schema/unit change, late data, version mismatch
    known_event: bool             # festival, campaign, holiday, planned change
    feature_important: bool       # importance or attribution share is material
    prediction_shift: bool        # score or positive-rate moved beyond its band
    labels_matured: bool
    perf_drop: bool | None        # None when labels not matured

def triage(e: Evidence):
    if e.pipeline_bug:
        return "FIX_PIPELINE", "data or code problem; fix upstream, do not retrain on bad data (roll back if the bad data is already served)"
    if e.known_event:
        return "NO_ACTION_WATCH", "explained by a known event; compare with same-period baseline and re-check after it ends"
    if not e.feature_important and not e.prediction_shift:
        return "NO_ACTION", "feature does not matter to the model and outputs are stable; log and tune the alert"
    if e.labels_matured and e.perf_drop:
        return "RETRAIN_OR_ROLLBACK", "matured labels confirm a drop; retrain on fresh data, roll back if a recent release caused it"
    if e.labels_matured and not e.perf_drop:
        return "NO_ACTION", "matured labels show no drop; drift is harmless for now"
    if e.prediction_shift:
        return "RECALIBRATE_AND_WATCH", "outputs moved but no labels yet; check calibration, estimate performance without labels, wait for labels"
    return "WATCH", "important feature moved, outputs stable, labels not matured; keep watching"

cases = {
 "A null spike after a schema change": Evidence(True, False, True, True, False, None),
 "B Diwali week traffic":              Evidence(False, True, True, True, False, None),
 "C minor feature, outputs stable":    Evidence(False, False, False, False, True, False),
 "D key feature, labels show drop":    Evidence(False, False, True, True, True, True),
}
for name, ev in cases.items():
    a, r = triage(ev)
    print(f"{name:38s} -> {a:22s} | {r}")
```

**Output (my run):**
```text
A null spike after a schema change     -> FIX_PIPELINE           | data or code problem; fix upstream, do not retrain on bad data (roll back if the bad data is already served)
B Diwali week traffic                  -> NO_ACTION_WATCH        | explained by a known event; compare with same-period baseline and re-check after it ends
C minor feature, outputs stable        -> NO_ACTION              | feature does not matter to the model and outputs are stable; log and tune the alert
D key feature, labels show drop        -> RETRAIN_OR_ROLLBACK    | matured labels confirm a drop; retrain on fresh data, roll back if a recent release caused it
```
Run with python3 -I (pure standard library plus a dataclass). The four cases are made up by me for the demo.

**Follow-ups:**
- *Why not retrain straight away?* If the cause is a bug, you train on corrupted data and lose your last good baseline. Retraining is also slow and risky; try cheaper actions first.
- *What if labels are weeks away?* Use label-free estimates, check calibration, keep a close watch, and set a deadline to revisit when labels land.
- *How do you reduce these alerts?* Rank features by importance, use effect-size floors, and only page on features that matter.

**Common mistakes:**
- Retraining on the alert alone.
- Skipping the data-quality check.
- Treating every drifting feature as equally important.
- No owner or decision log for the alert.
- Declaring "no performance drop" using labels that are not mature yet.

### Q15 ⭐⭐⭐ 🟡 The tool landscape at concept level: Evidently, whylogs and WhyLabs, Great Expectations, pandera, Arize, Fiddler, Prometheus with Grafana, and the cloud monitors (SageMaker Model Monitor, Vertex AI Model Monitoring). Say what each one does best, open source versus SaaS, batch report versus continuous metrics, and how you would choose for a team with no budget and for a bank. Generate a real local drift report with Evidently and a profile with whylogs on the same two DataFrames, record the versions and what ran, and label SaaS and cloud tools not executed.
**Asked at:** MLOps interview question banks and guides (K21Academy '47 MLOps interview questions' PDF, Towards AI '101 ML LLM agentic AIOps interview questions', DataCamp MLOps interview questions, The Interview Guys MLOps post, wecreateproblems.com, hyring.com, dev.to vivekk101, a Medium skphd post; search snippets only, not opened; the Devinterview-io/mlops-interview-questions GitHub page WAS opened and has no dedicated monitoring or drift question, only monitoring bullets inside Q1, Q2, Q4, Q6, Q7 and Q12); editorial question lists, not verified candidate reports; MLOps, ML platform and ML engineer roles at IT-services firms, product companies and GCCs | Prometheus and Grafana monitoring mentions (K21Academy and Towards AI question lists naming Prometheus, Grafana and Evidently for drift and accuracy dashboards; Devinterview-io page opened, Q12 mentions inference monitoring with Grafana and Prometheus; search snippets otherwise); question lists, not verified reports; MLOps and platform roles; Prometheus, Grafana and Alertmanager servers were not available in this sandbox
**Say this first (1 line):** I pick by job: Evidently or whylogs for batch drift reports and profiles, Great Expectations or pandera for data rules, Prometheus with Grafana for continuous health metrics and alerts, and a SaaS or cloud monitor when the team wants managed storage, UI and alerting and accepts the cost and data-sharing review.

**Then explain:**
- Evidently (open source): batch drift, quality and performance reports and test suites, with HTML output. Good at the analysis, you provide the scheduling and storage.
- whylogs (open source) with WhyLabs (SaaS platform): whylogs makes small mergeable statistical profiles, so you log profiles instead of raw data. Good when raw data must not leave. Check current docs for the state of the hosted WhyLabs service.
- Great Expectations: data-quality rules with reports (Data Docs), runs in pipelines. pandera: lightweight schema checks inside Python code. Next question covers them.
- Prometheus with Grafana: continuous numeric metrics, time series, alert rules, dashboards. Not good at "compare two datasets"; a drift job computes the score and Prometheus stores it.
- Arize, Fiddler: SaaS observability platforms (drift, performance, explainability, UI). SageMaker Model Monitor, Vertex AI Model Monitoring: managed monitors tied to their cloud. Check current docs for what each supports; I did not run any of them.
- Choosing. No budget: Evidently or whylogs plus pandera plus Prometheus and Grafana, scheduled by what you already use. A bank: data residency, audit trail and access control come first. Self-hosted open source or the cloud monitor inside the bank's own account, with a security review before any SaaS gets prediction data.
- Failure modes: version incompatibility (see output below), report-only tools that nobody schedules, defaults used without thought, raw data sent to a third party by mistake.

**Example:** Team of three, no budget, a daily batch credit model. Daily job: pandera checks on input, Evidently report saved to object storage, drift scores and null rates pushed as Prometheus metrics, a Grafana panel, and an alert rule for the one or two features that matter.

| Tool | Open source / SaaS | Batch report or continuous | Ran here |
|---|---|---|---|
| Evidently | open source | batch report, tests | yes (0.7.23) |
| whylogs | open source | profiles, batch or streaming | yes (1.6.4) |
| WhyLabs | SaaS | continuous platform | not executed |
| Great Expectations | open source | batch validation | yes (Q22) |
| pandera | open source | in-code validation | yes (Q22) |
| Prometheus + Grafana | open source | continuous metrics | client library only (Q16) |
| Arize, Fiddler | SaaS | continuous platform | not executed |
| SageMaker Model Monitor, Vertex AI Model Monitoring | cloud managed | scheduled monitors | not executed |

**Code:**
```python
# ---- file: q15_make_data.py ----
import sys, numpy as np, pandas as pd
rng = np.random.default_rng(15)
def frame(n, age_mu, inc_mu, p_city):
    return pd.DataFrame({"age": rng.normal(age_mu, 8, n).round(1),
                         "income": rng.normal(inc_mu, 15000, n).round(0),
                         "city": rng.choice(["Mumbai", "Pune", "Delhi"], n, p=p_city)})
frame(2000, 35, 60000, [.4, .3, .3]).to_csv(sys.argv[1] + "/ref.csv", index=False)
frame(2000, 36, 70000, [.2, .3, .5]).to_csv(sys.argv[1] + "/cur.csv", index=False)

# ---- file: q15_evidently.py ----
import sys, pandas as pd, evidently
from evidently import Report
from evidently.presets import DataDriftPreset
ref = pd.read_csv(sys.argv[1] + "/ref.csv"); cur = pd.read_csv(sys.argv[1] + "/cur.csv")
print("evidently", evidently.__version__, "pandas", pd.__version__)
snap = Report([DataDriftPreset()]).run(cur, ref)
d = snap.dict()
for m in d["metrics"]:
    print(m["metric_name"], "->", m["value"])
snap.save_html(sys.argv[1] + "/drift.html")
import os; print("html written:", os.path.getsize(sys.argv[1] + "/drift.html") > 100000)

# ---- file: q15_whylogs.py ----
import sys, pandas as pd, whylogs as why
from whylogs.viz.drift.column_drift_algorithms import calculate_drift_scores
ref = pd.read_csv(sys.argv[1] + "/ref.csv"); cur = pd.read_csv(sys.argv[1] + "/cur.csv")
print("whylogs", why.__version__, "pandas", pd.__version__)
ref["city"] = ref["city"].astype(object); cur["city"] = cur["city"].astype(object)  # pandas 3 str dtype breaks whylogs 1.6.4 type matching
pr = why.log(ref).view(); pc = why.log(cur).view()
print(pc.to_pandas()[["counts/n", "counts/null", "types/fractional", "distribution/mean", "distribution/stddev"]].round(1).to_string())
scores = calculate_drift_scores(target_view=pc, reference_view=pr, with_thresholds=True)
for col, s in scores.items():
    print(col, s["algorithm"], round(s["statistic"], 4), "p=", round(s["pvalue"], 6), s["drift_category"])
```

**Output (my run):**
```text
evidently 0.7.23 pandas 2.3.3
DriftedColumnsCount(drift_share=0.5) -> {'count': 3.0, 'share': 1.0}
ValueDrift(column=age,method=Wasserstein distance (normed),threshold=0.1) -> 0.10357764053630446
ValueDrift(column=income,method=Wasserstein distance (normed),threshold=0.1) -> 0.6956238223011112
ValueDrift(column=city,method=Jensen-Shannon distance,threshold=0.1) -> 0.16192601436159115
html written: True
```
```text
whylogs 1.6.4 pandas 3.1.0
        counts/n  counts/null  types/fractional  distribution/mean  distribution/stddev
column                                                                                 
age         2000            0              2000               36.1                  8.0
city        2000            0                 0                0.0                  0.0
income      2000            0              2000            70030.3              15191.9
age ks 0.0475 p= 0.021231 DRIFT
income ks 0.2775 p= 0.0 DRIFT
city chi-square 429.3821 p= 0.0 DRIFT
```
Versions: Evidently 0.7.23 ran in its own venv with pandas 2.3.3, because it fails to import with pandas 3.1.0. whylogs 1.6.4 with whylogs[viz] ran with pandas 3.1.0. It failed on pandas 3's new string dtype for the text column until I cast it to object, so that cast is in the script. Data: two 2000-row frames from numpy seed 15, with real shifts built in (age +1, income +10000, city mix changed). Evidently also wrote an HTML report (the script printed `html written: True` after a size check; I did not open it in a browser). Its output shows its defaults as seen in this local run: normed Wasserstein for numeric columns and Jensen-Shannon distance for the categorical one, each with threshold 0.1, and a dataset-level rule of drift share 0.5. The age score of 0.1036 is only just over 0.1. whylogs here used a KS test for numeric and chi-square for categorical, and flagged age as DRIFT at p=0.021, which shows how sensitive a p-value rule is at n=2000. SaaS and cloud tools: not executed (no accounts, no network to those services); the validation that did run is the two local runs above.

**Follow-ups:**
- *Why not just use the cloud monitor?* Fine if you are already on that cloud and it covers your model type. Check what baselines it needs and where the logs sit.
- *What is a whylogs profile?* A compact summary of each column (counts, nulls, distribution sketch), not raw rows, so it is cheap to store and share.
- *Evidently versus Prometheus?* Evidently answers "did this dataset change". Prometheus answers "what is the number over time and should we page".

**Common mistakes:**
- Buying a platform before knowing which three metrics matter.
- Treating default thresholds as truth.
- Sending raw customer data to a SaaS tool without review.
- Report with no schedule, owner or alert.
- Not pinning versions; these libraries change APIs quickly.

### Q16 ⭐⭐⭐ 🟡 Exposing model-health metrics to Prometheus: what to export (feature null rate, drift score per feature, prediction histogram, positive rate, label-join lag, model version info), why label cardinality must stay small, and how this relates to the serving metrics Part 6 already owns (latency, errors, saturation). Implement the metrics with prometheus_client in a CollectorRegistry, update them from a drift job, print the exposition text, and write the matching alert rules and Grafana panel query as text. The Prometheus, Grafana and Alertmanager servers are not available, so say what was not executed and validate the rule YAML with pyyaml.
**Asked at:** MLOps interview question banks and guides (K21Academy '47 MLOps interview questions' PDF, Towards AI '101 ML LLM agentic AIOps interview questions', DataCamp MLOps interview questions, The Interview Guys MLOps post, wecreateproblems.com, hyring.com, dev.to vivekk101, a Medium skphd post; search snippets only, not opened; the Devinterview-io/mlops-interview-questions GitHub page WAS opened and has no dedicated monitoring or drift question, only monitoring bullets inside Q1, Q2, Q4, Q6, Q7 and Q12); editorial question lists, not verified candidate reports; MLOps, ML platform and ML engineer roles at IT-services firms, product companies and GCCs | Prometheus and Grafana monitoring mentions (K21Academy and Towards AI question lists naming Prometheus, Grafana and Evidently for drift and accuracy dashboards; Devinterview-io page opened, Q12 mentions inference monitoring with Grafana and Prometheus; search snippets otherwise); question lists, not verified reports; MLOps and platform roles; Prometheus, Grafana and Alertmanager servers were not available in this sandbox
**Say this first (1 line):** A drift or quality job computes the numbers and exports them as a few low-cardinality gauges and histograms, labelled by model and feature only, and Prometheus alert rules and Grafana panels sit on top; request-level detail goes to the prediction log, not to labels.

**Then explain:**
- What to export: null ratio and drift score per feature, a histogram of prediction scores, positive rate, label-join lag (how old the newest matured labels are), and an info metric with model version and feature pipeline version.
- Cardinality: every label combination is a separate time series stored in memory. Labels like `model` and `feature` are bounded; `user_id`, `request_id` or raw values are not. Unbounded labels can overload the server.
- Part 6 owns serving metrics (latency, error rate, saturation). Model-health metrics sit beside them: the service can be perfectly healthy with a silently wrong model. Show both on one dashboard, with different owners and severities.
- Jobs that run once a day suit a push or a scrape of a long-lived exporter; check current Prometheus docs for the Pushgateway caveats. A gauge set by a job is the last known value, so also export the job's last-success time, or a dead job looks healthy.
- Alert rules: for-duration to avoid flapping, a page only for things needing action now (high null rate), a ticket for slower things (drift, stale labels).

**Example:** drift gauge for income is 0.31 (above 0.25) for 30 minutes, so `FeatureDriftHigh` opens a ticket. The null ratio for income is 0.02, under the 0.05 limit, so no page. Hand check: 3 features x 1 model = 3 series per gauge; adding `request_id` as a label would make one new series for every request.

**Code:**
```python
import yaml
from prometheus_client import CollectorRegistry, Gauge, Histogram, Info, generate_latest

reg = CollectorRegistry()
null_rate = Gauge("model_feature_null_ratio", "Share of nulls in last window", ["model", "feature"], registry=reg)
drift = Gauge("model_feature_drift_score", "Drift score (PSI) vs reference", ["model", "feature"], registry=reg)
pos_rate = Gauge("model_positive_rate", "Share of positive predictions in window", ["model"], registry=reg)
label_lag = Gauge("model_label_join_lag_seconds", "Age of newest matured label batch", ["model"], registry=reg)
score_h = Histogram("model_prediction_score", "Prediction score distribution", ["model"],
                    buckets=[0.1, 0.25, 0.5, 0.75, 0.9], registry=reg)
info = Info("model_build", "Model and feature pipeline version", registry=reg)

info.info({"model": "churn", "model_version": "7", "feature_pipeline": "2026.10.1"})
# a drift job updates the metrics (values hard-coded stand-ins for job output)
for f, nr, d in [("age", 0.00, 0.03), ("income", 0.02, 0.31), ("city", 0.00, 0.05)]:
    null_rate.labels("churn", f).set(nr)
    drift.labels("churn", f).set(d)
pos_rate.labels("churn").set(0.118)
label_lag.labels("churn").set(172800)
for s in [0.05, 0.2, 0.2, 0.4, 0.6, 0.95]:
    score_h.labels("churn").observe(s)
print(generate_latest(reg).decode())

rules_text = """
groups:
  - name: model-health
    rules:
      - alert: FeatureDriftHigh
        expr: model_feature_drift_score > 0.25
        for: 30m
        labels: {severity: ticket}
        annotations:
          summary: "Drift on {{ $labels.feature }} for {{ $labels.model }}"
      - alert: FeatureNullRateHigh
        expr: model_feature_null_ratio > 0.05
        for: 15m
        labels: {severity: page}
        annotations:
          summary: "Null rate high on {{ $labels.feature }}"
      - alert: PositiveRateOutOfBand
        expr: abs(model_positive_rate - avg_over_time(model_positive_rate[7d])) > 0.03
        for: 1h
        labels: {severity: ticket}
        annotations:
          summary: "Positive rate moved vs 7-day mean"
      - alert: LabelsStale
        expr: model_label_join_lag_seconds > 3 * 86400
        for: 1h
        labels: {severity: ticket}
        annotations:
          summary: "No new matured labels for 3 days"
"""
doc = yaml.safe_load(rules_text)
rules = doc["groups"][0]["rules"]
for r in rules:
    assert {"alert", "expr", "for", "labels", "annotations"} <= set(r), r
print("YAML parsed; groups:", len(doc["groups"]), "rules:", [r["alert"] for r in rules])
```
```text
# Grafana panel query (PromQL), time series panel, legend {{feature}}
max by (feature) (model_feature_drift_score{model="churn"})

# positive rate versus its own 7-day mean
model_positive_rate{model="churn"} - avg_over_time(model_positive_rate{model="churn"}[7d])
```

**Output (my run):**
```text
# HELP model_feature_null_ratio Share of nulls in last window
# TYPE model_feature_null_ratio gauge
model_feature_null_ratio{feature="age",model="churn"} 0.0
model_feature_null_ratio{feature="income",model="churn"} 0.02
model_feature_null_ratio{feature="city",model="churn"} 0.0
# HELP model_feature_drift_score Drift score (PSI) vs reference
# TYPE model_feature_drift_score gauge
model_feature_drift_score{feature="age",model="churn"} 0.03
model_feature_drift_score{feature="income",model="churn"} 0.31
model_feature_drift_score{feature="city",model="churn"} 0.05
# HELP model_positive_rate Share of positive predictions in window
# TYPE model_positive_rate gauge
model_positive_rate{model="churn"} 0.118
# HELP model_label_join_lag_seconds Age of newest matured label batch
# TYPE model_label_join_lag_seconds gauge
model_label_join_lag_seconds{model="churn"} 172800.0
# HELP model_prediction_score Prediction score distribution
# TYPE model_prediction_score histogram
model_prediction_score_bucket{le="0.1",model="churn"} 1.0
model_prediction_score_bucket{le="0.25",model="churn"} 3.0
model_prediction_score_bucket{le="0.5",model="churn"} 4.0
model_prediction_score_bucket{le="0.75",model="churn"} 5.0
model_prediction_score_bucket{le="0.9",model="churn"} 5.0
model_prediction_score_bucket{le="+Inf",model="churn"} 6.0
model_prediction_score_count{model="churn"} 6.0
model_prediction_score_sum{model="churn"} 2.4000000000000004
# HELP model_prediction_score_created Prediction score distribution
# TYPE model_prediction_score_created gauge
model_prediction_score_created{model="churn"} 1.7930350282762375e+09
# HELP model_build_info Model and feature pipeline version
# TYPE model_build_info gauge
model_build_info{feature_pipeline="2026.10.1",model="churn",model_version="7"} 1.0

YAML parsed; groups: 1 rules: ['FeatureDriftHigh', 'FeatureNullRateHigh', 'PositiveRateOutOfBand', 'LabelsStale']
```
Run with python3 -I in a venv with prometheus-client 0.26.0 and pyyaml. The `_created` timestamp line changes on every run. Not executed: Prometheus, Alertmanager and Grafana servers (not installed here), so the rules were never loaded, evaluated or fired, and `promtool` was not available to check the PromQL. What did run: the exposition text and a pyyaml structural check that each rule has `alert`, `expr`, `for`, `labels` and `annotations`. That check does not prove the PromQL is valid. The Grafana panel queries are text only.

**Follow-ups:**
- *Histogram or gauge for scores?* Histogram, so Prometheus can compute quantiles and you can compare bucket shares over time. Pick buckets from the training score distribution.
- *Can Prometheus compute PSI?* Not directly. Compute drift in a job, export the number.
- *Why `for: 30m`?* A single noisy window should not open a ticket; the condition must hold.

**Common mistakes:**
- High-cardinality labels (ids, raw values, free text).
- Pushing metrics from a job that dies silently, with no freshness metric.
- Paging on slow drift.
- Mixing model-health alerts into the service on-call page with no runbook.
- Assuming the YAML parses means the rule is correct.

### Q17 ⭐⭐⭐ 🟢 What do you log from a model service so that monitoring is possible later? Cover request id, timestamp, model and feature-pipeline version, input features (raw and transformed), prediction and score, and a key to join late labels. Discuss sampling, schema versioning, storage format and volume, and the cost of logging everything. Build a prediction-log record with pydantic or a dataclass, write 1000 simulated records to JSON lines, join delayed labels by request id, and compute a metric on the matured subset. Privacy is the next question.
**Asked at:** MLOps interview question banks and guides (K21Academy '47 MLOps interview questions' PDF, Towards AI '101 ML LLM agentic AIOps interview questions', DataCamp MLOps interview questions, The Interview Guys MLOps post, wecreateproblems.com, hyring.com, dev.to vivekk101, a Medium skphd post; search snippets only, not opened; the Devinterview-io/mlops-interview-questions GitHub page WAS opened and has no dedicated monitoring or drift question, only monitoring bullets inside Q1, Q2, Q4, Q6, Q7 and Q12); editorial question lists, not verified candidate reports; MLOps, ML platform and ML engineer roles at IT-services firms, product companies and GCCs | Prediction-logging and privacy sources (apxml.com ML audit trails, gravitee.io PII redaction and retention, scalevise.com audit-ready logging, regolo.ai and mljar prompt pages; search snippets only, not opened; nothing found on India's DPDP Act for prediction logs, and retention figures in the snippets are vendor suggestions, not legal limits); vendor and practitioner posts, not interview reports; ML platform, security and data governance roles
**Say this first (1 line):** Log one structured record per prediction with a request id, timestamp, model and feature-pipeline versions, the inputs (raw and transformed), the score and the decision, so that I can join the label later and replay or audit the case.

**Then explain:**
- Fields: `request_id` (the join key to labels), timestamp, `model_version`, `feature_pipeline` version, raw features (to debug the pipeline), transformed features (what the model saw), score, decision, and a `schema_version` so old and new records can be read together.
- Raw versus transformed: raw tells you if the upstream data changed, transformed tells you if the transform changed. Training-serving skew is found by comparing them.
- Sampling: log all decisions for low-volume or high-stakes models; sample or log only features and scores for high-volume ones. Keep all records for rare classes. Record the sampling rate so rates can be rescaled.
- Storage: append-only, partitioned by date, in a columnar or line format (JSON lines is easy to start, Parquet is better for volume). Check the cost; logging everything costs money and creates privacy risk (next question).
- Failure modes: logging blocks the request path (log asynchronously, and drop with a counter rather than fail the call), duplicate or missing request ids break the join, schema changes silently, logs without the version cannot be tied to the model that made them.
- Labels come later. Keep a separate label table keyed by `request_id` and a matured flag or label date.

**Example:** 1000 requests logged. Labels have arrived for 70 percent. The accuracy of 0.669 is computed only on those 700 matured rows, not on all 1000. Hand check: 700 of 1000 is 70 percent, and duplicate ids are zero so the join does not multiply rows.

**Code:**
```python
import json, os, tempfile
import numpy as np
from pydantic import BaseModel

class PredictionLog(BaseModel):
    schema_version: int
    request_id: str
    ts: str
    model_version: str
    feature_pipeline: str
    features_raw: dict
    features_model: dict
    score: float
    prediction: int

rng = np.random.default_rng(17)
n = 1000
d = tempfile.mkdtemp()
path = os.path.join(d, "pred.jsonl")
truth = {}
with open(path, "w") as f:
    for i in range(n):
        age = int(rng.integers(21, 65)); inc = float(rng.integers(20, 200)) * 1000
        z = (age - 40) / 20 + (inc - 100000) / 100000
        p = 1 / (1 + np.exp(-z))
        rec = PredictionLog(schema_version=1, request_id=f"r{i:05d}",
              ts=f"2026-10-{1 + i // 40:02d}T10:{i % 60:02d}:00Z", model_version="7", feature_pipeline="2026.10.1",
              features_raw={"age": age, "income": inc}, features_model={"age_z": round((age - 40) / 12, 3), "income_log": round(float(np.log(inc)), 3)},
              score=round(float(p), 4), prediction=int(p >= 0.5))
        f.write(rec.model_dump_json() + "\n")
        truth[rec.request_id] = int(rng.random() < p)
print("rows written:", sum(1 for _ in open(path)), "| first line:")
print(open(path).readline().strip())
# labels arrive late: only 70% of requests have a label yet
labels = {k: v for k, v in truth.items() if int(k[1:]) % 10 < 7}
rows = [PredictionLog.model_validate_json(l) for l in open(path)]
joined = [(r, labels[r.request_id]) for r in rows if r.request_id in labels]
acc = sum(r.prediction == y for r, y in joined) / len(joined)
print(f"matured labels: {len(joined)} of {n} ({len(joined)/n:.0%}); accuracy on matured subset: {acc:.3f}")
# duplicate request ids would break the join: check
ids = [r.request_id for r in rows]
print("duplicate request ids:", len(ids) - len(set(ids)))
```

**Output (my run):**
```text
rows written: 1000 | first line:
{"schema_version":1,"request_id":"r00000","ts":"2026-10-01T10:00:00Z","model_version":"7","feature_pipeline":"2026.10.1","features_raw":{"age":53,"income":172000.0},"features_model":{"age_z":1.083,"income_log":12.055},"score":0.7974,"prediction":1}
matured labels: 700 of 1000 (70%); accuracy on matured subset: 0.669
duplicate request ids: 0
```
Run with python3 -I in the Evidently venv (it has pydantic 2.14.1, numpy 2.5.4). Seed 17; the data and labels are simulated, and labels are "arriving" for request numbers whose last digit is below 7, which is an arbitrary rule for the demo.

**Follow-ups:**
- *Why not log everything?* Cost, latency and privacy exposure. Log what monitoring and audit need; hash or drop the rest.
- *What if the request id is missing?* The label can never be joined. Make the id mandatory at the gateway.
- *JSON lines or Parquet?* JSON lines to start; move to a columnar format with a schema when volume grows.

**Common mistakes:**
- No model or pipeline version in the record.
- Only the final features, so skew cannot be debugged.
- Evaluating on the matured subset as if it were everything (it can be biased, since easy cases may get labels first).
- Logging synchronously in the request path.
- Changing the schema without a version.

### Q18 ⭐⭐ 🟡 Multiple testing in drift monitoring. With 100 features tested at 5 percent each, how many false alarms per run when nothing has changed? Explain Bonferroni, Benjamini-Hochberg, and the practical alternatives (a share-of-drifted-features rule, effect-size floors, only monitoring the top features). Simulate 100 stable features over 200 runs, count runs with at least one alert under each rule, and show the power cost on 5 truly drifted features.
**Asked at:** MLOps interview question banks and guides (K21Academy '47 MLOps interview questions' PDF, Towards AI '101 ML LLM agentic AIOps interview questions', DataCamp MLOps interview questions, The Interview Guys MLOps post, wecreateproblems.com, hyring.com, dev.to vivekk101, a Medium skphd post; search snippets only, not opened; the Devinterview-io/mlops-interview-questions GitHub page WAS opened and has no dedicated monitoring or drift question, only monitoring bullets inside Q1, Q2, Q4, Q6, Q7 and Q12); editorial question lists, not verified candidate reports; MLOps, ML platform and ML engineer roles at IT-services firms, product companies and GCCs | Drift-test pitfall sources (Evidently blog 'data drift detection on large datasets' saying KS is too sensitive on large data, an Arize docs monitors page saying PSI is less sample-sensitive, an ICLR 2026 virtual-page submission 'When drift detectors cry wolf' on false-alarm rates with PSI unstable below about 200 samples and Bonferroni lowering power, a wikidocs PSI and KS guide; search snippets only, not opened; WebFetch of evidentlyai.com failed with getaddrinfo ENOTFOUND; sources partly conflict on PSI versus KS sensitivity); vendor docs and one conference submission, not interview reports; MLOps and data science roles
**Say this first (1 line):** Test 100 features at 5 percent and you get about 5 false alarms per run even when nothing changed, so a raw "any feature drifted" alert fires almost every time; I use a correction, a share-of-features rule, an effect-size floor and a short list of features that matter, and I accept that each costs some power.

**Then explain:**
- The maths: with no drift, each test fires 5 percent of the time. Expected false alarms per run are 100 x 0.05 = 5, and the chance of at least one is 1 - 0.95^100, about 99.4 percent.
- Bonferroni: test each feature at 0.05/100. Strong control of false alarms, low power for small shifts.
- Benjamini-Hochberg: controls the share of false discoveries among the alerts instead. More power than Bonferroni, still some false alarms.
- Practical rules: alert only if a share of features drift (for example 10 percent or more), require a minimum effect size (such as KS statistic D, so tiny but significant shifts do not fire), and monitor only top-importance features.
- Failure modes: effect floors must match sample size (a floor of D 0.15 misses a real 0.3-sigma shift at n=500); a share rule can hide a few important features; features are correlated so tests are not independent; and sources disagree on how sensitive PSI versus KS are, so calibrate on your own stable history.

**Example:** 100 stable features, 200 runs, KS test at 0.05, n=500 per window. Hand check: expected 5 false alerts per run, and the chance of at least one is 99.4 percent. The raw rule fired in every run, 200 of 200.

**Code:**
```python
import numpy as np
from scipy.stats import ks_2samp
rng = np.random.default_rng(18)
F, RUNS, N = 100, 200, 500
ALPHA = 0.05
def run_pvals(drifted):
    ref = rng.normal(0, 1, (N, F)); cur = rng.normal(0, 1, (N, F))
    cur[:, :drifted] += 0.3        # first features shift by 0.3 sigma
    return np.array([ks_2samp(ref[:, j], cur[:, j]) for j in range(F)])  # rows: (D, p)
def bh(p, q=ALPHA):
    m = len(p); o = np.argsort(p); thr = q * (np.arange(1, m + 1) / m)
    ok = np.where(p[o] <= thr)[0]; rej = np.zeros(m, bool)
    if len(ok): rej[o[:ok.max() + 1]] = True
    return rej
def rules(res):
    D, p = res[:, 0], res[:, 1]
    return {"raw p<0.05": p < ALPHA,
            "Bonferroni": p < ALPHA / F,
            "Benjamini-Hochberg": bh(p),
            "share rule (>=10% drifted)": np.full(F, (p < ALPHA).mean() >= 0.10),
            "effect floor (p<0.05 and D>=0.15)": (p < ALPHA) & (D >= 0.15)}
for drifted in (0, 5):
    any_alert = {}; caught = {}; fa_feat = {}
    for _ in range(RUNS):
        for k, flags in rules(run_pvals(drifted)).items():
            any_alert[k] = any_alert.get(k, 0) + bool(flags.any())
            if drifted:
                caught[k] = caught.get(k, 0) + flags[:drifted].mean()
    print(f"\n{'NO drift' if drifted == 0 else '5 of 100 features truly drifted by 0.3 sigma'}: {RUNS} runs, n={N} per window")
    for k in any_alert:
        extra = f" | avg share of the 5 true drifts caught {caught[k]/RUNS:.2f}" if drifted else ""
        print(f"  {k:36s} runs with an alert: {any_alert[k]:3d}/{RUNS}{extra}")
print("\nexpected false alarms per run at 5% x 100 features:", 0.05 * 100)
```

**Output (my run):**
```text

NO drift: 200 runs, n=500 per window
  raw p<0.05                           runs with an alert: 200/200
  Bonferroni                           runs with an alert:   6/200
  Benjamini-Hochberg                   runs with an alert:   6/200
  share rule (>=10% drifted)           runs with an alert:   4/200
  effect floor (p<0.05 and D>=0.15)    runs with an alert:   1/200

5 of 100 features truly drifted by 0.3 sigma: 200 runs, n=500 per window
  raw p<0.05                           runs with an alert: 200/200 | avg share of the 5 true drifts caught 0.99
  Bonferroni                           runs with an alert: 198/200 | avg share of the 5 true drifts caught 0.70
  Benjamini-Hochberg                   runs with an alert: 199/200 | avg share of the 5 true drifts caught 0.83
  share rule (>=10% drifted)           runs with an alert:  96/200 | avg share of the 5 true drifts caught 0.48
  effect floor (p<0.05 and D>=0.15)    runs with an alert: 180/200 | avg share of the 5 true drifts caught 0.42

expected false alarms per run at 5% x 100 features: 5.0
```
Run with python3 -I in the numpy/scipy venv, seed 18. Simulated normal data only. Reading it: with no drift, the raw rule alarmed in all 200 runs. Bonferroni and BH alarmed in 6 of 200 (about 3 percent). With 5 truly drifted features (0.3 sigma), Bonferroni caught about 70 percent of them and BH about 83 percent, against 99 percent for raw. The effect floor kept false alarms low (1 of 200) but caught only 42 percent of the true drifts because D for a 0.3-sigma shift at n=500 is close to the floor. The share rule at 10 percent fired in 96 of 200 runs and caught under half. This is one setup, not a general ranking; the numbers move with shift size, n and correlation.

**Follow-ups:**
- *Which would you ship?* BH or an effect floor on a short list of important features, calibrated on stable history, with a share rule as a second signal.
- *Why does power fall?* A stricter threshold per test needs a bigger shift before the test fires.
- *Is the effect floor a correction?* No. It is a business filter on size, not a statistical control.

**Common mistakes:**
- One raw p-value per feature per day, then paging on any.
- Applying Bonferroni and not noticing the missed real drift.
- Treating p-values as importance.
- Not testing the rule on stable history.
- Ignoring the dependence between features.

### Q19 ⭐⭐ 🟡 Choosing the reference window and handling seasonality. Compare training data, a fixed golden window, a rolling previous window and same-period-last-year as the baseline, and what each catches and misses. Simulate a weekly and yearly pattern, show false alarms when a weekday batch is compared with a weekend reference, and show a day-of-week matched baseline removing them. Mention festival and month-end effects in Indian retail, lending and payments as examples, without inventing figures.
**Asked at:** MLOps interview question banks and guides (K21Academy '47 MLOps interview questions' PDF, Towards AI '101 ML LLM agentic AIOps interview questions', DataCamp MLOps interview questions, The Interview Guys MLOps post, wecreateproblems.com, hyring.com, dev.to vivekk101, a Medium skphd post; search snippets only, not opened; the Devinterview-io/mlops-interview-questions GitHub page WAS opened and has no dedicated monitoring or drift question, only monitoring bullets inside Q1, Q2, Q4, Q6, Q7 and Q12); editorial question lists, not verified candidate reports; MLOps, ML platform and ML engineer roles at IT-services firms, product companies and GCCs | Drift-test pitfall sources (Evidently blog 'data drift detection on large datasets' saying KS is too sensitive on large data, an Arize docs monitors page saying PSI is less sample-sensitive, an ICLR 2026 virtual-page submission 'When drift detectors cry wolf' on false-alarm rates with PSI unstable below about 200 samples and Bonferroni lowering power, a wikidocs PSI and KS guide; search snippets only, not opened; WebFetch of evidentlyai.com failed with getaddrinfo ENOTFOUND; sources partly conflict on PSI versus KS sensitivity); vendor docs and one conference submission, not interview reports; MLOps and data science roles
**Say this first (1 line):** The baseline decides what "drift" means, so I match it to the pattern I expect: day-of-week matched windows for weekly cycles, same period last year for yearly ones, and a fixed training baseline only for the question "has it moved away from what the model learned?".

**Then explain:**
- Training data: answers "is production different from what the model saw". It will alarm on any seasonal pattern the training window did not cover.
- Fixed golden window: stable and simple, but a single day or week can be unrepresentative, and it never follows legitimate change.
- Rolling previous window: adapts, so it catches sudden jumps and misses slow drift (the baseline moves with it), and it flips at weekday-weekend edges.
- Same period last year or last cycle: handles seasonality, but needs history and breaks when the calendar moves (festival dates change by the lunar calendar, check the calendar for the year).
- Indian examples, no figures: festival weeks in retail, salary-day and month-end peaks in lending and payments, quarter-end and tax-season effects. Build a calendar of known events and compare like with like.
- Failure modes: not enough matched history; a one-off holiday in the reference; a baseline built from a period that already contained the drift.

**Example:** Weekday basket value around 1000 and weekend around 1500, nothing else changing. Compare a Tuesday batch against a Saturday reference and you get a huge mismatch, so an alert. Compare it with earlier Tuesdays and there is none.

**Code:**
```python
import numpy as np, pandas as pd
from scipy.stats import ks_2samp
rng = np.random.default_rng(19)
days = pd.date_range("2026-01-01", periods=84, freq="D")   # 12 weeks
rows = []
for d in days:
    n = 400
    weekend = d.dayofweek >= 5
    # weekend traffic: higher basket value; no real drift anywhere
    x = rng.normal(1500 if weekend else 1000, 300, n)
    rows.append(pd.DataFrame({"date": d, "dow": d.dayofweek, "amt": x}))
df = pd.concat(rows, ignore_index=True)
ref_days = df[df.date < "2026-02-01"]          # first 4 weeks
test_days = df[df.date >= "2026-02-01"]
def alerts(baseline_fn):
    hits, total = 0, 0
    for d, g in test_days.groupby("date"):
        ref = baseline_fn(d)
        p = ks_2samp(ref.amt, g.amt).pvalue
        hits += p < 0.01; total += 1
    return hits, total
# 1) baseline = the previous calendar day (rolling): flips at weekend edges
roll = lambda d: df[df.date == d - pd.Timedelta(days=1)]
# 2) baseline = a single fixed Saturday (what a careless 'golden day' looks like)
sat = df[df.date == pd.Timestamp("2026-01-03")]
fixed_sat = lambda d: sat
# 3) baseline = same weekday in the reference window
matched = lambda d: ref_days[ref_days.dow == d.dayofweek]
for name, fn in [("previous day (rolling)", roll), ("one fixed Saturday", fixed_sat), ("day-of-week matched", matched)]:
    h, t = alerts(fn)
    print(f"{name:24s} alerts {h:2d} of {t} days (nothing really changed)")
# weekday batch vs weekend reference, shown directly
wk = df[df.date == "2026-02-10"]; we = df[df.date == "2026-01-03"]
print("Tue batch vs Saturday reference: KS p =", f"{ks_2samp(we.amt, wk.amt).pvalue:.2e}")
```

**Output (my run):**
```text
previous day (rolling)   alerts 16 of 53 days (nothing really changed)
one fixed Saturday       alerts 38 of 53 days (nothing really changed)
day-of-week matched      alerts  0 of 53 days (nothing really changed)
Tue batch vs Saturday reference: KS p = 3.26e-72
```
Run with python3 -I in the numpy/scipy/pandas venv, seed 19. Data is simulated: 84 days, 400 rows a day, a weekend effect built in and no real drift. The KS test at p<0.01 on 53 test days gave: 16 false alarm days against the previous day, 38 against one fixed Saturday, and 0 against the day-of-week matched baseline. The yearly pattern is described, not simulated here.

**Follow-ups:**
- *Matched baseline needs history, what if new?* Start with the training baseline and wider thresholds, switch to matched windows once you have a few cycles.
- *How do you handle a festival?* Add an event calendar, compare with the same event in the previous year, and suppress or mark alerts on known dates instead of silencing them for good.
- *Is a rolling window enough for slow drift?* No, add a slower comparison against a fixed baseline.

**Common mistakes:**
- One reference for all days.
- A golden window that happened to include an unusual event.
- Silencing alerts for the festival and never turning them back on.
- Using a baseline that moves with the drift.

### Q20 ⭐⭐ 🔴 Label (prior) shift versus covariate shift in practice. Explain how class prevalence can change while P(x|y) stays the same, why score and positive-rate monitors move, and how a monitor can estimate the new prevalence without labels using a confusion matrix from validation data. Simulate a prevalence change from 5 to 12 percent, recover the new prevalence with the confusion-matrix method, correct the decision threshold, and show where the assumption breaks. Book 1 owns the theory, so cite it only by a checked heading if at all.
**Asked at:** MLOps interview question banks and guides (K21Academy '47 MLOps interview questions' PDF, Towards AI '101 ML LLM agentic AIOps interview questions', DataCamp MLOps interview questions, The Interview Guys MLOps post, wecreateproblems.com, hyring.com, dev.to vivekk101, a Medium skphd post; search snippets only, not opened; the Devinterview-io/mlops-interview-questions GitHub page WAS opened and has no dedicated monitoring or drift question, only monitoring bullets inside Q1, Q2, Q4, Q6, Q7 and Q12); editorial question lists, not verified candidate reports; MLOps, ML platform and ML engineer roles at IT-services firms, product companies and GCCs | Expert extension: no source found for the exact question; the topic follows from the library behaviour tested in this sandbox and from general monitoring practice, and Wave B must verify against current docs; MLOps, ML platform and ML engineer roles, including IT-services firms, product companies and GCCs
**Say this first (1 line):** In label shift the class mix changes but P(x given y) stays the same, so the model's positive rate moves; I can estimate the new prevalence without labels from the live positive rate and the validation confusion rates, then correct the priors and threshold.

**Then explain:**
- Covariate shift: the inputs change, P(y given x) is assumed the same. Label (prior) shift: P(y) changes, P(x given y) is assumed the same. Example: fraud rate rises during a campaign, but fraud still looks the same.
- What moves: the score average and the positive rate go up, while the feature drift for individual features may look small. A positive-rate monitor catches it.
- Estimate: live positive rate q = pi x TPR + (1 - pi) x FPR, where TPR and FPR come from validation labels. So pi = (q - FPR) / (TPR - FPR). This is the confusion-matrix idea, often called black-box shift estimation.
- Correct: multiply the posterior odds by the ratio of new odds to old odds, then pick the threshold for the new prevalence and the cost trade-off.
- Where it breaks: P(x given y) also changed (new fraud pattern, new user mix), so TPR and FPR from old validation are wrong; TPR close to FPR makes the estimate unstable; small live samples add noise; a threshold rule with one fixed cost may need re-optimising, not just prior correction.

**Example:** Validation TPR 0.363, FPR 0.007, live positive rate 0.050. Hand check: (0.050 - 0.007) / (0.363 - 0.007) = 0.043 / 0.356 = 0.121. Close to the true 0.119.

**Code:**
```python
import numpy as np
from sklearn.linear_model import LogisticRegression
rng = np.random.default_rng(20)
def make(n, prev, shift=0.0):
    y = (rng.random(n) < prev).astype(int)
    x = rng.normal(0, 1, (n, 2)) + 1.5 * y[:, None] + shift * y[:, None]
    return x, y
xt, yt = make(20000, 0.05)                    # training prevalence 5%
xv, yv = make(20000, 0.05)                    # validation, same prevalence
clf = LogisticRegression(class_weight=None).fit(xt, yt)
thr = 0.5
# confusion rates on validation: TPR = P(pred=1|y=1), FPR = P(pred=1|y=0)
pv = clf.predict_proba(xv)[:, 1] >= thr
tpr, fpr = pv[yv == 1].mean(), pv[yv == 0].mean()
# live: prevalence 12%, no labels
xl, yl = make(20000, 0.12)
pl = clf.predict_proba(xl)[:, 1] >= thr
q = pl.mean()                                  # live positive rate
# q = pi*TPR + (1-pi)*FPR  ->  pi = (q - FPR)/(TPR - FPR)
pi_hat = (q - fpr) / (tpr - fpr)
print(f"validation positive rate {pv.mean():.3f}")
print(f"validation TPR {tpr:.3f} FPR {fpr:.3f}")
print(f"live positive rate {q:.3f} | true live prevalence {yl.mean():.3f} | estimated {pi_hat:.3f}")
# threshold correction: Bayes rule with new prior, posterior odds scale by (pi_new/(1-pi_new)) / (pi_old/(1-pi_old))
old, new = 0.05, pi_hat
p = clf.predict_proba(xl)[:, 1]
odds = p / (1 - p) * (new / (1 - new)) / (old / (1 - old))
p_adj = odds / (1 + odds)
print(f"mean score before {p.mean():.3f} after prior correction {p_adj.mean():.3f} (true prevalence {yl.mean():.3f})")
# if we want the same cost trade-off as before, the old 0.5 threshold on adjusted probabilities
print(f"positives flagged at 0.5: raw {np.mean(p >= .5):.3f}, adjusted {np.mean(p_adj >= .5):.3f}")
# where it breaks: P(x|y) also changes (covariate shift inside the positive class)
xs, ys = make(20000, 0.12, shift=-0.8)         # positives look weaker now
qs = (clf.predict_proba(xs)[:, 1] >= thr).mean()
print(f"BROKEN case: true prevalence {ys.mean():.3f}, estimate {(qs - fpr) / (tpr - fpr):.3f}  (P(x|y) moved, method assumes it did not)")
```

**Output (my run):**
```text
validation positive rate 0.025
validation TPR 0.363 FPR 0.007
live positive rate 0.050 | true live prevalence 0.119 | estimated 0.120
mean score before 0.075 after prior correction 0.119 (true prevalence 0.119)
positives flagged at 0.5: raw 0.050, adjusted 0.084
BROKEN case: true prevalence 0.124, estimate 0.025  (P(x|y) moved, method assumes it did not)
```
Run with python3 -I in the numpy/scikit-learn venv, seed 20. Simulated two-feature Gaussian data, a logistic regression trained at 5 percent prevalence, and a live set at 12 percent. The method recovered 0.120 against a true 0.119. In the broken case I weakened the positive class as well as raising prevalence, and the estimate came out at 0.025 against a true 0.124, so the assumption failure is silent: the formula still returns a plausible-looking number. The corrected posterior moved the mean score from 0.075 to 0.119, and the share flagged at 0.5 from 0.050 to 0.084. The point of that last line is that a fixed threshold gives the wrong volume after a prior shift; whether to change it is a cost decision.

**Follow-ups:**
- *How would you check the assumption?* When labels mature, compare TPR and FPR on live matured data with validation. If they moved, it is not pure label shift.
- *Why not just retrain?* You can, but a prior correction is cheap and works while labels are late.
- *Where is the theory?* Book 1 owns it; I would only cite it if I had a checked heading.

**Common mistakes:**
- Calling every positive-rate move "drift in x".
- Using the formula when TPR is close to FPR.
- Forgetting the estimate needs validation rates from the same model version.
- Re-tuning thresholds with no cost reasoning.

### Q21 ⭐⭐ 🟡 Wasserstein distance and Jensen-Shannon divergence for drift monitoring. Explain why Wasserstein is in feature units (so a threshold can be business-meaningful) and sensitive to the whole shape, why JS is symmetric and bounded and handles zero counts better than KL, and when to prefer each. Run both with scipy on shifts of different kinds and different units (income in rupees versus age in years), normalise sensibly, and show what a fixed threshold means for each. Note Evidently's defaults as seen in a local run.
**Asked at:** MLOps interview question banks and guides (K21Academy '47 MLOps interview questions' PDF, Towards AI '101 ML LLM agentic AIOps interview questions', DataCamp MLOps interview questions, The Interview Guys MLOps post, wecreateproblems.com, hyring.com, dev.to vivekk101, a Medium skphd post; search snippets only, not opened; the Devinterview-io/mlops-interview-questions GitHub page WAS opened and has no dedicated monitoring or drift question, only monitoring bullets inside Q1, Q2, Q4, Q6, Q7 and Q12); editorial question lists, not verified candidate reports; MLOps, ML platform and ML engineer roles at IT-services firms, product companies and GCCs | Drift-test pitfall sources (Evidently blog 'data drift detection on large datasets' saying KS is too sensitive on large data, an Arize docs monitors page saying PSI is less sample-sensitive, an ICLR 2026 virtual-page submission 'When drift detectors cry wolf' on false-alarm rates with PSI unstable below about 200 samples and Bonferroni lowering power, a wikidocs PSI and KS guide; search snippets only, not opened; WebFetch of evidentlyai.com failed with getaddrinfo ENOTFOUND; sources partly conflict on PSI versus KS sensitivity); vendor docs and one conference submission, not interview reports; MLOps and data science roles
**Say this first (1 line):** Wasserstein says how far the distribution has to move, in the feature's own units, so I can set a threshold a business person understands; Jensen-Shannon is a bounded, symmetric score on histograms that copes with empty bins, so I use it for categorical features and for a unit-free score.

**Then explain:**
- Wasserstein (earth mover's) distance: the average distance mass must be moved to turn one distribution into the other. For a pure shift it equals the shift: +2 years gives 2.0. It looks at the whole shape, not just the mean.
- Units matter. 2 in age is big, 2000 in rupees of income is small. Compare raw values across features only after dividing by something like the reference standard deviation, or set a threshold per feature in business units.
- Jensen-Shannon: a smoothed, symmetric version of KL, bounded (0 to 1 with log base 2 for the distance version in scipy, which returns the square root). It works on histograms or category shares. An empty bin does not blow it up; KL would divide by zero.
- JS on histograms depends on binning and has no units. It saturates when distributions barely overlap, so it stops telling you how big the move is.
- Prefer Wasserstein for continuous features with a meaningful scale, JS for categorical and for a quick bounded alarm. Evidently's defaults (seen in my Q15 run): normed Wasserstein for numeric and JS distance for categorical, both with threshold 0.1. Check current docs, defaults change.
- Failure modes: binning changes the JS value; a heavy tail can dominate Wasserstein; one threshold for all features is rarely right.

**Example:** Age +2 years: W = 2.00 years (0.25 reference standard deviations). Income +2000 rupees: W = 2066, but only 0.139 standard deviations. Judged in raw numbers, income looks 1000 times bigger; judged in standard deviations, age moved more.

**Code:**
```python
import numpy as np
from scipy.stats import wasserstein_distance
from scipy.spatial.distance import jensenshannon
rng = np.random.default_rng(21)
n = 20000
age_ref = rng.normal(35, 8, n); inc_ref = rng.normal(60000, 15000, n)
cases = {
 "age +2 years (mean shift)":      ("age", age_ref, age_ref + 2 + rng.normal(0, 0, n)),
 "age sd 8 -> 12 (spread change)": ("age", age_ref, rng.normal(35, 12, n)),
 "income +2000 rupees":            ("inc", inc_ref, rng.normal(62000, 15000, n)),
 "income +10000 rupees":           ("inc", inc_ref, rng.normal(70000, 15000, n)),
}
def js_hist(a, b, bins=20):
    edges = np.histogram_bin_edges(np.concatenate([a, b]), bins=bins)
    pa = np.histogram(a, edges)[0] + 1e-9; pb = np.histogram(b, edges)[0] + 1e-9   # tiny count avoids 0 bins
    return jensenshannon(pa / pa.sum(), pb / pb.sum(), base=2)   # distance (sqrt of divergence), 0..1
print(f"{'case':34s} {'W (raw units)':>14s} {'W/ref sd':>9s} {'JS (base 2)':>12s}")
for name, (_, a, b) in cases.items():
    w = wasserstein_distance(a, b)
    print(f"{name:34s} {w:14.2f} {w / a.std():9.3f} {js_hist(a, b):12.3f}")
# zero-count behaviour: KL would be infinite, JS stays finite
p = np.array([0.5, 0.5, 0.0]); q = np.array([0.4, 0.4, 0.2])
print("JS distance with an empty bin in p:", round(float(jensenshannon(p, q, base=2)), 3), "| KL(q||p) would divide by zero")
```

**Output (my run):**
```text
case                                W (raw units)  W/ref sd  JS (base 2)
age +2 years (mean shift)                    2.00     0.251        0.106
age sd 8 -> 12 (spread change)               3.22     0.403        0.228
income +2000 rupees                       2066.71     0.139        0.062
income +10000 rupees                     10095.37     0.677        0.277
JS distance with an empty bin in p: 0.329 | KL(q||p) would divide by zero
```
Run with python3 -I in the numpy/scipy venv, seed 21, n=20000 per sample, simulated normal data, 20 shared histogram bins for JS. In the table, "W/ref sd" is Wasserstein divided by the reference standard deviation, which is my choice of normalisation; Evidently's "normed" may differ in detail, so check its docs before comparing numbers. A fixed threshold of 0.2 on W/ref sd would fire on both age cases and on income +10000, but not on income +2000 (0.139); a threshold of 0.1 would fire on all four. The threshold is the decision, not the metric.

**Follow-ups:**
- *Why not KL?* It is asymmetric and infinite when one side has an empty bin.
- *Wasserstein for categoricals?* Only if the categories are ordered with a real distance; otherwise use JS or chi-square.
- *How do you pick the threshold?* From stable history and from the model's sensitivity, not from a default.

**Common mistakes:**
- Comparing raw Wasserstein across features with different units.
- Changing the bins between runs.
- Reading JS as "how much", after it saturates.
- Using one threshold everywhere.

### Q22 ⭐⭐ 🟡 Great Expectations versus pandera versus hand-written checks for data quality in ML pipelines. Say how each defines expectations, where it runs (in code, in a pipeline, in a data platform), what reports it gives, and how much setup it needs. Run the same four rules (non-null, range, allowed set, row count) in Great Expectations (ephemeral context, pandas dataframe asset) and pandera, record versions, show both outputs, and say what Data Docs, checkpoints and stores would add (not executed).
**Asked at:** MLOps interview question banks and guides (K21Academy '47 MLOps interview questions' PDF, Towards AI '101 ML LLM agentic AIOps interview questions', DataCamp MLOps interview questions, The Interview Guys MLOps post, wecreateproblems.com, hyring.com, dev.to vivekk101, a Medium skphd post; search snippets only, not opened; the Devinterview-io/mlops-interview-questions GitHub page WAS opened and has no dedicated monitoring or drift question, only monitoring bullets inside Q1, Q2, Q4, Q6, Q7 and Q12); editorial question lists, not verified candidate reports; MLOps, ML platform and ML engineer roles at IT-services firms, product companies and GCCs | Data-validation tool comparisons (pandera GitHub discussion 'Great Expectations vs Pandera #598', endjin.com comparison, a conventions page suggesting a freshness check at 2x expected cadence; search snippets only, not opened; nothing found on volume or freshness checks in Great Expectations itself); community comparisons, not interview reports; data and ML engineer roles
**Say this first (1 line):** Hand-written checks are fine for a few rules, pandera is the light in-code schema for dataframes, and Great Expectations is the heavier option when you want a shared rule library, validation results, reports and runs inside pipelines.

**Then explain:**
- Hand-written: a few lines of pandas that raise or log. No dependency, full control. You build the report, the history and the naming yourself, and rules drift apart across teams.
- pandera: a schema object in code (column types, nullable, checks, table-level checks). Validation returns a table of failure cases. Setup is small; it fits tests and pipeline steps.
- Great Expectations: expectations are named objects (an "expectation suite") run against a batch of data from a data source, with structured results. More concepts to set up (context, data source, asset, batch definition). Beyond what I ran, it supports Data Docs (HTML reports), checkpoints (run a validation and trigger actions) and stores (persist suites and results). Not executed here, and API names change between versions, check current docs.
- Where each runs: hand-written and pandera in the code path; Great Expectations in a pipeline step or a data platform job against files, dataframes or databases.
- Failure modes: schemas that only check types and miss business rules; checks that run on a sample; failing a pipeline for a warning-level issue; two copies of the same rule that disagree.

**Example:** Five loan rows. The row at index 2 has no age, index 3 has age 17, index 4 has age 130, index 3 also has status "paid" (not in open/closed set), and the table has only 5 rows against a minimum of 100. All three methods find the same row indexes.

**Code:**
```python
# ---- file: q22_ge.py ----
import great_expectations as gx, pandas as pd
print("great_expectations", gx.__version__, "pandas", pd.__version__)
df = pd.DataFrame({"loan_id": [1, 2, 3, 4, 5],
                   "age": [25, 40, None, 17, 130],
                   "status": ["open", "closed", "open", "paid", "open"]})
ctx = gx.get_context(mode="ephemeral")
asset = ctx.data_sources.add_pandas("src").add_dataframe_asset("loans")
batch = asset.add_batch_definition_whole_dataframe("whole").get_batch(batch_parameters={"dataframe": df})
exps = {
 "non-null age":   gx.expectations.ExpectColumnValuesToNotBeNull(column="age"),
 "age range 18-100": gx.expectations.ExpectColumnValuesToBeBetween(column="age", min_value=18, max_value=100),
 "status allowed": gx.expectations.ExpectColumnValuesToBeInSet(column="status", value_set=["open", "closed"]),
 "row count 100+": gx.expectations.ExpectTableRowCountToBeBetween(min_value=100),
}
for name, e in exps.items():
    r = batch.validate(e)
    res = r.result
    print(f"{name:18s} success={r.success!s:5s} unexpected_count={res.get('unexpected_count', res.get('observed_value'))} "
          f"values={res.get('partial_unexpected_list', '')} idx={res.get('partial_unexpected_index_list', '')}")

# ---- file: q22_pandera.py ----
import pandas as pd, pandera, pandera.pandas as pa
print("pandera", pandera.__version__, "pandas", pd.__version__)
df = pd.DataFrame({"loan_id": [1, 2, 3, 4, 5],
                   "age": [25, 40, None, 17, 130],
                   "status": ["open", "closed", "open", "paid", "open"]})
schema = pa.DataFrameSchema(
    {"age": pa.Column(float, [pa.Check.in_range(18, 100)], nullable=False),       # non-null + range
     "status": pa.Column(str, pa.Check.isin(["open", "closed"]))},               # allowed set
    checks=pa.Check(lambda d: len(d) >= 100, error="row count must be >= 100"),  # table-level check
    coerce=True)
try:
    schema.validate(df, lazy=True)
except pa.errors.SchemaErrors as e:
    print(e.failure_cases[["schema_context", "column", "check", "failure_case", "index"]].to_string())

# ---- file: q22_handwritten.py ----
import pandas as pd
df = pd.DataFrame({"loan_id": [1, 2, 3, 4, 5], "age": [25, 40, None, 17, 130], "status": ["open", "closed", "open", "paid", "open"]})
errs = []
if df.age.isna().any(): errs.append(("non-null age", df.index[df.age.isna()].tolist()))
bad = df[df.age.notna() & ~df.age.between(18, 100)]
if len(bad): errs.append(("age range 18-100", bad.index.tolist()))
bad = df[~df.status.isin(["open", "closed"])]
if len(bad): errs.append(("status allowed", bad.index.tolist()))
if len(df) < 100: errs.append(("row count >= 100", [len(df)]))
for e in errs: print(e)
```

**Output (my run):**
```text
great_expectations 1.24.1 pandas 3.1.0
non-null age       success=False unexpected_count=1 values=[nan] idx=[2]
age range 18-100   success=False unexpected_count=2 values=[17.0, 130.0] idx=[3, 4]
status allowed     success=False unexpected_count=1 values=['paid'] idx=[3]
row count 100+     success=False unexpected_count=5 values= idx=
```
```text
pandera 0.35.0 pandas 3.1.0
    schema_context  column                     check failure_case index
4  DataFrameSchema    None  row count must be >= 100        False  None
0           Column     age              not_nullable          NaN     2
1           Column     age         in_range(18, 100)         17.0     3
2           Column     age         in_range(18, 100)        130.0     4
3           Column  status  isin(['open', 'closed'])         paid     3
```
```text
('non-null age', [2])
('age range 18-100', [3, 4])
('status allowed', [3])
('row count >= 100', [5])
```
Versions: great-expectations 1.24.1 (ephemeral context, pandas dataframe asset, whole-dataframe batch), pandera 0.35.0 (installed with the pandas extra), pandas 3.1.0, each in its own venv. All three found the same rows: null age at index 2, out-of-range ages at 3 and 4, a disallowed status at index 3, and the row-count failure. Differences I saw: Great Expectations returned a result per expectation and listed unexpected values and indexes (for the row count, the figure shown is the observed row count of 5, not an unexpected-row count); its range check ignored the null, so null and range are separate expectations; pandera returned one failure table in lazy mode, with the table-level check showing a `False` failure case and no index. Data Docs, checkpoints and stores: not executed; I only ran validations through the in-memory context.

**Follow-ups:**
- *Which would you pick?* pandera or hand-written for a small service, Great Expectations when several teams need shared rules and reports.
- *Where do the rules come from?* From the data owner and from profiling stable history, then reviewed. Do not auto-generate and trust.
- *Fail the pipeline or warn?* Fail for broken contracts (schema, nulls in required fields), warn for soft ranges.

**Common mistakes:**
- Only checking types.
- Rules living in a notebook.
- Failing hard on everything, so people disable the check.
- Not versioning the rules with the model.

### Q23 ⭐⭐ 🟡 Freshness and volume monitors. Explain how you decide a table is stale (max event time versus load time, expected cadence), how to set volume bounds that survive weekends, holidays and growth, and the failure where data arrives late but complete. Implement freshness and a seasonally-aware volume check with pandas, run on simulated daily counts with a missing partition, a half-size partition and a late partition, and show the alerts. Part 5 owns scheduling and sensors.
**Asked at:** MLOps interview question banks and guides (K21Academy '47 MLOps interview questions' PDF, Towards AI '101 ML LLM agentic AIOps interview questions', DataCamp MLOps interview questions, The Interview Guys MLOps post, wecreateproblems.com, hyring.com, dev.to vivekk101, a Medium skphd post; search snippets only, not opened; the Devinterview-io/mlops-interview-questions GitHub page WAS opened and has no dedicated monitoring or drift question, only monitoring bullets inside Q1, Q2, Q4, Q6, Q7 and Q12); editorial question lists, not verified candidate reports; MLOps, ML platform and ML engineer roles at IT-services firms, product companies and GCCs | Data-validation tool comparisons (pandera GitHub discussion 'Great Expectations vs Pandera #598', endjin.com comparison, a conventions page suggesting a freshness check at 2x expected cadence; search snippets only, not opened; nothing found on volume or freshness checks in Great Expectations itself); community comparisons, not interview reports; data and ML engineer roles
**Say this first (1 line):** Freshness asks "is the newest data as new as it should be", volume asks "is the row count normal for this weekday", and I also check late loads separately, because data that arrives late but complete still broke the model run that happened before it arrived.

**Then explain:**
- Freshness: compare the newest event time (not just load time) with now, against the expected cadence plus a slack. Event time stale means the upstream stopped; load time fine with old event time means a job re-loaded old data.
- Volume: compare each partition with a band for the same weekday, built from history with a robust centre and spread (median and median absolute deviation). A single global band hides weekends and half-size days. Re-fit as the business grows, and treat known holidays and campaign days with a calendar.
- Missing partitions are their own alert; a missing day is not just "volume zero".
- Late but complete: the partition has the right rows but landed after the consumer already ran. Track load delay per partition against its due time, and make downstream jobs wait or rerun.
- Part 5 owns scheduling and sensors, so here only the check logic.
- Failure modes: the band learns from a history that already contained an outage; the freshness SLA is longer than the model's tolerance; timezone mistakes (UTC versus IST day boundaries).

**Example:** History says Fridays are about 10000 rows (band about 7900 to 12200 here) and Saturdays about 5900. A Friday with 4923 rows is far under its band. A global mean-and-sd band would put the same 4923 comfortably inside. Hand check: half of 9846 is 4923.

**Code:**
```python
import numpy as np, pandas as pd
rng = np.random.default_rng(23)
days = pd.date_range("2026-08-01", "2026-10-25", freq="D")
base = np.where(days.dayofweek >= 5, 6000, 10000)          # weekends are lower
cnt = (base * rng.normal(1, 0.03, len(days))).round().astype(int)
df = pd.DataFrame({"event_date": days, "rows": cnt})
# load time per partition: normally 02:00 next day
df["loaded_at"] = df.event_date + pd.Timedelta(days=1, hours=2)
# inject problems in the last days
now = pd.Timestamp("2026-10-26 12:00")
df = df[df.event_date != "2026-10-22"]                           # missing partition
df.loc[df.event_date == "2026-10-23", "rows"] //= 2              # half-size partition (a Friday)
df.loc[df.event_date == "2026-10-24", "loaded_at"] += pd.Timedelta(hours=30)   # late but complete
df["dow"] = df.event_date.dt.dayofweek
hist = df[df.event_date < "2026-10-15"]
# seasonal band: same weekday, median and MAD-based band
stats = hist.groupby("dow")["rows"].agg(med="median", mad=lambda s: (s - s.median()).abs().median())
def checks(df, now, expected_cadence=pd.Timedelta(days=1), sla=pd.Timedelta(hours=6), k=8):
    out = []
    # freshness: newest event_date vs now; allow cadence + SLA slack
    newest = df.event_date.max()
    lag = now - (newest + pd.Timedelta(days=1))          # how old is the newest data
    if lag > expected_cadence + sla: out.append(f"STALE: newest partition {newest.date()}, data is {lag} old (allowed {expected_cadence + sla})")
    # missing partitions in the recent window
    want = pd.date_range("2026-10-15", "2026-10-25")
    for d in want.difference(df.event_date): out.append(f"MISSING partition {d.date()}")
    for _, r in df[df.event_date >= "2026-10-15"].iterrows():
        s = stats.loc[r.dow]; lo, hi = s.med - k * max(s.mad, 1), s.med + k * max(s.mad, 1)
        if not lo <= r.rows <= hi:
            out.append(f"VOLUME {r.event_date.date()} rows={r.rows} outside [{lo:.0f}, {hi:.0f}] for weekday {r.dow}")
        delay = r.loaded_at - (r.event_date + pd.Timedelta(days=1, hours=2))
        if delay > sla: out.append(f"LATE-LOAD {r.event_date.date()} loaded {delay} after due time (rows look complete: {r.rows})")
    return out
print("history weekday bands (median, MAD):"); print(stats.round(0).to_string())
print("--- run at", now)
for a in checks(df, now): print(a)
now2 = pd.Timestamp("2026-10-28 12:00")
print("--- same table, run at", now2, "(no new partition arrived)")
for a in checks(df, now2): print(a)
# a naive global band would flag every weekend:
g = hist.rows; lo, hi = g.median() - 3 * g.std(), g.median() + 3 * g.std()
wk = df[(df.event_date >= "2026-10-15") & (df.dow >= 5)]
print(f"\nnaive global band [{lo:.0f}, {hi:.0f}]; weekend rows in recent window: {wk.rows.tolist()} (all inside? {bool(wk.rows.between(lo, hi).all())})")
print("half-size Friday rows", int(df[df.event_date=='2026-10-23'].rows.iloc[0]), "inside the naive global band?", bool(lo <= df[df.event_date=='2026-10-23'].rows.iloc[0] <= hi))
```

**Output (my run):**
```text
history weekday bands (median, MAD):
         med    mad
dow                
0    10034.0  112.0
1     9823.0  308.0
2     9872.0  144.0
3     9999.0  268.0
4    10028.0  270.0
5     5899.0  118.0
6     6039.0  110.0
--- run at 2026-10-26 12:00:00
MISSING partition 2026-10-22
VOLUME 2026-10-23 rows=4923 outside [7864, 12192] for weekday 4
LATE-LOAD 2026-10-24 loaded 1 days 06:00:00 after due time (rows look complete: 6205)
--- same table, run at 2026-10-28 12:00:00 (no new partition arrived)
STALE: newest partition 2026-10-25, data is 2 days 12:00:00 old (allowed 1 days 06:00:00)
MISSING partition 2026-10-22
VOLUME 2026-10-23 rows=4923 outside [7864, 12192] for weekday 4
LATE-LOAD 2026-10-24 loaded 1 days 06:00:00 after due time (rows look complete: 6205)

naive global band [4222, 15344]; weekend rows in recent window: [5935, 5922, 6205, 5814] (all inside? True)
half-size Friday rows 4923 inside the naive global band? True
```
Run with python3 -I in the numpy/pandas venv (pandas 3.1.0), seed 23, simulated daily counts: weekdays about 10000, weekends about 6000, 3 percent noise. Injected: Oct 22 partition missing, Oct 23 cut to half, Oct 24 loaded 30 hours late with a normal row count. The band uses k=8 times the MAD with a floor of 1, which is my choice for the demo, not a standard. Every injected problem was caught. The second run, with no new partition for two more days, fires the stale alert; the first run correctly does not, since the newest partition was within the allowed lag. Last line: the naive global band lets both the weekends and the half-size Friday pass.

**Follow-ups:**
- *Holidays?* Keep a calendar of known low and high days and compare to the same event in earlier years, or mark those partitions as expected-different.
- *Growth?* Use a recent window per weekday, or a trend-adjusted band, and re-fit on a schedule.
- *Late data after the model already ran?* Rerun or backfill when the partition lands, and record which runs used incomplete data.

**Common mistakes:**
- One global threshold.
- Checking load time only.
- Treating a missing partition as a volume of zero.
- A band learned from a history with outages in it.
- Mixing time zones.

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

### Q35 ⭐ 🔴 Monitoring models on unstructured data (images, text, embeddings) at the Part 8 level. Explain drift on embeddings with distance to a reference centroid, a domain classifier (can a classifier tell reference from production, AUC near 0.5 or not), and simple metadata drift (image size, text length, language mix). Run a domain classifier on simulated embeddings with and without shift and show the AUC. Prompt, retrieval and answer-quality monitoring for LLM systems belong to Book 2, so only name the boundary.
**Asked at:** MLOps interview question banks and guides (K21Academy '47 MLOps interview questions' PDF, Towards AI '101 ML LLM agentic AIOps interview questions', DataCamp MLOps interview questions, The Interview Guys MLOps post, wecreateproblems.com, hyring.com, dev.to vivekk101, a Medium skphd post; search snippets only, not opened; the Devinterview-io/mlops-interview-questions GitHub page WAS opened and has no dedicated monitoring or drift question, only monitoring bullets inside Q1, Q2, Q4, Q6, Q7 and Q12); editorial question lists, not verified candidate reports; MLOps, ML platform and ML engineer roles at IT-services firms, product companies and GCCs | Expert extension: no source found for the exact question; the topic follows from the library behaviour tested in this sandbox and from general monitoring practice, and Wave B must verify against current docs; MLOps, ML platform and ML engineer roles, including IT-services firms, product companies and GCCs
**Say this first (1 line):** For embeddings I do not run a test per dimension; I ask "can a classifier tell reference from production?" (AUC near 0.5 means no, near 1 means yes), and I back it with centroid distance and cheap metadata drift like text length or image size.

**Then explain:**
- **Why not per-dimension tests:** a 768-dim embedding has no meaning per axis, and 768 KS tests give false alarms. Use one score for the whole vector.
- **Centroid distance:** distance between the mean embedding of reference and of today, scaled by the reference spread. Cheap, one number, good for a trend line. It misses shape changes where the mean stays put.
- **Domain classifier:** label reference 0 and production 1, cross-validate a simple model, read the AUC. About 0.5 is "cannot tell apart". Higher is "different", and the model's top features or misclassified rows show where.
- **Metadata drift:** text length, language mix, image width and height, file type, null rate. Boring but catches broken upstream pipelines the embedding hides (for example a resized image).
- **Failure modes:** a new embedding model version changes every vector (always compare same-version embeddings); small batches give noisy AUC; a flag tells you "different", not "worse", so pair it with a quality or label check. Prompt, retrieval and answer-quality monitoring for LLM systems is Book 2; this answer stops at the input side.

**Example:** 32-dim embeddings, 1000 rows each. Only 4 of the 32 dims are shifted. The per-dim shift is invisible by eye, but the domain AUC climbs from 0.505 (no shift) to 0.666 (shift 0.3) to 0.915 (shift 1.0). Text length (Poisson mean 40 to 55) is flagged by plain KS.

**Code:** (seeded; `python3 -I`)
```py
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import roc_auc_score
from scipy.stats import ks_2samp

rng = np.random.default_rng(35)
D, N = 32, 1000
def emb(n, shift=0.0):
    x = rng.normal(0, 1, (n, D))
    x[:, :4] += shift            # shift only 4 of 32 dims
    return x
ref = emb(N)
def centroid_dist(ref, cur):     # distance between mean vectors, scaled by ref spread
    return float(np.linalg.norm(cur.mean(0) - ref.mean(0)) / np.sqrt(D))
def domain_auc(ref, cur):
    X = np.vstack([ref, cur]); y = np.r_[np.zeros(len(ref)), np.ones(len(cur))]
    p = cross_val_predict(LogisticRegression(max_iter=500), X, y, cv=5, method="predict_proba")[:, 1]
    return float(roc_auc_score(y, p))
for name, shift in [("no shift", 0.0), ("small shift 0.3", 0.3), ("shift 1.0", 1.0)]:
    cur = emb(N, shift)
    print(f"{name:16s} centroid_dist={centroid_dist(ref,cur):.3f}  domain_AUC={domain_auc(ref,cur):.3f}")
# metadata drift: text length (tokens), same embeddings
len_ref = rng.poisson(40, N); len_cur = rng.poisson(55, N)
print("text length KS D=%.3f p=%.2g" % ks_2samp(len_ref, len_cur))
```

**Output (my run):** Python 3.13, numpy 2.5.4, scipy 1.18.1, pandas 3.1.0, scikit-learn 1.9.1, pytest 9.1.1, PyYAML 6.0.3 (sandbox; numbers are from these seeded runs).
```text
no shift         centroid_dist=0.044  domain_AUC=0.505
small shift 0.3  centroid_dist=0.118  domain_AUC=0.666
shift 1.0        centroid_dist=0.344  domain_AUC=0.915
text length KS D=0.728 p=6.1e-257
```

**Follow-ups:**
- *What if the domain classifier says AUC 0.9 but metrics are fine?* The shift may not touch what the model uses. Log it, check a labelled sample, do not auto-retrain.
- *Why cross-validate?* Scoring the classifier on its own training rows always looks great; AUC must be on held-out rows.
- *Distances in high dimensions?* Distances concentrate; prefer cosine or a PCA-reduced space, and keep the classifier as the main signal.

**Common mistakes:** per-dimension KS on every axis; mixing embeddings from two model versions; reading AUC on training rows; treating "drift" as "bad"; forgetting metadata checks.

### Q36 ⭐ 🔴 Multivariate drift that univariate tests miss. Show an example where each feature's marginal is unchanged but the correlation flips, explain PCA reconstruction error, a domain classifier, and a pairwise-correlation check, and how to choose among them. Simulate it, run per-feature KS (quiet) against the domain classifier and the correlation diff (loud), and say what the loud detectors cannot tell you (which feature changed).
**Asked at:** Expert extension: no source found for the exact question; the topic follows from the library behaviour tested in this sandbox and from general monitoring practice, and Wave B must verify against current docs; MLOps, ML platform and ML engineer roles, including IT-services firms, product companies and GCCs
**Say this first (1 line):** Per-feature tests look only at one column at a time, so they miss a change in how features relate; I add a domain classifier, a PCA reconstruction error and a pairwise-correlation diff, which are loud when the marginals are quiet.

**Then explain:**
- **The blind spot:** two features can each stay N(0,1) while their correlation flips from +0.8 to -0.8. Every KS test passes, the joint distribution is totally different.
- **Correlation diff:** compare the correlation matrix to the reference. Cheap, readable ("x0 and x1 now move opposite"), but only sees linear pairs.
- **PCA reconstruction error:** fit PCA on reference, reconstruct production with the same components, watch the error. Rising error means production sits off the old structure. Linear again.
- **Domain classifier:** any model that can separate the two windows. A tree model sees non-linear changes too. Most general, and the most expensive to keep running.
- **Choosing:** daily and cheap, correlation diff plus PCA error. When one fires, or on a weekly cadence, run the domain classifier. Per-feature KS stays on, for single-column faults.
- **What the loud ones cannot say:** which feature changed. All of them only say "the joint changed". To localise: look at the pairwise cell with the biggest diff, or the classifier's feature importance; neither is proof of a cause.
- **Failure mode:** with many features, correlation diffs multiply (p features give p(p-1)/2 pairs), so set the threshold from a bootstrap (Q38).

**Example:** 2000 rows each, reference corr +0.81, production -0.79. KS p-values 0.53 and 0.46 (quiet). Random-forest domain AUC 0.893, correlation difference 1.60, PCA(1) error 0.188 to 1.781. In a control with no change the AUC is 0.512, corr diff 0.002 and errors 0.197 vs 0.202.

**Code:** (seeded; `python3 -I`)
```py
import numpy as np
from scipy.stats import ks_2samp
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import roc_auc_score
from sklearn.decomposition import PCA

rng = np.random.default_rng(36)
n = 2000
def make(rho):
    cov = [[1, rho], [rho, 1]]
    return rng.multivariate_normal([0, 0], cov, n)
ref, cur = make(0.8), make(-0.8)   # marginals identical N(0,1), correlation flips
for j in range(2):
    D, p = ks_2samp(ref[:, j], cur[:, j])
    print(f"per-feature KS x{j}: D={D:.3f} p={p:.2f}")
# domain classifier (non-linear, so it can see the correlation)
X = np.vstack([ref, cur]); y = np.r_[np.zeros(n), np.ones(n)]
pr = cross_val_predict(RandomForestClassifier(100, min_samples_leaf=20, random_state=0), X, y, cv=5, method="predict_proba")[:, 1]
print("domain classifier AUC: %.3f" % roc_auc_score(y, pr))
# correlation diff
c0, c1 = np.corrcoef(ref.T)[0, 1], np.corrcoef(cur.T)[0, 1]
print(f"corr ref={c0:.3f} cur={c1:.3f} abs diff={abs(c1-c0):.3f}")
# PCA reconstruction error: fit on ref, 1 component
pca = PCA(1).fit(ref)
def rec_err(x): return float(np.mean(np.sum((x - pca.inverse_transform(pca.transform(x)))**2, axis=1)))
print(f"PCA(1) recon error ref={rec_err(ref):.3f} cur={rec_err(cur):.3f}")
# control: no change at all
ref2, cur2 = make(0.8), make(0.8)
pr2 = cross_val_predict(RandomForestClassifier(100, min_samples_leaf=20, random_state=0), np.vstack([ref2, cur2]), y, cv=5, method="predict_proba")[:, 1]
print("control (no change) domain AUC: %.3f  corr diff %.3f  recon %.3f vs %.3f" % (
    roc_auc_score(y, pr2), abs(np.corrcoef(cur2.T)[0,1]-np.corrcoef(ref2.T)[0,1]), rec_err(ref2), rec_err(cur2)))
```

**Output (my run):** Python 3.13, numpy 2.5.4, scipy 1.18.1, pandas 3.1.0, scikit-learn 1.9.1, pytest 9.1.1, PyYAML 6.0.3 (sandbox; numbers are from these seeded runs).
```text
per-feature KS x0: D=0.026 p=0.53
per-feature KS x1: D=0.027 p=0.46
domain classifier AUC: 0.893
corr ref=0.808 cur=-0.794 abs diff=1.602
PCA(1) recon error ref=0.188 cur=1.781
control (no change) domain AUC: 0.512  corr diff 0.002  recon 0.197 vs 0.202
```

**Follow-ups:**
- *Why a random forest and not logistic regression?* A linear model on (x0, x1) cannot separate a flipped correlation; a tree model can. Pick a classifier that matches the shapes you worry about.
- *Does the model care?* Check feature-pair interactions in the model; a flipped correlation hurts a model that relies on the pair, and may do nothing to one that does not.

**Common mistakes:** trusting green per-feature KS as "no drift"; running a linear domain classifier and calling the joint "fine"; expecting these detectors to name the culprit.

### Q37 ⭐ 🔴 Online change detection on a metric stream: CUSUM, Page-Hinkley and an adaptive window idea (ADWIN at concept level). Explain the delay versus false-alarm trade-off, the parameters (drift allowance and threshold), and why they suit a slow-moving error rate better than repeated KS tests. Implement CUSUM and Page-Hinkley with numpy, run on a stream with a step change and with noise only, report detection delay and false alarms over 200 seeds. Part 9 owns streaming infrastructure.
**Asked at:** Expert extension: no source found for the exact question; the topic follows from the library behaviour tested in this sandbox and from general monitoring practice, and Wave B must verify against current docs; MLOps, ML platform and ML engineer roles, including IT-services firms, product companies and GCCs
**Say this first (1 line):** CUSUM and Page-Hinkley keep a running sum of "how far above normal, minus an allowance", and alarm when the sum crosses a threshold; that finds a small, lasting rise in an error rate much faster than repeating a KS test on windows.

**Then explain:**
- **CUSUM:** `s = max(0, s + z - k)`; alarm when `s > h`. `k` is the drift allowance (ignore wobble smaller than about k sd), `h` is the threshold.
- **Page-Hinkley:** same idea with a running mean as reference: accumulate `z - mean - delta`, alarm when the sum rises `lam` above its running minimum.
- **ADWIN (concept only, not implemented here):** keeps a window that grows while data is stable and drops the old part when two sub-windows have different means. It adapts the window so you do not pick one.
- **The trade-off:** a low threshold finds changes sooner and fires on noise more; a high threshold is quiet and slow. The "average run length" between false alarms and the detection delay move in opposite directions.
- **Why not repeated KS:** each KS test uses a fixed window, tests again and again (more chances to false-alarm), and is slow for a slow shift; a cumulative sum uses every point since the change.
- **Failure modes:** parameters are in units of the baseline sd, so a wrong baseline mean or sd means wrong alarms; reset the sum after an alarm; for stream infrastructure see Part 9.

**Example:** baseline 0.10, sd 0.02, a +1 sd step (0.12) at t=300, 600 points, 200 seeds. `h=5` is too jumpy (94/200 noise-only runs alarm). `h=8` gives 5/200 false alarms and a median delay of 14 points; Page-Hinkley `lam=15` gives 0/200 false alarms with a median delay of 31.5.

**Code:** (seeded, numpy only; `python3 -I`)
```py
import numpy as np
# Stream: daily error rate-like metric, baseline mean 0.10, sd 0.02; step to 0.12 at t=300 (1 sd).
MU, SD, T, STEP_AT, STEP = 0.10, 0.02, 600, 300, 0.02

def cusum(x, k=0.5, h=5.0):
    """Upper CUSUM on standardised values. k = drift allowance (in sd), h = threshold (in sd). Returns first alarm index or None."""
    s = 0.0
    for i, v in enumerate(x):
        z = (v - MU) / SD
        s = max(0.0, s + z - k)
        if s > h: return i
    return None

def page_hinkley(x, delta=0.5, lam=8.0):
    """Page-Hinkley for an increase. delta = tolerated drift (in sd), lam = threshold (in sd). Running mean as the reference."""
    m, cum, cum_min = 0.0, 0.0, 0.0
    for i, v in enumerate(x):
        z = (v - MU) / SD
        m += (z - m) / (i + 1)
        cum += z - m - delta
        cum_min = min(cum_min, cum)
        if cum - cum_min > lam: return i
    return None

def run(detector, **kw):
    delays, fa_noise, pre = [], 0, 0
    for seed in range(200):
        r = np.random.default_rng(seed)
        noise = r.normal(MU, SD, T)
        fa_noise += detector(noise, **kw) is not None       # noise-only stream: any alarm is false
        shifted = noise.copy(); shifted[STEP_AT:] += STEP    # same noise plus a step at t=300
        a = detector(shifted, **kw)
        if a is not None and a < STEP_AT: pre += 1           # alarmed before the step: false alarm
        elif a is not None: delays.append(a - STEP_AT)
    return np.median(delays), len(delays), fa_noise, pre

print("noise-only: 600 points. step run: +1 sd (0.02) at t=300. 200 seeds.")
for name, det, kws in [("CUSUM k=0.5 h=5", cusum, dict(k=0.5, h=5.0)),
                       ("CUSUM k=0.5 h=8", cusum, dict(k=0.5, h=8.0)),
                       ("PageHinkley d=0.5 lam=8", page_hinkley, dict(delta=0.5, lam=8.0)),
                       ("PageHinkley d=0.5 lam=15", page_hinkley, dict(delta=0.5, lam=15.0))]:
    med, n, fa, pre = run(det, **kws)
    print(f"{name:26s} false alarms (noise-only)={fa:3d}/200  alarmed before step={pre:3d}/200  detected after step={n:3d}/200  median delay={med:.1f} points")
```

**Output (my run):** Python 3.13, numpy 2.5.4, scipy 1.18.1, pandas 3.1.0, scikit-learn 1.9.1, pytest 9.1.1, PyYAML 6.0.3 (sandbox; numbers are from these seeded runs). Delay is measured only on runs that had not already alarmed before the step, so it is slightly flattering for the jumpy settings.
```text
noise-only: 600 points. step run: +1 sd (0.02) at t=300. 200 seeds.
CUSUM k=0.5 h=5            false alarms (noise-only)= 94/200  alarmed before step= 56/200  detected after step=144/200  median delay=8.0 points
CUSUM k=0.5 h=8            false alarms (noise-only)=  5/200  alarmed before step=  3/200  detected after step=197/200  median delay=14.0 points
PageHinkley d=0.5 lam=8    false alarms (noise-only)=  6/200  alarmed before step=  3/200  detected after step=197/200  median delay=15.0 points
PageHinkley d=0.5 lam=15   false alarms (noise-only)=  0/200  alarmed before step=  0/200  detected after step=200/200  median delay=31.5 points
```

**Follow-ups:**
- *How do you pick h?* Simulate noise-only streams (as above) to hit a target false-alarm rate, then read the delay you get.
- *Two-sided?* Run one CUSUM for up and one for down.
- *Seasonal metric?* De-trend or compare to the same weekday first, or the weekly cycle looks like drift.

**Common mistakes:** k and h copied from a blog without matching your units; never resetting after an alarm; using it on a metric whose baseline is not stable; claiming a delay number without reporting false alarms next to it.

### Q38 ⭐ 🔴 Calibrating drift thresholds from history instead of rules of thumb. Explain bootstrapping the reference to get a null distribution of PSI or KS D for your batch size, choosing a threshold for a target false-alarm rate, and backtesting on past incidents. Implement it with numpy, run for batch sizes 200, 2000 and 20000, show that the same 0.1 PSI means different things at each, and show the chosen thresholds. Say how seasonality and multiple features change the answer.
**Asked at:** Drift-test pitfall sources (Evidently blog 'data drift detection on large datasets' saying KS is too sensitive on large data, an Arize docs monitors page saying PSI is less sample-sensitive, an ICLR 2026 virtual-page submission 'When drift detectors cry wolf' on false-alarm rates with PSI unstable below about 200 samples and Bonferroni lowering power, a wikidocs PSI and KS guide; search snippets only, not opened; WebFetch of evidentlyai.com failed with getaddrinfo ENOTFOUND; sources partly conflict on PSI versus KS sensitivity); vendor docs and one conference submission, not interview reports; MLOps and data science roles | Expert extension: no source found for the exact question; the topic follows from the library behaviour tested in this sandbox and from general monitoring practice, and Wave B must verify against current docs; MLOps, ML platform and ML engineer roles, including IT-services firms, product companies and GCCs
**Say this first (1 line):** I do not use "PSI above 0.1"; I draw many clean batches of my real batch size from history, see what PSI or KS D looks like when nothing changed, and set the threshold at the level that gives me my target false-alarm rate.

**Then explain:**
- **Why a fixed number fails:** PSI on small batches is noisy. At n=200 a clean batch exceeds 0.1 about 3 percent of the time; at n=2000 or 20000 never. 0.1 is a rule of thumb from credit scoring, not a standard.
- **Method:** bootstrap batches of size n from the reference, compute the statistic each time, take the 95th or 99th percentile as threshold. That is the null distribution for this batch size.
- **Backtest:** replay past days and past incidents through the chosen threshold. Count false alarms on known-quiet days and hits on known incidents. Adjust the percentile, not the story.
- **Many features:** with 50 features at a 1 percent per-feature rate you expect at least one alarm on 39.5 percent of days. Use a stricter per-feature level (about 0.0002 for a 1 percent daily rate over 50 independent features), or alert on "how many features moved".
- **Seasonality:** build the reference from the same weekday or season, or the null distribution itself is too narrow and every Monday alarms.
- **Failure modes:** a null built from a reference that already contains drift; bootstrapping with replacement from a tiny reference; a high threshold that no longer catches a real 0.15 sigma shift (check power as well).

**Example:** n=200 gives a PSI null p99 of 0.1217; n=2000 gives 0.0111; n=20000 gives 0.0010. The same 0.1 means "almost the noise ceiling" at 200 and "huge" at 20000. At n=2000 a threshold of 0.0114 had 1.5 percent false alarms on fresh clean batches and caught a 0.15-sigma shift 99 percent of the time.

**Code:** (seeded, numpy and scipy; `python3 -I`)
```py
import numpy as np
from scipy.stats import ks_2samp

rng = np.random.default_rng(38)
ref = rng.normal(0, 1, 50000)                       # history: a large, clean reference
edges = np.quantile(ref, np.linspace(0, 1, 11)); edges[0], edges[-1] = -np.inf, np.inf  # 10 reference-quantile bins
ref_p = np.full(10, 0.1)

def psi(x):
    c = np.histogram(x, edges)[0] / len(x)
    c = np.clip(c, 1e-4, None)
    return float(np.sum((c - ref_p) * np.log(c / ref_p)))

B = 1000
print("null distribution = PSI/KS between the reference and clean batches drawn from the SAME history, %d bootstrap batches" % B)
print(f"{'n':>6} {'mean PSI':>9} {'p95 PSI':>8} {'p99 PSI':>8} {'P(PSI>0.1) on clean':>20} {'p99 KS D':>9}")
for n in (200, 2000, 20000):
    ps, ds = [], []
    for _ in range(B):
        b = rng.choice(ref, n, replace=True)
        ps.append(psi(b)); ds.append(ks_2samp(ref, b).statistic)
    ps, ds = np.array(ps), np.array(ds)
    print(f"{n:6d} {ps.mean():9.4f} {np.quantile(ps,.95):8.4f} {np.quantile(ps,.99):8.4f} {np.mean(ps>0.1):20.3f} {np.quantile(ds,.99):9.4f}")

# backtest: a threshold at the 99th pct, n=2000, against a real 0.15-sigma shift and 200 clean days
n = 2000
ps = [psi(rng.choice(ref, n)) for _ in range(B)]
thr = float(np.quantile(ps, .99))
clean_fa = np.mean([psi(rng.normal(0, 1, n)) > thr for _ in range(200)])
hit = np.mean([psi(rng.normal(0.15, 1, n)) > thr for _ in range(200)])
print(f"\nn=2000 chosen PSI threshold (p99 of null) = {thr:.4f}; false alarms on 200 fresh clean batches = {clean_fa:.3f}; detection of a 0.15-sigma shift = {hit:.3f}")
# many features: per-feature alpha 0.01 across 50 independent features
print("50 features, per-feature false-alarm rate 0.01: P(at least one alarm per day) = %.3f" % (1 - 0.99**50))
print("per-feature rate for a 0.01 daily family-wise rate over 50 features = %.5f" % (1 - 0.99**(1/50)))
```

**Output (my run):** Python 3.13, numpy 2.5.4, scipy 1.18.1, pandas 3.1.0, scikit-learn 1.9.1, pytest 9.1.1, PyYAML 6.0.3 (sandbox; numbers are from these seeded runs). (The batches are drawn from the same 50000-row history that is the reference, so the null is slightly narrower than with fully independent data.)
```text
null distribution = PSI/KS between the reference and clean batches drawn from the SAME history, 1000 bootstrap batches
     n  mean PSI  p95 PSI  p99 PSI  P(PSI>0.1) on clean  p99 KS D
   200    0.0470   0.0896   0.1217                0.031    0.1157
  2000    0.0046   0.0085   0.0111                0.000    0.0346
 20000    0.0005   0.0008   0.0010                0.000    0.0113

n=2000 chosen PSI threshold (p99 of null) = 0.0114; false alarms on 200 fresh clean batches = 0.015; detection of a 0.15-sigma shift = 0.990
50 features, per-feature false-alarm rate 0.01: P(at least one alarm per day) = 0.395
per-feature rate for a 0.01 daily family-wise rate over 50 features = 0.00020
```

**Follow-ups:**
- *Why PSI and KS both?* PSI shrinks with n (noise), KS D shrinks too; a p-value alone grows sensitive at large n, so I also set a minimum effect size (Evidently's blog says the same for KS at large n; check current docs).
- *What target rate?* Whatever the on-call can bear: alert fatigue is the real cost, so tie it to one false page per feature-month, not 5 percent.

**Common mistakes:** one threshold for every batch size; quoting 0.1 and 0.25 as industry standards; calibrating on a reference that includes the incident; checking false alarms but never power.

### Q39 ⭐ 🔴 Monitoring at scale and cost. Explain why you do not log or test every row: sampling, sketches and mergeable profiles (whylogs-style), pre-aggregated histograms, windowed jobs, and the cost of many models times many features. Use whylogs to profile three daily batches, merge the profiles, compare against the reference with its drift scores, and compare the profile size with the raw data size. Record the whylogs version and what ran; SaaS storage (WhyLabs) was not executed.
**Asked at:** Prometheus and Grafana monitoring mentions (K21Academy and Towards AI question lists naming Prometheus, Grafana and Evidently for drift and accuracy dashboards; Devinterview-io page opened, Q12 mentions inference monitoring with Grafana and Prometheus; search snippets otherwise); question lists, not verified reports; MLOps and platform roles; Prometheus, Grafana and Alertmanager servers were not available in this sandbox | Expert extension: no source found for the exact question; the topic follows from the library behaviour tested in this sandbox and from general monitoring practice, and Wave B must verify against current docs; MLOps, ML platform and ML engineer roles, including IT-services firms, product companies and GCCs
**Say this first (1 line):** At scale I do not store or test every row; I keep small mergeable profiles (histograms and counts, whylogs-style) per day, merge them for longer windows, and compare profiles to the reference, which costs almost nothing compared with raw data.

**Then explain:**
- **Sampling:** a random sample is fine for aggregate drift; keep every flagged or rare event (fraud, errors) at 100 percent.
- **Sketches and profiles:** a profile stores counts, min/max, distribution sketches per column. Profiles are mergeable: day1 + day2 + day3 = a 3-day profile without the rows.
- **Pre-aggregated histograms:** if you already have bucket counts in your warehouse, compute PSI from those; no raw pull.
- **Windowed jobs:** schedule per model per window; cost scales as models x features x windows, so tier models (critical ones get more features and hourly windows).
- **Failure modes:** sketches are approximate; a profile cannot be re-sliced by a column you did not profile; high-cardinality columns blow up size; string columns failed here (see below).

**Example:** three daily batches of 50000 rows (day 3 has `amount` shifted up), compared to a 50000-row reference. Day 1 shows no drift on any column; day 3 shows drift on `amount` only (statistic 0.237); the merged 3-day profile shows `amount` drift (0.079) diluted by two clean days. Merged profile file about 61.8 KB against 3.6 MB of in-memory dataframes (58 times smaller, and it does not grow with rows).

**Code:** (seeded; whylogs env with `[viz]`; `python3 -I`)
```py
import os, tempfile, warnings, logging
warnings.filterwarnings("ignore"); logging.disable(logging.CRITICAL)
import numpy as np, pandas as pd, whylogs as why
from whylogs.viz.drift.column_drift_algorithms import calculate_drift_scores

rng = np.random.default_rng(39)
def batch(n, mean, scale=1.0):
    return pd.DataFrame({"amount": rng.lognormal(mean, 0.5 * scale, n),
                         "age": rng.normal(40, 10, n),
                         "channel_code": rng.choice([0, 1, 2], n, p=[.5, .3, .2])})  # ints on purpose: string columns hit an np.unicode_ error on numpy 2 here
ref = batch(50000, 3.0)
days = [batch(50000, 3.0), batch(50000, 3.0), batch(50000, 3.3)]   # day 3 amount shifted
print("whylogs", why.__version__, "| pandas", pd.__version__)
ref_view = why.log(ref).view()
views = [why.log(d).view() for d in days]
merged = views[0]
for v in views[1:]: merged = merged.merge(v)
print("merged rows (count of amount):", merged.get_column("amount").get_metric("counts").n.value)
for name, tgt in [("day1", views[0]), ("day3", views[2]), ("merged 3 days", merged)]:
    s = calculate_drift_scores(target_view=tgt, reference_view=ref_view, with_thresholds=True)
    print(f"{name:14s}", {k: (round(v["statistic"], 3), v["algorithm"], v["drift_category"]) for k, v in s.items() if v})
raw = sum(d.memory_usage(deep=True).sum() for d in days)
d = tempfile.mkdtemp(); p = os.path.join(d, "merged.bin"); merged.write(p)
print("raw bytes in memory (3 days):", int(raw), "| merged profile file bytes:", os.path.getsize(p), "| ratio raw/profile: %.0f" % (raw / os.path.getsize(p)))
```

**Output (my run):** whylogs 1.6.4, pandas 3.1.0, numpy 2.5.4 in /tmp/claude-0/b8p08/e_whylogs. Drift scores come from `calculate_drift_scores` (needs `whylogs[viz]`); the number printed is the score for the KS algorithm, and the DRIFT or NO_DRIFT label uses whylogs' default threshold (check current docs). I did not rerun the string column case; a string column raised `AttributeError: np.unicode_ was removed in the NumPy 2.0 release` here, so I used numeric columns only. WhyLabs or any SaaS storage: not executed (no account or network service); the profile file above is the local equivalent.
```text
whylogs 1.6.4 | pandas 3.1.0
merged rows (count of amount): 150000
day1           {'amount': (0.003, 'ks', 'NO_DRIFT'), 'age': (0.006, 'ks', 'NO_DRIFT'), 'channel_code': (0.003, 'ks', 'NO_DRIFT')}
day3           {'amount': (0.236, 'ks', 'DRIFT'), 'age': (0.005, 'ks', 'NO_DRIFT'), 'channel_code': (0.004, 'ks', 'NO_DRIFT')}
merged 3 days  {'age': (0.005, 'ks', 'NO_DRIFT'), 'amount': (0.078, 'ks', 'DRIFT'), 'channel_code': (0.003, 'ks', 'NO_DRIFT')}
raw bytes in memory (3 days): 3600396 | merged profile file bytes: 61818 | ratio raw/profile: 58
```

**Follow-ups:**
- *Are merged profiles exact?* Counts, min, max, mean are exact. Quantile or distribution sketches carry a small error.
- *What do you lose?* Row-level debugging; keep a small sampled raw store next to the profiles.
- *Cost lever?* Fewer features, a longer window, a lower tier for low-risk models.

**Common mistakes:** logging every row to the warehouse "just in case"; profiling only the averages (distribution shape lost); forgetting that a merged window hides a one-day spike; assuming a library works on a new numpy without running it.

### Q40 ⭐ 🔴 Attribution drift and 'metric dropped but no drift detected'. Explain monitoring feature importance or contribution shift (permutation importance on a recent labelled window, mean absolute contribution for linear or tree models), the cases drift tests miss (concept change, a changed label definition, a join bug), and the debugging order when performance drops and every drift test is green. Simulate a concept change where only importance shifts, show the importance comparison catching it, and give the checklist.
**Asked at:** Label-delay and estimation sources (NannyML blog 'machine learning monitoring workflow' on delayed or absent targets, CBPE and DLE, and warning that drift alerts alone can flood a team; arXiv 'Monitoring Machine Learning Systems: A Multivocal Literature Review' 2509.14294; arXiv 2403.16795 interview study 'We have no idea how models will behave in production until production' reporting alert fatigue from false positives; search snippets only, not opened); vendor blog and academic papers, not interview reports; ML engineer and MLOps roles | Expert extension: no source found for the exact question; the topic follows from the library behaviour tested in this sandbox and from general monitoring practice, and Wave B must verify against current docs; MLOps, ML platform and ML engineer roles, including IT-services firms, product companies and GCCs
**Say this first (1 line):** When the metric drops and every drift test is green, I suspect the relationship between inputs and the label changed (concept change), a label or join bug, so I compare feature importance on a recent labelled window against the reference; the model's key feature stops mattering.

**Then explain:**
- **Drift tests only see inputs (and scores).** If the inputs look the same but the label's meaning moved, they stay quiet. That is the classic case.
- **Permutation importance:** on a labelled recent window, shuffle one feature and measure the metric drop. A big feature that used to matter and now matters 0 is a strong sign. Needs labels, so it lags.
- **Mean absolute contribution** (linear coefficients times values, or tree SHAP values; check your library's docs): label-free, can run daily; a shift in contribution means the inputs push the score differently.
- **Cases drift tests miss:** concept change; a changed label definition (a new chargeback rule); a join bug (labels attached to the wrong rows, so everything looks fine on inputs); feedback loops.
- **Debugging order when metric is down and drift is green:** (1) is the metric itself right (label definition, cohort, time window)? (2) label and join integrity on a sample; (3) data quality and schema; (4) score distribution and thresholds; (5) importance and slice analysis; (6) then conclude concept change and retrain on new labels.
- **Failure mode:** importance on a tiny window is noisy; correlated features share importance; importance shift is a clue, not proof.

**Example:** f0 drives the label before, f1 after (marginals never change). AUC drops 0.933 to 0.511; KS p-values 0.52, 0.58, 0.75 (quiet); mean score 0.498 vs 0.500 (quiet). Permutation importance of f0 falls 0.413 to -0.001 while f1 stays near 0 (the model never learned it).

**Code:** (seeded; `python3 -I`)
```py
import numpy as np
from scipy.stats import ks_2samp
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.inspection import permutation_importance
from sklearn.metrics import roc_auc_score

rng = np.random.default_rng(40)
n = 6000
def X(n): return rng.normal(0, 1, (n, 3))          # f0, f1, f2: marginals never change
def y_old(x): return (x[:, 0] + 0.2 * x[:, 2] + rng.normal(0, 0.5, len(x)) > 0).astype(int)  # f0 drives the label
def y_new(x): return (x[:, 1] + 0.2 * x[:, 2] + rng.normal(0, 0.5, len(x)) > 0).astype(int)  # concept change: f1 drives it now
Xtr, Xref, Xcur = X(n), X(n), X(n)
ytr, yref, ycur = y_old(Xtr), y_old(Xref), y_new(Xcur)
m = GradientBoostingClassifier(random_state=0).fit(Xtr, ytr)
print("AUC reference window: %.3f   AUC current window: %.3f" % (roc_auc_score(yref, m.predict_proba(Xref)[:, 1]), roc_auc_score(ycur, m.predict_proba(Xcur)[:, 1])))
print("per-feature KS p-values ref vs cur:", [round(float(ks_2samp(Xref[:, j], Xcur[:, j]).pvalue), 2) for j in range(3)], "(all quiet)")
def perm(Xw, yw):
    return permutation_importance(m, Xw, yw, scoring="roc_auc", n_repeats=5, random_state=0).importances_mean
pr, pc = perm(Xref, yref), perm(Xcur, ycur)
print("perm importance (AUC drop) ref:", np.round(pr, 3), " cur:", np.round(pc, 3))
print("importance change cur-ref     :", np.round(pc - pr, 3))
# Mean |contribution| of the model's own scores per feature is label-free; show prediction distribution stays put
print("mean predicted prob ref %.3f cur %.3f (score drift quiet too)" % (m.predict_proba(Xref)[:, 1].mean(), m.predict_proba(Xcur)[:, 1].mean()))
```

**Output (my run):** Python 3.13, numpy 2.5.4, scipy 1.18.1, pandas 3.1.0, scikit-learn 1.9.1, pytest 9.1.1, PyYAML 6.0.3 (sandbox; numbers are from these seeded runs).
```text
AUC reference window: 0.933   AUC current window: 0.511
per-feature KS p-values ref vs cur: [0.52, 0.58, 0.75] (all quiet)
perm importance (AUC drop) ref: [ 0.413 -0.     0.018]  cur: [-0.001  0.002  0.013]
importance change cur-ref     : [-0.414  0.002 -0.005]
mean predicted prob ref 0.498 cur 0.500 (score drift quiet too)
```

**Follow-ups:**
- *So what is the fix?* New labels under the new rule, retrain, validate (Q41 gates). A threshold tweak does not repair a concept change.
- *No labels yet?* Use contribution shift plus proxy labels, or an estimate like NannyML's CBPE (concept only here).

**Common mistakes:** "no drift so no problem"; blaming the model before checking the label definition; trusting a feature-importance diff on a few hundred rows.

### Q41 ⭐ 🔴 Model risk governance and monitoring for a regulated lender, for example an Indian bank or NBFC credit-scoring model. Cover model inventory, periodic validation, monitoring thresholds that trigger review, challenger models, audit trail of decisions, explainability on request, and change control for retraining. Give a whiteboard answer and a monitoring-policy YAML, validate it with pyyaml, and state that the specific regulator expectations (check current RBI and other guidance, which was not looked up here) are not quoted. Part 12 owns system design in depth.
**Asked at:** Expert extension: no source found for the exact question; the topic follows from the library behaviour tested in this sandbox and from general monitoring practice, and Wave B must verify against current docs; MLOps, ML platform and ML engineer roles, including IT-services firms, product companies and GCCs
**Say this first (1 line):** For a regulated lender I treat the model as a controlled asset: it is in an inventory, validated independently, monitored against thresholds that trigger a human review, changed only through change control, and every decision is traceable and explainable.

**Then explain:**
- **Model inventory:** every model has an owner, risk tier, intended use and version. If it is not in the inventory, it should not score.
- **Validation:** independent validation before go-live and periodic revalidation; monitoring feeds that, it does not replace it.
- **Thresholds that trigger review:** warn then breach levels (input PSI, score PSI, matured-cohort Gini or KS drop, approval-rate change, data quality). A breach opens a review, not an automatic retrain.
- **Challenger:** run a shadow challenger; promotion needs validation, approval and a rollback plan.
- **Audit trail:** log request id, model version, features (hashed or referenced), score, decision, reason codes, timestamp; retention set by compliance.
- **Explainability on request:** reason codes from contributions, reproducible for an old decision with the logged version.
- **Change control:** retrain request with ticket, validation report, approver who is not the author; rollback to the previous registered version.
- **Failure modes:** labels (defaults) mature slowly; a policy YAML nobody enforces; thresholds copied, not calibrated (Q38).
- **Regulator:** I did not look up RBI or other regulator guidance, so none is quoted. In the interview I would say "my policy follows whatever the bank's model-risk framework and current regulator guidance require; I would check with compliance".

**Example (whiteboard):** inventory -> validate -> deploy v3 -> monthly monitor -> warn: notify owner; breach: review meeting -> challenger in shadow -> committee approves -> versioned rollout with rollback. Next to it, a decision log row per application.

**Code:** (placeholders, not real policy numbers; validated with pyyaml)
```yaml
# Illustrative monitoring policy for a regulated credit-scoring model.
# Numbers are placeholders for the model-risk team to set; regulator expectations are NOT quoted here.
model:
  id: credit_score_v3
  owner: retail-risk-analytics
  risk_tier: high
  inventory_ref: MRM-0042
  intended_use: unsecured personal loan underwriting
validation:
  independent_validation_before_go_live: true
  periodic_revalidation_months: 12
monitoring:
  cadence: monthly
  checks:
    - {name: input_psi_max, level: warn, threshold: 0.10, action: notify_owner}
    - {name: input_psi_max, level: breach, threshold: 0.25, action: open_review}
    - {name: score_psi, level: breach, threshold: 0.20, action: open_review}
    - {name: gini_matured_cohort_drop, level: breach, threshold: 0.05, action: open_review}
    - {name: approval_rate_change_abs, level: warn, threshold: 0.05, action: notify_owner}
    - {name: missing_rate_any_feature, level: breach, threshold: 0.02, action: block_scoring_and_page}
  thresholds_status: calibrated_on_history   # see Q38; backtest on past incidents
challenger:
  enabled: true
  mode: shadow
  promote_requires: [independent_validation, committee_approval, rollback_plan]
audit:
  log_fields: [request_id, model_version, feature_hash, score, decision, reason_codes, timestamp]
  retain_years: TBD_by_compliance
  pii_policy: hash_or_omit
explainability:
  on_request: true
  method: reason_codes_from_contributions
change_control:
  retrain_requires: [ticket, validation_report, approver_not_author]
  rollback_to: previous_registered_version
```
```py
import yaml, sys
p = yaml.safe_load(open(sys.argv[1]))
need = ["model", "validation", "monitoring", "challenger", "audit", "explainability", "change_control"]
missing = [k for k in need if k not in p]
assert not missing, missing
levels = {"warn", "breach"}
for c in p["monitoring"]["checks"]:
    assert c["level"] in levels and isinstance(c["threshold"], float) and c["action"], c
# every check name with a breach level must have an action that is not just a notification
breach_actions = {c["action"] for c in p["monitoring"]["checks"] if c["level"] == "breach"}
assert breach_actions <= {"open_review", "block_scoring_and_page"}, breach_actions
# a warn threshold must be below its breach threshold when both exist
by = {}
for c in p["monitoring"]["checks"]: by.setdefault(c["name"], {})[c["level"]] = c["threshold"]
for n, d in by.items():
    if len(d) == 2: assert d["warn"] < d["breach"], n
assert p["challenger"]["mode"] == "shadow" and "retain_years" in p["audit"]
print("policy OK: sections", sorted(p), "| checks", len(p["monitoring"]["checks"]), "| names with both levels:", [n for n, d in by.items() if len(d) == 2])
```

**Output (my run):** PyYAML 6.0.3. Structural validation only (sections present, thresholds numeric, warn < breach where both exist, breach actions are reviews or blocks). Actual regulator rules, audit-retention length and any bank tooling: not executed / not looked up.
```text
policy OK: sections ['audit', 'challenger', 'change_control', 'explainability', 'model', 'monitoring', 'validation'] | checks 6 | names with both levels: ['input_psi_max']
```

**Follow-ups:**
- *Who approves a retrain?* Someone other than the author, per the policy (validation plus committee).
- *Why shadow challenger?* It scores live traffic without affecting decisions, so you compare before promotion.
- *Fairness?* Add segment-level checks to the policy (concept in the YAML for Q43; regulator expectations not looked up).

**Common mistakes:** automatic retraining with no validation; no model inventory; logging features without a version; quoting regulator rules from memory.

### Q42 ⭐ 🟡 LLM and GenAI monitoring, only at the boundary with Book 2. State what carries over from classic ML monitoring (input data quality, schema, latency, cost, error rates, feedback logging, drift on input categories, privacy of logs, incident process) and what does not (hallucination, groundedness, prompt-injection and retrieval quality, which Book 2 and a later LLMOps part own). Implement a small logger for request, response length, latency and thumbs feedback with a rolling summary, run it on a stub model (no real API call, so say the real provider is not executed).
**Asked at:** MLOps interview question banks and guides (K21Academy '47 MLOps interview questions' PDF, Towards AI '101 ML LLM agentic AIOps interview questions', DataCamp MLOps interview questions, The Interview Guys MLOps post, wecreateproblems.com, hyring.com, dev.to vivekk101, a Medium skphd post; search snippets only, not opened; the Devinterview-io/mlops-interview-questions GitHub page WAS opened and has no dedicated monitoring or drift question, only monitoring bullets inside Q1, Q2, Q4, Q6, Q7 and Q12); editorial question lists, not verified candidate reports; MLOps, ML platform and ML engineer roles at IT-services firms, product companies and GCCs | Expert extension: no source found for the exact question; the topic follows from the library behaviour tested in this sandbox and from general monitoring practice, and Wave B must verify against current docs; MLOps, ML platform and ML engineer roles, including IT-services firms, product companies and GCCs
**Say this first (1 line):** Most classic monitoring carries over (input quality, schema, latency, cost, errors, feedback, privacy, incidents); what does not is quality judgement like hallucination, groundedness, prompt-injection and retrieval quality, which Book 2 and a later LLMOps part own.

**Then explain:**
- **Carries over:** request validity and schema, latency percentiles, error and timeout rate, token or cost per call, response length, drift on input categories, thumbs or other feedback with a delay, privacy of logs, an incident process.
- **Does not carry over cleanly:** there is no single label; "correct" is fuzzy. Hallucination, groundedness, injection and retrieval quality need their own evaluators (Book 2).
- **Log metadata first:** store length, latency, a hash of the prompt and feedback; store raw text only if policy allows, masked.
- **Rolling summary:** a fixed window of recent calls gives p50, p95, error rate, mean length and thumbs-up rate; compare to a baseline.
- **Failure modes:** feedback is sparse and biased (only unhappy users click); a rolling window over a quiet hour is noisy; changing the provider's model silently moves everything.

**Example:** 80 calls to a stub, window of 50. At call 50: error 0.06, p50 266 ms, p95 390 ms. At call 80 (a simulated slowdown): p50 362, p95 853, error 0.08, thumbs-up 0.812 on 16 votes (too few to read much into).

**Code:** (stub model, seeded; `python3 -I`). The real provider call is not executed; latencies are simulated numbers.
```py
import time, json, random, zlib, statistics as st
from collections import deque

class CallLogger:
    """Log metadata first: no raw text stored, only length, latency, a hash of the request, feedback."""
    def __init__(self, window=50):
        self.rows = deque(maxlen=window)
    def log(self, request_id, prompt, response, latency_ms, error=None):
        self.rows.append({"id": request_id, "prompt_len": len(prompt), "resp_len": len(response or ""),
                          "latency_ms": latency_ms, "error": error, "thumb": None, "prompt_hash": zlib.crc32(prompt.encode())})
    def feedback(self, request_id, thumb):
        for r in self.rows:
            if r["id"] == request_id: r["thumb"] = thumb
    def summary(self):
        rows = list(self.rows); lat = sorted(r["latency_ms"] for r in rows)
        fb = [r["thumb"] for r in rows if r["thumb"] is not None]
        return {"n": len(rows), "error_rate": round(sum(r["error"] is not None for r in rows) / len(rows), 3),
                "p50_ms": lat[len(lat) // 2], "p95_ms": lat[int(0.95 * (len(lat) - 1))],
                "mean_resp_len": round(st.mean(r["resp_len"] for r in rows), 1),
                "feedback_n": len(fb), "thumbs_up_rate": round(sum(fb) / len(fb), 3) if fb else None}

def stub_model(prompt, rng):                       # stands in for a real provider call (NOT executed here)
    if rng.random() < 0.10: raise TimeoutError("stub timeout")
    return "ok " * rng.randint(3, 30)

rng = random.Random(42); lg = CallLogger(window=50)
for i in range(80):
    p = "question %d " % i + "x" * rng.randint(0, 100)
    t0 = time.perf_counter()
    try: out, err = stub_model(p, rng), None
    except TimeoutError as e: out, err = None, str(e)
    lat = rng.randint(80, 400) if i < 60 else rng.randint(300, 900)   # simulated latency; late slowdown
    lg.log(i, p, out, lat, err)
    if i % 3 == 0 and err is None: lg.feedback(i, rng.random() < 0.7)
    if i in (49, 79): print(f"after {i+1} calls:", json.dumps(lg.summary()))
```

**Output (my run):** Python 3.13, numpy 2.5.4, scipy 1.18.1, pandas 3.1.0, scikit-learn 1.9.1, pytest 9.1.1, PyYAML 6.0.3 (sandbox; numbers are from these seeded runs).
```text
after 50 calls: {"n": 50, "error_rate": 0.06, "p50_ms": 266, "p95_ms": 390, "mean_resp_len": 46.1, "feedback_n": 16, "thumbs_up_rate": 0.562}
after 80 calls: {"n": 50, "error_rate": 0.08, "p50_ms": 362, "p95_ms": 853, "mean_resp_len": 46.0, "feedback_n": 16, "thumbs_up_rate": 0.812}
```

**Follow-ups:**
- *Is the thumbs-up rate a quality metric?* A weak one; use it as a trend, and sample for human review.
- *What do you log about the prompt?* Length, hash, category; raw text only under a masking and retention policy.

**Common mistakes:** logging full prompts with personal data; treating latency as quality; reusing a classification-accuracy dashboard for generation; claiming a stub run proves anything about a real provider.

### Q43 ⭐ 🔴 Design question: the monitoring system for a card-fraud model with chargeback labels that arrive 30 to 90 days late, millions of events per day, and a regulated Indian bank or a global payments company. Cover logging, data-quality gates, feature and score drift, delayed-label performance with matured cohorts, analyst feedback labels, alert tiers, retraining policy, shadow challenger, fairness checks, privacy and on-call. Give a one-page whiteboard answer, a monitoring-spec YAML validated with pyyaml, and state which parts are concept only. Part 12 owns system design in depth.
**Asked at:** MLOps interview question banks and guides (K21Academy '47 MLOps interview questions' PDF, Towards AI '101 ML LLM agentic AIOps interview questions', DataCamp MLOps interview questions, The Interview Guys MLOps post, wecreateproblems.com, hyring.com, dev.to vivekk101, a Medium skphd post; search snippets only, not opened; the Devinterview-io/mlops-interview-questions GitHub page WAS opened and has no dedicated monitoring or drift question, only monitoring bullets inside Q1, Q2, Q4, Q6, Q7 and Q12); editorial question lists, not verified candidate reports; MLOps, ML platform and ML engineer roles at IT-services firms, product companies and GCCs | Scenario question write-ups (a Glassdoor EPAM Systems interview page whose snippet lists 'why does production differ from training' with feature, preprocessing and version mismatch as causes, and an end-to-end design prompt; one candidate's review, search snippet only, not opened, unverified; The Interview Guys post saying drift is asked in almost every MLOps interview, snippet only); anecdotal, not company-verified reports; MLOps and ML engineer roles | Expert extension: no source found for the exact question; the topic follows from the library behaviour tested in this sandbox and from general monitoring practice, and Wave B must verify against current docs; MLOps, ML platform and ML engineer roles, including IT-services firms, product companies and GCCs
**Say this first (1 line):** Log every scored event with a feature snapshot, gate the data first, watch feature and score drift in real time as early warnings, measure true performance only on matured cohorts once chargebacks arrive, and use tiered alerts so only data-quality or score-collapse issues page someone.

**Then explain (whiteboard in order):**
- **Logging:** event id, timestamp, model version, feature snapshot reference, score, decision; tokenised card data; sampled raw rows plus all flagged.
- **Data-quality gates:** null rate, schema, freshness, volume vs same weekday. A failed gate pages the data owner and blocks drift alerts (no point testing garbage).
- **Drift:** daily feature drift with calibrated thresholds (Q38), hourly score drift plus a score-band pile-up check (Q44). These are early warnings, not proof of damage.
- **Delayed labels:** chargebacks arrive 30 to 90 days late. Compute recall and precision on matured cohorts (events old enough that most labels exist), and mark the share of labels received. Early proxies: analyst feedback labels, alert rate, score-based estimates.
- **Alert tiers:** page (gate failed, score collapse), ticket (persistent drift, matured-cohort drop), info (one-day feature drift).
- **Retraining:** hybrid (monthly schedule plus a trigger confirmed by labels); offline backtest, shadow challenger, approval; rollback to the previous version.
- **Fairness and privacy:** false-positive-rate gaps across segments monthly; minimise stored PII; access-controlled logs.
- **On-call:** a runbook per page; the model owner is on a rota; false-alert reviews monthly.
- **Concept only (not run):** fairness checks, shadow challenger, analyst labels, on-call routing. Run here: the YAML validation and the matured-cohort simulation.

**Example:** in the simulation real recall drops from 0.80 to 0.60 at day 120. By day 199, the day-110 cohort is 98 percent labelled and shows 0.80; day 130 is 68 percent labelled and shows 0.57; day 150 is only 32 percent labelled. The drop is visible only as old cohorts mature, which is why the proxies and drift stay as early warnings.

**Code:** (YAML spec with placeholders; validation and cohort simulation, seeded)
```yaml
# Illustrative monitoring spec for a card-fraud model (concept; thresholds are placeholders to calibrate, see Q38)
model: {id: card_fraud_v7, serving: real_time, volume: millions_per_day}
logging:
  fields: [event_id, ts, model_version, feature_snapshot_ref, score, decision]
  pii: {card_number: tokenised, raw_text: not_logged}
  sampling: {features: full_for_aggregates, raw_rows: one_percent_plus_all_flagged}
data_quality_gates:       # run before drift; a failed gate pages the data owner, not the model owner
  - {check: null_rate, max: 0.02}
  - {check: schema_match, required: true}
  - {check: freshness_minutes, max: 15}
  - {check: volume_vs_same_weekday, min_ratio: 0.7, max_ratio: 1.4}
drift:
  features: {test: psi_calibrated, window: daily, per_feature_alpha: bonferroni}
  score: {test: ks_and_band_pileup, window: hourly}
performance:
  label_source: chargeback
  label_delay_days: {min: 30, max: 90}
  matured_cohort_days: 90
  early_proxy: [analyst_feedback_labels, alert_rate, estimated_precision_from_scores]
  metric: [recall_at_fixed_review_capacity, precision_at_threshold]
fairness:
  segments: [region, card_type, customer_age_band]
  check: false_positive_rate_gap
  cadence: monthly
alert_tiers:
  - {tier: page, when: [data_quality_gate_failed, score_distribution_collapse], route: oncall}
  - {tier: ticket, when: [feature_drift_persistent_3_days, matured_cohort_metric_drop], route: ml_team}
  - {tier: info, when: [single_day_feature_drift], route: dashboard}
retraining:
  policy: hybrid
  schedule: monthly
  triggers: [matured_cohort_metric_drop, persistent_drift_with_label_confirmation]
  gate: [offline_backtest, shadow_challenger_14_days, approver_sign_off]
  rollback: previous_registered_version
shadow_challenger: {enabled: true, compare: [score_correlation, flagged_overlap, matured_metrics]}
concept_only: [fairness, shadow_challenger, analyst_feedback_labels, oncall_routing]
```
```py
# --- q43_validate.py ---
import yaml, sys
s = yaml.safe_load(open(sys.argv[1]))
for k in ["logging", "data_quality_gates", "drift", "performance", "fairness", "alert_tiers", "retraining", "shadow_challenger"]:
    assert k in s, k
assert s["performance"]["matured_cohort_days"] >= s["performance"]["label_delay_days"]["max"]
assert {t["tier"] for t in s["alert_tiers"]} == {"page", "ticket", "info"}
assert s["retraining"]["rollback"] and "shadow_challenger_14_days" in s["retraining"]["gate"]
print("spec OK:", len(s["data_quality_gates"]), "gates,", len(s["alert_tiers"]), "alert tiers, matured cohort", s["performance"]["matured_cohort_days"], "days")

# --- q43_cohort.py ---
import numpy as np
# Matured-cohort recall: labels arrive 30-90 days after the event, so today's cohort is unlabelled.
rng = np.random.default_rng(43)
days, per = 200, 20000
rec = []
for d in range(days):
    fraud = rng.random(per) < 0.01
    caught = fraud & (rng.random(per) < (0.80 if d < 120 else 0.60))   # real recall drops from day 120
    delay = rng.integers(30, 91, per)
    rec += [(d, f, c, dl) for f, c, dl in zip(fraud, caught, delay)]
d_, f_, c_, dl_ = map(np.array, zip(*rec))
today = 199
def recall_cohort(day):  # what we know today about the cohort of that day
    m = (d_ == day) & f_ & (day + dl_ <= today)
    return (c_[m].sum() / max(m.sum(), 1)), int(m.sum())
for day in (60, 110, 130, 150):
    r, n = recall_cohort(day)
    known = ((d_ == day) & f_ & (day + dl_ <= today)).sum() / max(((d_ == day) & f_).sum(), 1)
    print(f"cohort day {day}: share of its fraud labelled by day {today}: {known:.2f}  recall on labelled part: {("%.2f" % r) if n else "n/a"} (n={n})")
```

**Output (my run):** PyYAML 6.0.3 for validation, numpy 2.5.4 for the simulation. Kafka, a feature store, the bank's alerting stack and on-call tooling: not executed. The simulation assumes label delay is independent of whether the fraud was caught.
`validation`
```text
spec OK: 4 gates, 3 alert tiers, matured cohort 90 days
```
`matured cohorts`
```text
cohort day 60: share of its fraud labelled by day 199: 1.00  recall on labelled part: 0.78 (n=226)
cohort day 110: share of its fraud labelled by day 199: 0.98  recall on labelled part: 0.80 (n=200)
cohort day 130: share of its fraud labelled by day 199: 0.68  recall on labelled part: 0.57 (n=126)
cohort day 150: share of its fraud labelled by day 199: 0.32  recall on labelled part: 0.65 (n=66)
```

**Follow-ups:**
- *Why not wait for chargebacks?* You would learn about a bad model 3 months late; hence drift and proxies as early warning.
- *Bias in analyst labels?* Analysts only review flagged cases, so labels are biased toward what the model already flags; keep a random review sample.
- *Millions of events?* Profiles and sketches (Q39), tiered features.

**Common mistakes:** computing recall on the latest week (labels missing); paging on any drift; one retraining trigger with no validation gate; forgetting that blocked transactions get no chargeback label.

### Q44 ⭐ 🔴 Adversarial and non-stationary inputs: gaming and fraud adaptation, a model whose decisions change user behaviour (performative drift), and bot or test traffic polluting the monitor. Explain how monitoring must separate organic drift from adaptation, filter synthetic or internal traffic, and why a rising score for a blocked segment may be the model working. Simulate an adaptive attacker moving features just below a threshold, show feature drift and the score-band pile-up, and write the detector for the pile-up.
**Asked at:** Expert extension: no source found for the exact question; the topic follows from the library behaviour tested in this sandbox and from general monitoring practice, and Wave B must verify against current docs; MLOps, ML platform and ML engineer roles, including IT-services firms, product companies and GCCs
**Say this first (1 line):** Adversaries and the model itself change the data, so I separate organic drift from adaptation: watch the score bands just below the decision threshold for a pile-up, filter internal and test traffic before drift tests, and read a rising score in a blocked segment as possibly the model working.

**Then explain:**
- **Adaptive attackers:** they probe, then tune inputs to land just under a threshold. Marginal feature drift is mild; the signature is a pile-up in the band below the line.
- **Performative drift:** decisions change behaviour (a declined user retries with different details), so the data you see after launch depends on the model. The old reference stops being "normal".
- **Bot, test and internal traffic:** synthetic or QA traffic can make drift tests fire or mask real shifts; tag it (header, IP list, test account) and filter it before computing drift.
- **Blocked segment:** if the blocked group's average score rises, that may be the model correctly catching more; do not "fix" it.
- **Detector:** compare mass just below the threshold with the reference band and with the band just above it; alert when the ratio is high and the count is large enough.
- **Failure modes:** label feedback is biased (you only see outcomes for approved cases); a retrain on attacker-shaped data teaches the model the attacker's pattern; threshold is public knowledge in some systems.

**Example:** threshold 0.80; 15 percent of week-8 traffic is an attacker with feature value 1.25 to 1.50 (score about 0.65 to 0.76). Feature KS D 0.134. The block rate falls from 6.05 to 5.24 percent. The band 0.70 to 0.80 holds 3.26 percent of traffic at week 0 and 12.2 percent at week 8 (ratio 3.74, 4.79 times the band above); the control run shows ratio 0.93 and no alert.

**Code:** (seeded, numpy and scipy; `python3 -I`)
```py
import numpy as np
from scipy.stats import ks_2samp
rng = np.random.default_rng(44)
n = 20000
THRESH = 0.80                                    # model blocks at score >= 0.80
def score(x): return 1 / (1 + np.exp(-(x - 1.0) * 2.5))   # monotone score from a risk feature
organic = rng.normal(0, 1, n)                     # week 0 traffic
score0 = score(organic)
# week 8: 15% of traffic is an adaptive attacker who tunes the feature to land just under the block line
atk = int(0.15 * n)
x_cur = rng.normal(0, 1, n)
x_cur[:atk] = rng.uniform(1.25, 1.50, atk)       # score about 0.65 to 0.76 (just below 0.80) , i.e. x < ~1.55
score1 = score(x_cur)
print("block threshold on score: %.2f (feature x=%.2f)" % (THRESH, 1 + np.log(THRESH/(1-THRESH))/2.5))
print("feature KS D=%.3f  score KS D=%.3f  block rate %.4f -> %.4f" % (
    ks_2samp(organic, x_cur).statistic, ks_2samp(score0, score1).statistic, (score0 >= THRESH).mean(), (score1 >= THRESH).mean()))

def pileup_detector(ref_scores, cur_scores, thr, width=0.10, min_ratio=2.0, min_count=30):
    """Compare the mass in the band just BELOW the threshold with the mass in the same band at reference, and with the band just ABOVE."""
    lo, hi = thr - width, thr
    ref_b = np.mean((ref_scores >= lo) & (ref_scores < hi)); cur_b = np.mean((cur_scores >= lo) & (cur_scores < hi))
    above = np.mean((cur_scores >= thr) & (cur_scores < thr + width))
    cnt = int(np.sum((cur_scores >= lo) & (cur_scores < hi)))
    return {"below_band_ref": round(float(ref_b), 4), "below_band_cur": round(float(cur_b), 4),
            "band_ratio": round(float(cur_b / ref_b), 2), "below_over_above": round(float(cur_b / max(above, 1e-9)), 2),
            "alert": bool(cnt >= min_count and cur_b / ref_b >= min_ratio)}
print("week 8 vs week 0:", pileup_detector(score0, score1, THRESH))
print("control (no attacker):", pileup_detector(score0, score(rng.normal(0, 1, n)), THRESH))
```

**Output (my run):** Python 3.13, numpy 2.5.4, scipy 1.18.1, pandas 3.1.0, scikit-learn 1.9.1, pytest 9.1.1, PyYAML 6.0.3 (sandbox; numbers are from these seeded runs). The traffic filter was not simulated; it is a rule applied before the test.
```text
block threshold on score: 0.80 (feature x=1.55)
feature KS D=0.134  score KS D=0.134  block rate 0.0605 -> 0.0524
week 8 vs week 0: {'below_band_ref': 0.0326, 'below_band_cur': 0.122, 'band_ratio': 3.74, 'below_over_above': 4.79, 'alert': True}
control (no attacker): {'below_band_ref': 0.0326, 'below_band_cur': 0.0304, 'band_ratio': 0.93, 'below_over_above': 1.03, 'alert': False}
```

**Follow-ups:**
- *Do you tell the model team or the fraud ops?* Both: the model team for threshold or feature changes, ops for the attacker segment.
- *Randomise the threshold?* A defensive idea (check your risk team); it makes probing harder.

**Common mistakes:** retraining on traffic that includes the attacker's tuned samples without review; including QA traffic in the baseline; treating every score rise as a model failure.

### Q45 ⭐ 🔴 Testing the monitors themselves. How do you know your drift and data-quality checks work before an incident: inject known faults (null spike, unit change, shifted mean, dropped partition) into a clean batch, assert the right monitor fires and the others stay quiet, measure detection rate and false-alarm rate over many seeds, and replay logged history through new monitor versions (backfill) before enabling alerts. Write pytest cases for a small monitor suite with a fault-injection helper, run them, and report the detection matrix. Part 1 owns pytest basics.
**Asked at:** Expert extension: no source found for the exact question; the topic follows from the library behaviour tested in this sandbox and from general monitoring practice, and Wave B must verify against current docs; MLOps, ML platform and ML engineer roles, including IT-services firms, product companies and GCCs
**Say this first (1 line):** I test monitors like code: inject known faults into a clean batch, assert that the right monitor fires and the others stay quiet, measure detection and false-alarm rate over many seeds, and replay logged history through a new monitor version before enabling its alerts.

**Then explain:**
- **Fault injection helper:** one function per fault (null spike, unit change, mean shift, dropped partition) applied to a clean batch.
- **Detection matrix:** rows are faults, columns are monitors, cells are the fraction of seeds where it fired. You want a clean diagonal-like pattern and an all-zero "no fault" row.
- **Many seeds:** one lucky seed proves nothing; 30 to 200 seeds give a rate. Assert rates (at least 95 percent detect, at most 5 percent false alarm).
- **Backfill replay:** run the new monitor over past logged days, count alerts, compare with known incidents, then enable paging (concept here; the logic is the same function in a loop).
- **What the first run taught me:** the volume monitor (min ratio 0.7) missed a dropped region because 1 of 4 regions is only 25 percent of rows (75 percent remain). My first test failed (0 of 30 detections). I added a category-presence monitor and left a test that documents the volume monitor's limit.
- **Failure modes:** tests with fixed seeds that hide flakiness; thresholds tuned until the tests pass; asserting only "something fired".

**Example:** the matrix below. `none` row all 0.00 (no false alarms in 200 seeds). Unit change fires `drift` and `range`; mean shift only `drift`; null spike only `null`; dropped partition only `category`.

**Code:** (three files in `code/q45/`: monitors, tests, matrix script; pytest basics are Part 1)
```py
# --- q45/monitors.py ---
import numpy as np, pandas as pd
from scipy.stats import ks_2samp

# each monitor returns True when it fires
def null_monitor(ref, cur, col="amount", max_rate=0.02):
    return cur[col].isna().mean() > max_rate
def drift_monitor(ref, cur, col="amount", alpha=0.001, min_d=0.1):
    d = ks_2samp(ref[col].dropna(), cur[col].dropna())
    return d.pvalue < alpha and d.statistic > min_d          # significant AND big enough
def range_monitor(ref, cur, col="amount", factor=3.0):
    return cur[col].max() > factor * ref[col].max()          # catches unit changes
def volume_monitor(ref, cur, min_ratio=0.7):
    return len(cur) < min_ratio * len(ref)                   # catches dropped partitions
def category_monitor(ref, cur, col="region"):
    return bool(set(ref[col].unique()) - set(cur[col].unique()))   # a known value vanished
MONITORS = {"null": null_monitor, "drift": drift_monitor, "range": range_monitor, "volume": volume_monitor, "category": category_monitor}

# fault injection
def clean_batch(rng, n=5000):
    return pd.DataFrame({"amount": rng.lognormal(3.0, 0.5, n), "region": rng.choice(list("NSEW"), n)})
def inject(df, fault, rng):
    df = df.copy()
    if fault == "null_spike": df.loc[rng.random(len(df)) < 0.10, "amount"] = np.nan
    elif fault == "unit_change": df["amount"] = df["amount"] * 100       # rupees to paise
    elif fault == "mean_shift": df["amount"] = df["amount"] * 1.25
    elif fault == "dropped_partition": df = df[df["region"] != "W"].reset_index(drop=True)
    elif fault != "none": raise ValueError(fault)
    return df

# --- q45/test_monitors.py ---
import numpy as np, pytest
from monitors import MONITORS, clean_batch, inject

# expected: which monitors MUST fire for each fault (the rest are not asserted here; the matrix script reports them)
MUST = {"null_spike": {"null"}, "unit_change": {"drift", "range"}, "mean_shift": {"drift"}, "dropped_partition": {"category"}}
SEEDS = range(30)

@pytest.mark.parametrize("fault", list(MUST))
def test_fault_detected(fault):
    hits = {m: 0 for m in MONITORS}
    for s in SEEDS:
        rng = np.random.default_rng(1000 + s)
        ref, cur = clean_batch(rng), inject(clean_batch(rng), fault, rng)
        for m, f in MONITORS.items(): hits[m] += bool(f(ref, cur))
    for m in MUST[fault]:
        assert hits[m] / len(SEEDS) >= 0.95, (fault, m, hits)

def test_clean_batches_are_quiet():
    fa = {m: 0 for m in MONITORS}
    for s in SEEDS:
        rng = np.random.default_rng(2000 + s)
        ref, cur = clean_batch(rng), clean_batch(rng)
        for m, f in MONITORS.items(): fa[m] += bool(f(ref, cur))
    assert all(v / len(SEEDS) <= 0.05 for v in fa.values()), fa

def test_null_spike_does_not_trigger_volume():
    rng = np.random.default_rng(7)
    ref, cur = clean_batch(rng), inject(clean_batch(rng), "null_spike", rng)
    assert not MONITORS["volume"](ref, cur)

def test_volume_monitor_misses_a_one_in_four_drop():
    """Documented limit found by the first run: dropping 1 of 4 regions leaves 75 percent of rows, above the 0.7 floor."""
    rng = np.random.default_rng(9)
    ref, cur = clean_batch(rng), inject(clean_batch(rng), "dropped_partition", rng)
    assert not MONITORS["volume"](ref, cur)
    assert MONITORS["category"](ref, cur)

# --- q45/matrix.py ---
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from monitors import MONITORS, clean_batch, inject
faults = ["none", "null_spike", "unit_change", "mean_shift", "dropped_partition"]
print(f"{'fault':18s}" + "".join(f"{m:>9s}" for m in MONITORS) + "   (fraction of 200 seeds where the monitor fired)")
for fault in faults:
    row = {m: 0 for m in MONITORS}
    for s in range(200):
        rng = np.random.default_rng(s)
        ref, cur = clean_batch(rng), inject(clean_batch(rng), fault, rng)
        for m, f in MONITORS.items(): row[m] += bool(f(ref, cur))
    print(f"{fault:18s}" + "".join(f"{row[m]/200:9.2f}" for m in MONITORS))
```

**Output (my run):** Python 3.13, numpy 2.5.4, scipy 1.18.1, pandas 3.1.0, scikit-learn 1.9.1, pytest 9.1.1, PyYAML 6.0.3 (sandbox; numbers are from these seeded runs). First pytest run (before adding the category monitor):
```text
E            +  where 30 = len(range(0, 30))

/home/user/case_studies/interviews/scratch/B4P08_Q35-45/code/q45/test_monitors.py:16: AssertionError
=========================== short test summary info ============================
FAILED test_monitors.py::test_fault_detected[dropped_partition] - AssertionEr...
1 failed, 5 passed in 1.86s
```After the fix:
`pytest`
```text
.......                                                                  [100%]
7 passed in 1.91s
```
`matrix.py`
```text
fault                  null    drift    range   volume category   (fraction of 200 seeds where the monitor fired)
none                   0.00     0.00     0.00     0.00     0.00
null_spike             1.00     0.00     0.00     0.00     0.00
unit_change            0.00     1.00     1.00     0.00     0.00
mean_shift             0.00     1.00     0.00     0.00     0.00
dropped_partition      0.00     0.00     0.00     0.00     1.00
```

**Follow-ups:**
- *How do you avoid tuning to the tests?* Keep a held-out set of historic incidents and faults the thresholds never saw.
- *Which fault is the hardest?* Slow, small shifts; test with graded fault sizes and read power, not one size.

**Common mistakes:** testing only the happy path; asserting on one seed; no "no fault" row; enabling a new monitor's pager without a backfill replay.

