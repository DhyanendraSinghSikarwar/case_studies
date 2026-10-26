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
