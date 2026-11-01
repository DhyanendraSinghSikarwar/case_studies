### Q19 ⭐⭐ 🟡 Vertex AI Feature Store versus feature management in Azure ML: the current Vertex design (BigQuery as the offline source, feature groups and feature views, online serving through Bigtable or optimized online serving), the deprecation dates published for the legacy store and optimized online serving, and what a migration means. Part 9 owns feature-store concepts: cover only the managed-service choices, sync modes and the risk of building on a deprecated service. Check the docs-deprecations page the snippets point to and state that nothing was run.
**Asked at:** GCP Vertex AI interview question list (javainuse 'gcp vertex ai' 2026 list: Vertex Pipelines, Feature Store, Model Registry, model monitoring, MLOps, model versioning; search snippet only, not opened); editorial prep site, not verified candidate reports; ML engineer and MLOps roles at GCP-using product companies and cloud-consulting firms | Google Cloud Vertex AI documentation pages as returned by search (MLOps on Vertex AI, feature management and online serving types, deprecations page, VPC Service Controls, Private Service Connect interface for training; search snippets only, not opened; details hedged 'check current docs')
**Say this first (1 line):** Vertex AI Feature Store today means BigQuery as the offline source plus feature groups and feature views synced to online serving (Bigtable-backed is the recommended path), the legacy store and optimized online serving carry published deprecation dates, and Azure ML has a separate managed feature store workspace, so I never start new work on a deprecated service.

**Then explain:**
- **Vertex current design:** features live in BigQuery tables or views. A feature group points at the BigQuery source. A feature view picks features from groups and syncs them to an online store on a schedule (cron) or manually. Check current docs for exact class names, they have changed.
- **Legacy store:** the old Feature Store (Legacy) and "optimized" online serving were announced as deprecated. From the search snippets of the deprecations page (page not opened, check current docs): deprecated 17 Feb 2026, no new features from 17 May 2026, sunset 17 Feb 2027. The pattern matters more than the dates: managed services get retired, so you keep an exit path.
- **Migration means:** new feature groups and views over the BigQuery source, re-sync to the new online store, switch the serving client to the new read API, dual-read to compare values, then retire the old store. Old online values are not copied for you, you rebuild them from the offline source.
- **Azure side:** a managed feature store is its own workspace type. You define a feature store entity, a feature set (with a transformation spec) and materialise to offline and online stores. SDK shape: `FeatureStore`, `FeatureStoreEntity`, `FeatureSet`. Not one-to-one with Vertex, check current docs for status.
- **Failure modes:** online and offline values drift if sync is slow, a sync schedule that is too rare serves stale features, a point-in-time-wrong join leaks the future (Part 9 owns that), and building on a deprecated service means a forced migration on someone else's calendar.

**Example:** a fraud team has features in BigQuery and online serving on the legacy store. Today is 2026-10-26. By the snippet dates the store is past its "no new features" mark, so the checker below says HIGH: plan the migration this quarter. A design on Bigtable-backed serving says ok. Hand check: 26 Oct 2026 is after 17 May 2026 and before 17 Feb 2027, so HIGH, not BLOCKER.

**Code:** two scripts, run with two different venvs (gcp and az). Nothing was created in any cloud.
```python
# ---- q19_gcp_featurestore.py ----
"""Q19 Vertex side: FeatureView proto offline + deprecation-clock checker. No network."""
import warnings; warnings.filterwarnings("ignore")
from datetime import date
import importlib.metadata as md
from google.cloud.aiplatform_v1beta1.types import FeatureView
print("google-cloud-aiplatform", md.version("google-cloud-aiplatform"))

# Current design: a FeatureView syncs from a BigQuery source on a cron schedule.
fv = FeatureView(
    big_query_source=FeatureView.BigQuerySource(
        uri="bq://my-proj.fs_demo.user_features", entity_id_columns=["user_id"]),
    sync_config=FeatureView.SyncConfig(cron="0 */6 * * *"),
)
print(FeatureView.to_json(fv, indent=None))

# Deprecation clock. Dates are from search snippets of the docs-deprecations page, NOT opened.
SNIPPET_DATES = {"deprecated": date(2026, 2, 17), "no_new_features": date(2026, 5, 17), "sunset": date(2027, 2, 17)}
LEGACY = {"legacy_featurestore", "optimized_online_serving"}

def risk(design: dict, today: date) -> str:
    uses = design.get("online_serving")
    if uses not in LEGACY:
        return "ok: not on the legacy services (still check current docs)"
    if today >= SNIPPET_DATES["sunset"]:
        return "BLOCKER: past the snippet sunset date, migrate now"
    if today >= SNIPPET_DATES["no_new_features"]:
        return "HIGH: no new features expected, plan the migration this quarter"
    if today >= SNIPPET_DATES["deprecated"]:
        return "MEDIUM: deprecated, do not start new work on it"
    return "LOW: not deprecated yet by the snippet dates"

for d in [{"online_serving": "legacy_featurestore"}, {"online_serving": "bigtable"},
          {"online_serving": "optimized_online_serving"}]:
    for t in (date(2026, 1, 1), date(2026, 10, 26), date(2027, 3, 1)):
        print(t, d["online_serving"], "->", risk(d, t))

# ---- q19_azure_featurestore.py ----
"""Q19 Azure side: managed feature store entities built offline (nothing is created)."""
import warnings; warnings.filterwarnings("ignore")
import importlib.metadata as md
from azure.ai.ml.entities import FeatureStore, FeatureStoreEntity, FeatureSet, FeatureSetSpecification, DataColumn
print("azure-ai-ml", md.version("azure-ai-ml"))
fs = FeatureStore(name="fs-demo", location="centralindia")
print(type(fs).__name__, fs.name, fs.location)
ent = FeatureStoreEntity(name="account", version="1", index_columns=[DataColumn(name="accountID", type="string")], stage="Development")
print(type(ent).__name__, ent.name, ent.version, [c.name for c in ent.index_columns])
fset = FeatureSet(name="txn_agg", version="1", entities=["azureml:account:1"],
                  specification=FeatureSetSpecification(path="./featureset_spec"), stage="Development")
print(type(fset).__name__, fset.name, fset.version, fset.entities)
```

**Output (my run):** `python -I` in venvs with google-cloud-aiplatform 1.165.1 and azure-ai-ml 1.35.2. Proto and entity objects were built offline. Not executed: the docs-deprecations page (the snippets were the only source, WebFetch failed earlier), any real Feature Store, BigQuery, Bigtable, sync job or Azure materialisation. Dates are from snippets and hedged.
```text
$ python -I q19_gcp_featurestore.py
google-cloud-aiplatform 1.165.1
{"bigQuerySource": {"uri": "bq://my-proj.fs_demo.user_features", "entityIdColumns": ["user_id"]}, "syncConfig": {"cron": "0 */6 * * *"}, "name": "", "etag": "", "labels": {}, "serviceAgentType": 0, "serviceAccountEmail": "", "satisfiesPzs": false, "satisfiesPzi": false}
2026-01-01 legacy_featurestore -> LOW: not deprecated yet by the snippet dates
2026-10-26 legacy_featurestore -> HIGH: no new features expected, plan the migration this quarter
2027-03-01 legacy_featurestore -> BLOCKER: past the snippet sunset date, migrate now
2026-01-01 bigtable -> ok: not on the legacy services (still check current docs)
2026-10-26 bigtable -> ok: not on the legacy services (still check current docs)
2027-03-01 bigtable -> ok: not on the legacy services (still check current docs)
2026-01-01 optimized_online_serving -> LOW: not deprecated yet by the snippet dates
2026-10-26 optimized_online_serving -> HIGH: no new features expected, plan the migration this quarter
2027-03-01 optimized_online_serving -> BLOCKER: past the snippet sunset date, migrate now

$ python -I q19_azure_featurestore.py
azure-ai-ml 1.35.2
FeatureStore fs-demo centralindia
FeatureStoreEntity account 1 ['accountID']
FeatureSet txn_agg 1 ['azureml:account:1']
```

**Follow-ups:**
- *Why not just wait until the sunset date?* The cost is migration under deadline plus no new features. Start with a dual-read pilot now.
- *Where do features come from if not the store?* From the BigQuery tables or views, the store is a serving copy. Keep the transformation in version-controlled SQL or code.
- *Do I even need a managed store?* Only if online low-latency lookups need shared, consistent features. Otherwise a batch table is enough (Part 9).

**Common mistakes:**
- Starting a new project on a service whose docs page says deprecated.
- Quoting deprecation dates from memory or a blog instead of the vendor page on the day.
- Forgetting that online values must be re-synced after migration.
- Treating the Azure feature store as a drop-in for Vertex.

### Q20 ⭐⭐ 🟡 Model monitoring services: Vertex AI Model Monitoring (training-serving skew and prediction drift, baseline, sampling rate, schedule, alert channels) and Azure ML model monitoring (signals, thresholds, a monitor schedule), at the configuration level only. Part 8 owns drift maths and alerting design. Build the Azure monitor entities offline if the import works, write a config checker for a monitoring spec (baseline set, sample rate in range, alert target present), and list what each service does not do for you (labels, business metrics, retraining).
**Asked at:** Azure ML interview question lists (javainuse 'azure ml' list incl. managed online endpoints and MLOps in Azure ML, a Medium scenario-based Azure ML post by mihirpopat covering registry-then-promote across dev, staging and prod; search snippets only, not opened; WebFetch of learn.microsoft.com failed with getaddrinfo ENOTFOUND); editorial prep sites, not verified candidate reports; ML engineer and MLOps roles at Azure-heavy IT-services firms and GCCs | GCP Vertex AI interview question list (javainuse 'gcp vertex ai' 2026 list: Vertex Pipelines, Feature Store, Model Registry, model monitoring, MLOps, model versioning; search snippet only, not opened); editorial prep site, not verified candidate reports; ML engineer and MLOps roles at GCP-using product companies and cloud-consulting firms | Google Cloud Vertex AI documentation pages as returned by search (MLOps on Vertex AI, feature management and online serving types, deprecations page, VPC Service Controls, Private Service Connect interface for training; search snippets only, not opened; details hedged 'check current docs') | Microsoft Learn Azure Machine Learning pages as returned by search (MLOps model management and deployment, managed online endpoints, managed network isolation, enterprise security, online-endpoint YAML reference, SDK v1 to v2 migration; search snippets and mirrors on docs.azure.cn and mintlify, none opened; details hedged 'check current docs')
**Say this first (1 line):** Both services compare production data to a baseline on a schedule, on a sample, against thresholds, and send an alert; neither one gives you labels, business metrics or retraining, so those stay your job.

**Then explain:**
- **Vertex Model Monitoring (v1 objects):** baseline is the training dataset (BigQuery, Cloud Storage) for skew, or the previous window for drift. You set per-feature thresholds, a sampling rate for logged requests, a schedule interval, and an alert config (email, Cloud Monitoring channels). There is also a newer monitoring design; check current docs which one your project should use, I could not confirm its status.
- **Azure ML model monitoring:** a monitor schedule runs a monitor definition on Spark compute. The definition has a target (endpoint deployment), signals (data drift, data quality, prediction drift, feature attribution drift, model performance) with metric thresholds, and an alert notification. Production data comes from collected inference data.
- **Not done for you:** collecting ground truth, computing business KPIs, deciding the retrain trigger, running the retrain, rollback. Delayed labels mean model performance signals lag (Part 8).
- **Failure modes:** no baseline means nothing to compare, a sample rate that is too low misses rare classes, thresholds copied from a blog fire daily and get muted, alerts to a mailbox nobody reads, schema change in logged data breaks the job silently.

**Example:** daily Azure monitor with drift, quality and prediction-drift signals and one alert email: built offline below. The checker flags a spec with an empty baseline, sample rate 1.5, no alert target and no thresholds, and passes the good spec. Hand check: 4 problems in the bad spec (the schedule is present).

**Code:** Azure and Vertex configuration objects plus a config checker. Nothing was sent.
```python
# ---- q20_monitoring.py ----
"""Q20: monitoring configs offline. Azure MonitorDefinition/MonitorSchedule built (not created);
Vertex ModelMonitoringObjectiveConfig proto printed by the gcp venv separately (q20_vertex.py)."""
import warnings; warnings.filterwarnings("ignore")
import importlib.metadata as md
from azure.ai.ml.entities import (MonitorDefinition, MonitorSchedule, MonitoringTarget, DataDriftSignal,
    DataQualitySignal, PredictionDriftSignal, AlertNotification, ServerlessSparkCompute, RecurrenceTrigger,
    RecurrencePattern, PredictionDriftMetricThreshold)
print("azure-ai-ml", md.version("azure-ai-ml"))
md_ = MonitorDefinition(
    compute=ServerlessSparkCompute(instance_type="standard_e4s_v3", runtime_version="3.4"),
    monitoring_target=MonitoringTarget(ml_task="classification", endpoint_deployment_id="azureml:my-ep:blue"),
    monitoring_signals={"drift": DataDriftSignal(), "quality": DataQualitySignal(), "pred": PredictionDriftSignal(metric_thresholds=PredictionDriftMetricThreshold())},
    alert_notification=AlertNotification(emails=["mlops@example.com"]),
)
sched = MonitorSchedule(name="daily-monitor", trigger=RecurrenceTrigger(frequency="day", interval=1,
        schedule=RecurrencePattern(hours=3, minutes=0)), create_monitor=md_)
print(type(sched).__name__, sched.name, sorted(md_.monitoring_signals), md_.alert_notification.emails)

# ---- config checker (works on a plain dict so it also fits a Vertex-style spec) ----
def check_monitor(spec: dict) -> list[str]:
    errs = []
    if not spec.get("baseline"): errs.append("no baseline set (training data or reference window)")
    r = spec.get("sample_rate")
    if r is None or not (0 < r <= 1): errs.append(f"sample_rate {r!r} not in (0, 1]")
    if not spec.get("alert_targets"): errs.append("no alert target (email, channel, webhook)")
    if not spec.get("schedule"): errs.append("no schedule")
    if not spec.get("thresholds"): errs.append("no thresholds: signals would never fire")
    return errs

good = {"baseline": "train_v7", "sample_rate": 0.1, "alert_targets": ["mlops@example.com"],
        "schedule": "daily", "thresholds": {"psi": 0.2}}
bad = {"baseline": "", "sample_rate": 1.5, "alert_targets": [], "schedule": "daily", "thresholds": {}}
for name, s in [("good", good), ("bad", bad)]:
    print(name, "->", check_monitor(s) or "OK")

# ---- q20_vertex.py ----
"""Q20 Vertex side: ModelMonitoringObjectiveConfig proto built offline (v1beta1 types); nothing sent."""
import warnings; warnings.filterwarnings("ignore")
import importlib.metadata as md
from google.cloud.aiplatform_v1.types import (ModelDeploymentMonitoringObjectiveConfig, ModelMonitoringObjectiveConfig,
    ModelMonitoringAlertConfig, SamplingStrategy, ThresholdConfig)
print("google-cloud-aiplatform", md.version("google-cloud-aiplatform"))
obj = ModelMonitoringObjectiveConfig(
    training_dataset=ModelMonitoringObjectiveConfig.TrainingDataset(
        bigquery_source={"input_uri": "bq://my-proj.ds.train"}, target_field="label"),
    training_prediction_skew_detection_config=ModelMonitoringObjectiveConfig.TrainingPredictionSkewDetectionConfig(
        skew_thresholds={"age": ThresholdConfig(value=0.3)}),
    prediction_drift_detection_config=ModelMonitoringObjectiveConfig.PredictionDriftDetectionConfig(
        drift_thresholds={"age": ThresholdConfig(value=0.3)}))
dep = ModelDeploymentMonitoringObjectiveConfig(deployed_model_id="1234", objective_config=obj)
sampling = SamplingStrategy(random_sample_config=SamplingStrategy.RandomSampleConfig(sample_rate=0.2))
alert = ModelMonitoringAlertConfig(email_alert_config=ModelMonitoringAlertConfig.EmailAlertConfig(user_emails=["mlops@example.com"]))
print("sample_rate", sampling.random_sample_config.sample_rate, "| emails", list(alert.email_alert_config.user_emails))
print("skew thresholds:", {k: v.value for k, v in obj.training_prediction_skew_detection_config.skew_thresholds.items()})
print("types:", type(dep).__name__, type(obj).__name__)
```

**Output (my run):** azure-ai-ml 1.35.2 (az venv) and google-cloud-aiplatform 1.165.1 (gcp venv), `python -I`. Entities and protos built offline; no monitor was created. Not executed: any scheduled monitor run, Spark compute, Cloud Monitoring alerts. The Azure `PredictionDriftSignal` needed explicit `metric_thresholds` (my first run raised a TypeError), which shows constructor shapes change between versions.
```text
$ python -I q20_monitoring.py
azure-ai-ml 1.35.2
MonitorSchedule daily-monitor ['drift', 'pred', 'quality'] ['mlops@example.com']
good -> OK
bad -> ['no baseline set (training data or reference window)', 'sample_rate 1.5 not in (0, 1]', 'no alert target (email, channel, webhook)', 'no thresholds: signals would never fire']

$ python -I q20_vertex.py
google-cloud-aiplatform 1.165.1
sample_rate 0.2 | emails ['mlops@example.com']
skew thresholds: {'age': 0.3}
types: ModelDeploymentMonitoringObjectiveConfig ModelMonitoringObjectiveConfig
```

**Follow-ups:**
- *Who decides the threshold?* Start from history of normal days, review after a month. The drift maths is in Part 8.
- *Skew versus drift?* Skew is training versus serving now, drift is serving now versus serving earlier.
- *What triggers retraining?* A policy you write; the service only alerts.

**Common mistakes:**
- Turning on monitoring with no baseline or no owner for the alert.
- Sampling 100 percent on a busy endpoint and being surprised by log volume (cost depth: Part 12).
- Calling drift an accuracy drop. It is a warning, not proof.

### Q21 ⭐⭐ 🟡 AutoML in Azure ML versus Vertex AI AutoML: supported task types, what you give it (an MLTable or a managed dataset), limits and timeouts, primary metric, explainability and guardrails, and when you refuse to use it (leakage, tiny data, strict latency, need for custom features). Build an Azure automl.classification job offline with limits set, print its settings, and say what a trained AutoML model gives you for registry and deployment. Book 1 owns ML theory.
**Asked at:** Azure ML interview question lists (javainuse 'azure ml' list incl. managed online endpoints and MLOps in Azure ML, a Medium scenario-based Azure ML post by mihirpopat covering registry-then-promote across dev, staging and prod; search snippets only, not opened; WebFetch of learn.microsoft.com failed with getaddrinfo ENOTFOUND); editorial prep sites, not verified candidate reports; ML engineer and MLOps roles at Azure-heavy IT-services firms and GCCs | GCP Vertex AI interview question list (javainuse 'gcp vertex ai' 2026 list: Vertex Pipelines, Feature Store, Model Registry, model monitoring, MLOps, model versioning; search snippet only, not opened); editorial prep site, not verified candidate reports; ML engineer and MLOps roles at GCP-using product companies and cloud-consulting firms | Certification-style question families (Microsoft DP-100 study guide and its replacement AI-300 as reported by third-party sites, Google Cloud Professional Machine Learning Engineer exam-prep listings; mentioned as a source type only, no exam questions reproduced; skills lists conflicted between sources, so verify on the vendor pages)
**Say this first (1 line):** AutoML tries many models and preprocessing for you under a time and trial budget, which is a fast baseline for tabular data, but I refuse it when leakage risk, tiny data, strict latency or custom features matter more than speed.

**Then explain:**
- **Azure ML AutoML:** SDK v2 `automl.classification`, `regression`, `forecasting`, plus image and text tasks (check current docs for the exact list). You give it an MLTable data input, a target column, a primary metric, validation (for example cross-validation folds) and limits (total timeout, per-trial timeout, max trials, concurrency, early termination). You can allow or block algorithms and ask for ONNX-compatible models.
- **Vertex AI AutoML:** a managed dataset or BigQuery table in, an optimization objective (for example `maximize-au-roc`) and a node-hour budget out. Supported data types and task names move between releases, check current docs.
- **What you get back:** a trained model with the best run, explainability and a model object you register and deploy like any other. Check the generated model's inputs: AutoML does its own featurization, so serving must apply the same one.
- **Refuse it when:** the target leaks (a column that is only known after the outcome), you have a few hundred rows, latency budget is tight and the winner is a big ensemble, regulators need a model you can fully describe, or the value is in hand-built features.
- **Failure modes:** leaky column wins by a huge margin (a warning sign, not a success), time budget too short to finish, a random split on time-ordered data, and treating the leaderboard as the final test.

**Example:** churn data with 3-fold cross-validation, primary metric AUC weighted, 60 minutes total, 10 per trial, 20 trials, 2 in parallel. Hand check: 20 trials at 2 in parallel is about 10 rounds, so up to roughly 100 minutes if every trial used its full 10 minutes, which is more than the 60-minute cap. The cap wins, so not every trial may run. Raise the timeout or cut the trials.

**Code:** both jobs built offline, nothing submitted.
```python
# ---- q21_automl_azure.py ----
"""Q21 Azure: automl.classification built offline. Nothing submitted."""
import warnings; warnings.filterwarnings("ignore")
import importlib.metadata as md
from azure.ai.ml import automl, Input
print("azure-ai-ml", md.version("azure-ai-ml"))
j = automl.classification(compute="cpu-cluster", experiment_name="churn-automl",
        training_data=Input(type="mltable", path="./train_mltable"), target_column_name="churned",
        primary_metric="AUC_weighted", n_cross_validations=3, enable_model_explainability=True)
j.set_limits(timeout_minutes=60, trial_timeout_minutes=10, max_trials=20, max_concurrent_trials=2, enable_early_termination=True)
j.set_training(allowed_training_algorithms=["LightGBM", "LogisticRegression"], enable_onnx_compatible_models=True)
print("task:", j.task_type, "| metric:", j.primary_metric, "| target:", j.target_column_name)
L = j.limits
print("limits:", dict(timeout_minutes=L.timeout_minutes, trial_timeout_minutes=L.trial_timeout_minutes,
      max_trials=L.max_trials, max_concurrent_trials=L.max_concurrent_trials, early=L.enable_early_termination))
print("allowed algos:", j.training.allowed_training_algorithms, "| onnx:", j.training.enable_onnx_compatible_models)

# ---- q21_automl_vertex.py ----
"""Q21 Vertex: AutoMLTabularTrainingJob constructed offline with anonymous credentials. run() NOT called."""
import warnings; warnings.filterwarnings("ignore")
import importlib.metadata as md
from google.auth.credentials import AnonymousCredentials
import google.cloud.aiplatform as aip
print("google-cloud-aiplatform", md.version("google-cloud-aiplatform"))
aip.init(project="demo-proj", location="asia-south1", credentials=AnonymousCredentials())
job = aip.AutoMLTabularTrainingJob(display_name="churn-automl", optimization_prediction_type="classification",
        optimization_objective="maximize-au-roc")
print(type(job).__name__, "| objective:", job._optimization_objective, "| type:", job._optimization_prediction_type)
print("run() signature has budget arg:", "budget_milli_node_hours" in job.run.__code__.co_varnames)
```

**Output (my run):** azure-ai-ml 1.35.2 and google-cloud-aiplatform 1.165.1, `python -I`. Objects constructed offline; the Vertex training job was not run and the Azure job was not submitted. Not executed: any AutoML training, explainability output, registry or deployment of an AutoML model. I did not run the SDK featurization or validation printing beyond what is shown.
```text
$ python -I q21_automl_azure.py
azure-ai-ml 1.35.2
task: TaskType.CLASSIFICATION | metric: ClassificationPrimaryMetrics.AUC_WEIGHTED | target: churned
limits: {'timeout_minutes': 60, 'trial_timeout_minutes': 10, 'max_trials': 20, 'max_concurrent_trials': 2, 'early': True}
allowed algos: [<ClassificationModels.LIGHT_GBM: 'LightGBM'>, <ClassificationModels.LOGISTIC_REGRESSION: 'LogisticRegression'>] | onnx: True

$ python -I q21_automl_vertex.py
google-cloud-aiplatform 1.165.1
AutoMLTabularTrainingJob | objective: maximize-au-roc | type: classification
run() signature has budget arg: True
```

**Follow-ups:**
- *How do you stop leakage?* Split by time or by group first, drop post-outcome columns, check feature importance for suspicious winners.
- *Is AutoML a replacement for a data scientist?* No. It is a baseline and a time saver.
- *Where does it fit in the registry?* The output is a model like another: register it, tag the data version and the job id.

**Common mistakes:**
- Trusting the leaderboard without a final holdout.
- Letting AutoML pick features from an ID or timestamp column.
- Forgetting that the deployed model needs the same featurization.

### Q22 ⭐⭐ 🟡 Hyperparameter tuning as a service: Azure ML sweep jobs (search space, sampling algorithm, primary metric and goal, early termination such as Bandit, trial limits) versus Vertex AI HyperparameterTuningJob and Vizier (metric spec, parameter spec, trial counts, parallel trials, Bayesian search). Build a sweep job and a HyperparameterTuningJob offline, show both specs, and explain why parallel trials and Bayesian search pull against each other. Book 1 owns tuning theory.
**Asked at:** Azure ML interview question lists (javainuse 'azure ml' list incl. managed online endpoints and MLOps in Azure ML, a Medium scenario-based Azure ML post by mihirpopat covering registry-then-promote across dev, staging and prod; search snippets only, not opened; WebFetch of learn.microsoft.com failed with getaddrinfo ENOTFOUND); editorial prep sites, not verified candidate reports; ML engineer and MLOps roles at Azure-heavy IT-services firms and GCCs | GCP Vertex AI interview question list (javainuse 'gcp vertex ai' 2026 list: Vertex Pipelines, Feature Store, Model Registry, model monitoring, MLOps, model versioning; search snippet only, not opened); editorial prep site, not verified candidate reports; ML engineer and MLOps roles at GCP-using product companies and cloud-consulting firms | Google Cloud Vertex AI documentation pages as returned by search (MLOps on Vertex AI, feature management and online serving types, deprecations page, VPC Service Controls, Private Service Connect interface for training; search snippets only, not opened; details hedged 'check current docs')
**Say this first (1 line):** Both clouds run a hyperparameter search as a managed job of trials over your training code, with a metric, a search space and trial limits; and more parallel trials means faster wall-clock but a Bayesian search learns from fewer finished results.

**Then explain:**
- **Azure ML sweep job:** you take a command job, replace inputs with a search space (`Uniform`, `Choice` and so on), call `.sweep()` with sampling algorithm (random, grid, bayesian), primary metric and goal, then set limits (total trials, concurrent trials, timeout). Early termination (Bandit, median stopping, truncation) is an optional policy. The docs say Bayesian sampling does not support early termination policies (check current docs), so I paired Bandit with random sampling.
- **Vertex AI HyperparameterTuningJob (Vizier):** a `custom_job` is the trial template, `metric_spec` has the metric and goal, `parameter_spec` has Double, Integer, Discrete or Categorical parameters with a scale, and `max_trial_count` and `parallel_trial_count` set the budget. If the algorithm is unset the service picks its default, which is Bayesian-style optimization, check current docs.
- **Your script must report the metric:** in Azure, log the metric the sweep names (MLflow); in Vertex, report through the hypertune helper library or the documented mechanism, otherwise trials finish with no value.
- **Why parallel and Bayesian fight:** a Bayesian method proposes the next point from finished trials. If P trials run at once, a new trial is proposed with up to P-1 results still missing. With P equal to the trial count it is just random search.
- **Failure modes:** metric name mismatch (all trials look failed), too-wide log-scale ranges, each trial paying cold start, tuning on the test set, and quota limiting real concurrency below what you set.

**Example:** 20 trials. Parallel 1: trial 10 sees 9 finished results. Parallel 4: trial 10 sees 6. Parallel 20: trial 10 sees 0. Hand check: trial i sees about i minus P finished results, never below 0. With parallel 4 the first 4 trials are proposed blind.

**Code:** Azure sweep, Vertex tuning job, plus the small count of what each trial can see.
```python
# ---- q22_tuning.py ----
"""Q22 Azure sweep job offline + the parallel-vs-Bayesian arithmetic (pure Python)."""
import warnings; warnings.filterwarnings("ignore")
import importlib.metadata as md
from azure.ai.ml import command
from azure.ai.ml.sweep import Uniform, Choice, BanditPolicy
print("azure-ai-ml", md.version("azure-ai-ml"))
base = command(code=".", command="python train.py --lr ${{inputs.lr}} --depth ${{inputs.depth}}",
               inputs={"lr": 0.1, "depth": 4}, environment="azureml:train-env:1", compute="cpu-cluster")
sw = base(lr=Uniform(min_value=0.001, max_value=0.1), depth=Choice(values=[3, 4, 6])).sweep(
        sampling_algorithm="bayesian", primary_metric="auc", goal="maximize")
sw.set_limits(max_total_trials=20, max_concurrent_trials=4, timeout=3600)
print(type(sw).__name__, "| sampling:", sw.sampling_algorithm, "| goal:", sw.objective.goal, "| metric:", sw.objective.primary_metric)
print("limits: total", sw.limits.max_total_trials, "concurrent", sw.limits.max_concurrent_trials)
print("search space:", {k: type(v).__name__ for k, v in sw.search_space.items()})

# Bandit early termination goes on a random-sampling sweep (docs say Bayesian does not support
# early-termination policies: check current docs).
sw2 = base(lr=Uniform(min_value=0.001, max_value=0.1), depth=Choice(values=[3, 4, 6])).sweep(
        sampling_algorithm="random", primary_metric="auc", goal="maximize")
sw2.set_limits(max_total_trials=20, max_concurrent_trials=4)
sw2.early_termination = BanditPolicy(slack_factor=0.1, evaluation_interval=1, delay_evaluation=2)
print("sweep2:", sw2.sampling_algorithm, "+", type(sw2.early_termination).__name__, "slack", sw2.early_termination.slack_factor)

# Why parallel trials and Bayesian search pull against each other: a Bayesian suggester only learns from
# FINISHED trials. With P trials running at once, trial i (1-based) starts after at most i-P finished.
def informed_trials(total, parallel):
    return [max(0, i - parallel) for i in range(1, total + 1)]   # finished results visible when trial i is proposed
for p in (1, 4, 20):
    seen = informed_trials(20, p)
    print(f"parallel={p:2d}: results seen by trial 5={seen[4]}, trial 10={seen[9]}, trial 20={seen[19]}, trials proposed blind={sum(1 for x in seen if x==0)}")

# ---- q22_vertex_hpt.py ----
"""Q22 Vertex HyperparameterTuningJob built offline (anonymous creds). run() NOT called."""
import warnings; warnings.filterwarnings("ignore")
import importlib.metadata as md
from google.auth.credentials import AnonymousCredentials
import google.cloud.aiplatform as aip
from google.cloud.aiplatform import hyperparameter_tuning as hpt
print("google-cloud-aiplatform", md.version("google-cloud-aiplatform"))
aip.init(project="demo-proj", location="asia-south1", staging_bucket="gs://demo-stage-bkt", credentials=AnonymousCredentials())
cj = aip.CustomJob(display_name="trial-template", worker_pool_specs=[{"machine_spec": {"machine_type": "n1-standard-4"},
        "replica_count": 1, "container_spec": {"image_uri": "asia-south1-docker.pkg.dev/demo-proj/repo/train:1"}}])
h = aip.HyperparameterTuningJob(display_name="hpt", custom_job=cj, metric_spec={"auc": "maximize"},
        parameter_spec={"lr": hpt.DoubleParameterSpec(min=0.001, max=0.1, scale="log"),
                        "depth": hpt.DiscreteParameterSpec(values=[3, 4, 6], scale=None)},
        max_trial_count=20, parallel_trial_count=4, search_algorithm=None)
spec = h._gca_resource.trial_job_spec
print(type(h).__name__, "| max_trials", h._gca_resource.max_trial_count, "| parallel", h._gca_resource.parallel_trial_count)
print("metrics:", [(m.metric_id, m.goal.name) for m in h._gca_resource.study_spec.metrics])
print("params:", [(p.parameter_id, p.scale_type.name) for p in h._gca_resource.study_spec.parameters])
print("algorithm (unset = service default):", h._gca_resource.study_spec.algorithm.name)
```

**Output (my run):** azure-ai-ml 1.35.2 and google-cloud-aiplatform 1.165.1, `python -I`; objects built offline (Vertex with anonymous credentials, `run()` not called). The informed-trials count is my simplified model of a sequential suggester, not a measurement of Vizier or Azure internals. Not executed: any trial, quota check or search result.
```text
$ python -I q22_tuning.py
azure-ai-ml 1.35.2
Sweep | sampling: bayesian | goal: maximize | metric: auc
limits: total 20 concurrent 4
search space: {'lr': 'Uniform', 'depth': 'Choice'}
sweep2: random + BanditPolicy slack 0.1
parallel= 1: results seen by trial 5=4, trial 10=9, trial 20=19, trials proposed blind=1
parallel= 4: results seen by trial 5=1, trial 10=6, trial 20=16, trials proposed blind=4
parallel=20: results seen by trial 5=0, trial 10=0, trial 20=0, trials proposed blind=20

$ python -I q22_vertex_hpt.py
google-cloud-aiplatform 1.165.1
HyperparameterTuningJob | max_trials 20 | parallel 4
metrics: [('auc', 'MAXIMIZE')]
params: [('lr', 'UNIT_LOG_SCALE'), ('depth', 'SCALE_TYPE_UNSPECIFIED')]
algorithm (unset = service default): ALGORITHM_UNSPECIFIED
```

**Follow-ups:**
- *What parallelism would you pick?* A small share of the trial budget (for example 4 of 20), then check results. Do not pick it from a rule of thumb alone.
- *When is random search enough?* Few parameters, cheap trials, or when you run many in parallel.
- *Why log scale for learning rate?* Good values span orders of magnitude.

**Common mistakes:**
- Setting concurrency above the cluster's real node count so trials queue.
- Reporting the metric under a different name than the spec.
- Reading a best-trial score as the expected production score.

### Q23 ⭐⭐ 🟡 Azure ML network isolation: workspace public_network_access, a private endpoint for inbound access, the managed virtual network for outbound control (allow internet outbound versus allow only approved outbound, outbound rules, private endpoints to Storage, Key Vault and Container Registry), and securing a managed online endpoint. Build a Workspace entity with public access disabled offline, write a checker for a network config, and name the deployment-time RBAC that managed-network creation needs. Part 12 owns security design in depth.
**Asked at:** Microsoft Learn Azure Machine Learning pages as returned by search (MLOps model management and deployment, managed online endpoints, managed network isolation, enterprise security, online-endpoint YAML reference, SDK v1 to v2 migration; search snippets and mirrors on docs.azure.cn and mintlify, none opened; details hedged 'check current docs') | Azure ML interview question lists (javainuse 'azure ml' list incl. managed online endpoints and MLOps in Azure ML, a Medium scenario-based Azure ML post by mihirpopat covering registry-then-promote across dev, staging and prod; search snippets only, not opened; WebFetch of learn.microsoft.com failed with getaddrinfo ENOTFOUND); editorial prep sites, not verified candidate reports; ML engineer and MLOps roles at Azure-heavy IT-services firms and GCCs
**Say this first (1 line):** Close the front door with public_network_access disabled plus a private endpoint, control the back door with the managed virtual network (allow only approved outbound, private endpoints to Storage, Key Vault and Container Registry), and make sure whoever creates it has the RBAC to build private endpoints.

**Then explain:**
- **Inbound:** set the workspace `public_network_access` to Disabled and add a private endpoint in your own VNet. Users and CI then reach the workspace only through that network (VPN, ExpressRoute or a jump host).
- **Outbound:** the managed virtual network is created and run by the service for compute. Isolation modes as named in the SDK: disabled, allow internet outbound, allow only approved outbound (check current docs for names). In the strict mode you add outbound rules: FQDN rules (for example a package mirror) and private endpoint rules to the workspace's Storage, Key Vault and Container Registry.
- **Online endpoints:** a managed online endpoint has its own public network access setting; set it to disabled so scoring is private as well (check current docs for the current property and for the workspace-level interplay).
- **RBAC for creating it:** the identity that provisions the managed network needs permission to create private endpoints and to read the target resources (from snippets: rights on the Storage account and others, Reader on storage private endpoints; the exact role list is version-specific, check current docs).
- **Failure modes:** a Docker image pull or `pip install` fails because outbound is closed and no rule exists, workspace is private but the CI runner is on the public internet, DNS for private endpoints not resolved from your network, and "allow internet outbound" left on forever "for now".

**Example:** a bank GCC sets Disabled public access, strict outbound, three private endpoint rules and one FQDN rule for an internal package mirror. The checker passes it, and fails a sample with public access Enabled, internet outbound and only a storage rule. Hand check: the bad sample has 7 findings (public access, no inbound private endpoint, internet outbound, key vault and registry rules missing, public endpoint, missing deployer RBAC).

**Code:** Workspace entity with a managed network built offline, and a checker.
```python
# ---- q23_azure_network.py ----
"""Q23: Workspace with managed network + checker, offline. Nothing is created."""
import warnings; warnings.filterwarnings("ignore")
import importlib.metadata as md
from azure.ai.ml.entities import Workspace, ManagedNetwork, IsolationMode, FqdnDestination, PrivateEndpointDestination
print("azure-ai-ml", md.version("azure-ai-ml"))
mn = ManagedNetwork(isolation_mode=IsolationMode.ALLOW_ONLY_APPROVED_OUTBOUND, outbound_rules=[
    FqdnDestination(name="pypi", destination="pypi.org"),
    PrivateEndpointDestination(name="pe-storage", service_resource_id="/subscriptions/0000/resourceGroups/rg/providers/Microsoft.Storage/storageAccounts/stdemo", subresource_target="blob", spark_enabled=False)])
ws = Workspace(name="ws-secure", location="centralindia", public_network_access="Disabled", managed_network=mn)
print(type(ws).__name__, ws.location, "public:", ws.public_network_access, "| mode:", ws.managed_network.isolation_mode,
      "| rules:", [(r.name, type(r).__name__) for r in ws.managed_network.outbound_rules])

def check_network(cfg: dict) -> list[str]:
    f = []
    if cfg.get("public_network_access") != "Disabled": f.append("workspace public_network_access is not Disabled")
    if not cfg.get("private_endpoint_inbound"): f.append("no private endpoint for inbound access to the workspace")
    mode = cfg.get("isolation_mode")
    if mode == "disabled": f.append("managed network off: outbound is uncontrolled")
    if mode == "allow_internet_outbound": f.append("internet outbound allowed: exfiltration path open (ok only with a written reason)")
    for dep in ("storage", "key_vault", "container_registry"):
        if dep not in cfg.get("private_endpoint_outbound", []): f.append(f"no outbound private endpoint rule for {dep}")
    for ep in cfg.get("online_endpoints", []):
        if ep.get("public_network_access") != "disabled": f.append(f"endpoint {ep['name']} is public")
    if not cfg.get("deployer_can_create_private_endpoints"): f.append("deployer lacks RBAC to create private endpoints (managed network creation fails)")
    return f

good = {"public_network_access": "Disabled", "private_endpoint_inbound": True, "isolation_mode": "allow_only_approved_outbound",
        "private_endpoint_outbound": ["storage", "key_vault", "container_registry"],
        "online_endpoints": [{"name": "fraud-ep", "public_network_access": "disabled"}], "deployer_can_create_private_endpoints": True}
bad = {"public_network_access": "Enabled", "isolation_mode": "allow_internet_outbound", "private_endpoint_outbound": ["storage"],
       "online_endpoints": [{"name": "fraud-ep", "public_network_access": "enabled"}]}
for n, c in (("good", good), ("bad", bad)):
    r = check_network(c); print(n, "->", "OK" if not r else ""); [print("   -", x) for x in r]
```

**Output (my run):** azure-ai-ml 1.35.2, `python -I`. The Workspace entity was constructed in memory only. Not executed: workspace creation, private endpoints, DNS, outbound rule provisioning, RBAC evaluation. The checker reads a dict I wrote, it does not read Azure. Security design depth is Part 12.
```text
$ python -I q23_azure_network.py
azure-ai-ml 1.35.2
Workspace centralindia public: Disabled | mode: AllowOnlyApprovedOutbound | rules: [('pypi', 'FqdnDestination'), ('pe-storage', 'PrivateEndpointDestination')]
good -> OK
bad -> 
   - workspace public_network_access is not Disabled
   - no private endpoint for inbound access to the workspace
   - internet outbound allowed: exfiltration path open (ok only with a written reason)
   - no outbound private endpoint rule for key_vault
   - no outbound private endpoint rule for container_registry
   - endpoint fraud-ep is public
   - deployer lacks RBAC to create private endpoints (managed network creation fails)
```

**Follow-ups:**
- *Why not allow internet outbound?* It is an exfiltration path. Use it only for a short, written reason.
- *Where do packages come from then?* A mirror reachable via FQDN or private endpoint rules.
- *How do you test it?* A job that tries `pip install` and a blob read from inside the network.

**Common mistakes:**
- Disabling public access and forgetting the build and CI path.
- Forgetting that Storage, Key Vault and registry each need their own rule.
- Assuming a private workspace means a private endpoint for scoring.

### Q24 ⭐⭐ 🟡 Vertex AI network and perimeter controls: VPC Service Controls perimeters (what they protect against, exfiltration, ingress and egress rules), Private Service Connect interface for custom training and pipelines (network attachment, subnet sizing as documented, default internet access blocked inside a perimeter), private endpoints for online prediction, and restricted Google APIs access. A training job works in a dev project and fails in the perimeter: list what you check in order. Write the checklist as a function over a config dict and run it on two samples. No Google call was made.
**Asked at:** Google Cloud Vertex AI documentation pages as returned by search (MLOps on Vertex AI, feature management and online serving types, deprecations page, VPC Service Controls, Private Service Connect interface for training; search snippets only, not opened; details hedged 'check current docs') | GCP Vertex AI interview question list (javainuse 'gcp vertex ai' 2026 list: Vertex Pipelines, Feature Store, Model Registry, model monitoring, MLOps, model versioning; search snippet only, not opened); editorial prep site, not verified candidate reports; ML engineer and MLOps roles at GCP-using product companies and cloud-consulting firms
**Say this first (1 line):** A job that works in dev and fails in the perimeter is almost always a blocked path, not a bad model: so I check identity first, then perimeter membership, then network attachment, DNS, internet use, data location and rules, and I read the denial in the audit logs.

**Then explain:**
- **VPC Service Controls:** a perimeter around projects and services (such as Vertex AI and Cloud Storage) that blocks calls crossing its edge unless an ingress or egress rule allows them. It protects against data exfiltration with stolen credentials. It does not replace IAM: both must allow.
- **Custom training in a perimeter:** from the snippets, the job's data plane needs extra networking. A Private Service Connect interface (network attachment in your VPC, subnet around /28 is the documented size, check current docs) gives the job a path. Default internet access is blocked inside the perimeter.
- **Restricted Google APIs:** DNS for `*.googleapis.com` should resolve to the restricted VIP so API calls stay inside.
- **Online prediction:** private endpoints (a private network path to the endpoint) instead of the shared public one.
- **Service accounts inside a perimeter** are not covered by my sources: check current docs for how service agents and your job account are treated.
- **Failure modes:** `pip install` and `git clone` silently need the internet, the container image sits in a repository outside the perimeter, the bucket project is outside, a dry-run perimeter hides what an enforced one breaks.

**Example:** the dev project is outside any perimeter, so only API and IAM checks matter and it passes. The prod project is inside: its attachment subnet is a /29, DNS is not on the restricted VIP, the job pip installs from the internet and nothing allows the bucket project. The ordered checklist stops at check 6, and four more fail after it. Hand check: /29 has 8 addresses, a /28 has 16, so "prefix length at most 28" is the test.

**Code:** the checklist as a function over a dict.
```python
# ---- q24_vertex_perimeter.py ----
"""Q24: ordered checklist over a config dict. Pure Python, no Google call. Facts hedged: check current docs."""
import ipaddress

def checklist(c: dict) -> list[tuple[int, str, str]]:
    out = []
    def chk(name, ok, hint): out.append((len(out) + 1, name, "PASS" if ok else "FAIL: " + hint))
    chk("Vertex AI API and Storage API enabled in the project", c["apis_enabled"], "enable the APIs")
    chk("job service account has roles on bucket, image repo, project", c["sa_roles_ok"], "fix IAM first: perimeter is the second wall, not the first")
    chk("project perimeter membership matches the intent", c["project_in_perimeter"] == c["perimeter_expected"], "add project to perimeter (or confirm it is meant to be outside)")
    chk("restricted services include aiplatform and storage consistently", c["services_restricted"], "check the restricted-services list")
    chk("job has a network attachment (PSC interface) when data-plane egress is needed", c["network_attachment"], "create attachment, pass it in the job spec")
    ok_subnet = False
    if c["network_attachment"]:
        ok_subnet = ipaddress.ip_network(c["attachment_subnet"]).prefixlen <= 28   # docs recommend /28 or larger, check current docs
    chk("attachment subnet has room (docs recommend /28; check current docs)", ok_subnet or not c["network_attachment"], "subnet too small")
    chk("DNS resolves googleapis.com names to the restricted VIP", c["restricted_vip_dns"], "add private DNS zone for restricted.googleapis.com")
    chk("no step needs the public internet (pip install, git clone, external API)", not c["needs_internet"], "mirror packages in Artifact Registry or allow egress through a controlled proxy")
    chk("images and data live in-perimeter, or an ingress/egress rule names this identity", c["data_in_perimeter"] or c["egress_rule_for_sa"], "add an egress rule for the job service account and the bucket project")
    chk("denials checked in audit logs (dry-run mode first)", c["audit_logs_read"], "read the VPC-SC violation entries")
    return out

dev = dict(apis_enabled=True, sa_roles_ok=True, project_in_perimeter=False, services_restricted=False, network_attachment=False,
           attachment_subnet="10.0.0.0/24", restricted_vip_dns=False, needs_internet=True, data_in_perimeter=True,
           egress_rule_for_sa=False, audit_logs_read=False, perimeter_expected=False)
prod = dict(dev, perimeter_expected=True, project_in_perimeter=True, services_restricted=True, network_attachment=True, attachment_subnet="10.9.0.0/29",
            restricted_vip_dns=False, data_in_perimeter=False)

def run(cfg):
    rows = checklist(cfg)
    if not cfg["project_in_perimeter"]:       # outside a perimeter, checks 4-10 are not enforced
        rows = rows[:3]
    return rows

for name, cfg in (("dev project (outside perimeter)", dev), ("prod project (inside perimeter)", prod)):
    rows = run(cfg)
    print("==", name, "->", "first failure: #%d" % next((r[0] for r in rows if r[2] != "PASS"), 0) if any(r[2] != "PASS" for r in rows) else "all checks pass")
    for n, what, res in rows: print(f" {n:2d}. {what}: {res}")
```

**Output (my run):** Python 3.13 `python -I`, no Google libraries needed. No Google call was made and no perimeter existed; the checks encode my reading of the doc snippets and a real denial is found in the audit logs (not executed).
```text
$ python -I q24_vertex_perimeter.py
== dev project (outside perimeter) -> all checks pass
  1. Vertex AI API and Storage API enabled in the project: PASS
  2. job service account has roles on bucket, image repo, project: PASS
  3. project perimeter membership matches the intent: PASS
== prod project (inside perimeter) -> first failure: #6
  1. Vertex AI API and Storage API enabled in the project: PASS
  2. job service account has roles on bucket, image repo, project: PASS
  3. project perimeter membership matches the intent: PASS
  4. restricted services include aiplatform and storage consistently: PASS
  5. job has a network attachment (PSC interface) when data-plane egress is needed: PASS
  6. attachment subnet has room (docs recommend /28; check current docs): FAIL: subnet too small
  7. DNS resolves googleapis.com names to the restricted VIP: FAIL: add private DNS zone for restricted.googleapis.com
  8. no step needs the public internet (pip install, git clone, external API): FAIL: mirror packages in Artifact Registry or allow egress through a controlled proxy
  9. images and data live in-perimeter, or an ingress/egress rule names this identity: FAIL: add an egress rule for the job service account and the bucket project
 10. denials checked in audit logs (dry-run mode first): FAIL: read the VPC-SC violation entries
```

**Follow-ups:**
- *First thing you do on a denial?* Read the violation entry in the audit logs; it names the service, identity and rule that was missing.
- *Dry-run mode?* Logs what would be blocked without blocking: use before enforcing.
- *IAM or perimeter first?* IAM, then perimeter, because the perimeter error can hide a missing role.

**Common mistakes:**
- Opening the perimeter wide "to see if it works" and leaving it.
- Forgetting the image repository and the package source.
- Sizing the attachment subnet too small.

### Q25 ⭐⭐ 🟡 CI/CD authentication and deployment for Azure ML and Vertex AI: GitHub Actions or Azure DevOps to Azure ML with a federated service principal or managed identity and az ml CLI v2 commands, versus GitHub Actions or Cloud Build to Vertex AI with Workload Identity Federation and a deployer service account. Why no long-lived keys, what the deployer identity may and may not do, and where the approval gate sits. Write both workflows as YAML, lint them offline (actionlint or pyyaml), and say nothing was deployed. Part 7 owns CI/CD design and GitHub OIDC to AWS.
**Asked at:** Azure ML interview question lists (javainuse 'azure ml' list incl. managed online endpoints and MLOps in Azure ML, a Medium scenario-based Azure ML post by mihirpopat covering registry-then-promote across dev, staging and prod; search snippets only, not opened; WebFetch of learn.microsoft.com failed with getaddrinfo ENOTFOUND); editorial prep sites, not verified candidate reports; ML engineer and MLOps roles at Azure-heavy IT-services firms and GCCs | Microsoft Learn Azure Machine Learning pages as returned by search (MLOps model management and deployment, managed online endpoints, managed network isolation, enterprise security, online-endpoint YAML reference, SDK v1 to v2 migration; search snippets and mirrors on docs.azure.cn and mintlify, none opened; details hedged 'check current docs') | GCP Vertex AI interview question list (javainuse 'gcp vertex ai' 2026 list: Vertex Pipelines, Feature Store, Model Registry, model monitoring, MLOps, model versioning; search snippet only, not opened); editorial prep site, not verified candidate reports; ML engineer and MLOps roles at GCP-using product companies and cloud-consulting firms | Job-posting and community patterns for Azure-heavy IT-services firms and GCCs (Azure ML plus Azure DevOps) versus GCP-using product companies (Vertex plus BigQuery); inferred from search snippets about ecosystem fit, not from a verified company report
**Say this first (1 line):** CI logs in with a short-lived OIDC token exchanged for a cloud identity (federated credential on Azure, Workload Identity Federation on Google), never a stored key, and the deployer identity can ship to one environment but cannot administer IAM, with the approval gate on the prod environment.

**Then explain:**
- **Azure:** the workflow sets `permissions: id-token: write`, and `azure/login` takes a client id, tenant id and subscription id (not a secret). In Entra, the app registration or managed identity has a federated credential that trusts this repo and branch or environment. Then `az ml job create` and `az ml online-deployment create` run with that identity (needs the `ml` CLI extension, check current docs).
- **Google:** `google-github-actions/auth` takes a workload identity provider and a service account. A pool and provider trust GitHub's token with a condition on repository; the pipeline impersonates the deployer service account. Then `gcloud ai custom-jobs create` and `gcloud ai endpoints deploy-model`. Flag spellings change, check current docs.
- **Why no long-lived keys:** a leaked JSON key or client secret works from anywhere until someone finds and rotates it. A federated token lives for minutes and only for matching claims.
- **Deployer may / may not:** may submit jobs, register models, deploy to the one workspace or project. May not grant roles, edit network or perimeter, read unrelated data. Use separate identities for dev and prod (the two files use different ids).
- **Approval gate:** a GitHub `environment: prod` with required reviewers. The prod login job only starts after approval. Azure DevOps has an equivalent with environments and checks.
- **Failure modes:** federated credential subject does not match the branch or environment (login fails with an obscure error), `id-token: write` missing, one identity for all stages, and a train job that deploys without a gate.

**Example:** two workflows, train then deploy-prod behind a gate. Lint rules I run: id-token permission present, a federated login step in every job, no secret-looking key, actions pinned with `@`, deploy jobs have an environment. The bad sample has three findings. Hand check: bad.yml lacks the permission, uses `AZURE_CREDENTIALS`, and has a deploy job with no environment, so 3.

**Code:** a linter (python) and the two workflows (yaml).
```python
# ---- q25_lint_workflows.py ----
"""Q25: offline lint with pyyaml. No deploy, no network. (actionlint is not installed here.)"""
import sys, re, yaml
SECRET_PAT = re.compile(r"(client[-_]secret|credentials_json|AZURE_CREDENTIALS|private_key|\.json)", re.I)

def lint(path):
    doc = yaml.safe_load(open(path))
    trig = doc.get("on", doc.get(True))             # pyyaml (YAML 1.1) reads the key `on` as boolean True
    errs = []
    perms = doc.get("permissions", {})
    if perms.get("id-token") != "write": errs.append("workflow lacks permissions.id-token: write (OIDC login would fail)")
    text = open(path).read()
    for line in text.splitlines():
        code = line.split("#")[0]
        if SECRET_PAT.search(code): errs.append(f"long-lived credential pattern: {code.strip()}")
    for name, job in doc["jobs"].items():
        steps = job["steps"]
        login = [s for s in steps if str(s.get("uses", "")).startswith(("azure/login", "google-github-actions/auth"))]
        if not login: errs.append(f"job {name}: no federated login step")
        for s in steps:
            if "uses" in s and "@" not in s["uses"]: errs.append(f"job {name}: unpinned action {s['uses']}")
        if "deploy" in name and "environment" not in job: errs.append(f"job {name}: deploy job without an environment (no approval gate)")
    return trig, errs

for p in sys.argv[1:]:
    trig, errs = lint(p)
    print(p.split("/")[-1], "| trigger:", trig)
    for e in errs: print("   -", e)
    if not errs: print("   lint: OK")

# negative test: a bad workflow must be caught
bad = """
name: bad
on: push
jobs:
  deploy-prod:
    runs-on: ubuntu-latest
    steps:
      - uses: azure/login@v2
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}
"""
open("bad.yml", "w").write(bad)
trig, errs = lint("bad.yml"); print("bad.yml |", len(errs), "findings"); [print("   -", e) for e in errs]
import os; os.remove("bad.yml")
```

```yaml
# ---- azure_ml_deploy.yml ----
name: azure-ml-train-and-deploy
on:
  push:
    branches: [main]
permissions:
  id-token: write      # lets the job request an OIDC token
  contents: read
jobs:
  train:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: azure/login@v2           # federated credential: no client secret stored
        with:
          client-id: ${{ vars.AZURE_CLIENT_ID }}
          tenant-id: ${{ vars.AZURE_TENANT_ID }}
          subscription-id: ${{ vars.AZURE_SUBSCRIPTION_ID }}
      - run: az extension add -n ml -y
      - run: >
          az ml job create --file jobs/train.yml
          --resource-group rg-ml --workspace-name ws-ml-dev --stream
  deploy-prod:
    needs: train
    runs-on: ubuntu-latest
    environment: prod                  # required reviewers are set on this environment in repo settings
    steps:
      - uses: actions/checkout@v4
      - uses: azure/login@v2
        with:
          client-id: ${{ vars.AZURE_CLIENT_ID_PROD }}
          tenant-id: ${{ vars.AZURE_TENANT_ID }}
          subscription-id: ${{ vars.AZURE_SUBSCRIPTION_ID }}
      - run: az extension add -n ml -y
      - run: >
          az ml online-deployment create --file deploy/green.yml
          --resource-group rg-ml --workspace-name ws-ml-prod
---
# ---- vertex_deploy.yml ----
name: vertex-train-and-deploy
on:
  push:
    branches: [main]
permissions:
  id-token: write
  contents: read
jobs:
  train:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: google-github-actions/auth@v2     # Workload Identity Federation: no key file
        with:
          workload_identity_provider: projects/123456789/locations/global/workloadIdentityPools/gh-pool/providers/gh-provider
          service_account: vertex-deployer@demo-proj.iam.gserviceaccount.com
      - uses: google-github-actions/setup-gcloud@v2
      - run: >
          gcloud ai custom-jobs create --region=asia-south1 --display-name=train-${{ github.sha }}
          --config=jobs/custom_job.yaml
  deploy-prod:
    needs: train
    runs-on: ubuntu-latest
    environment: prod
    steps:
      - uses: actions/checkout@v4
      - uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: projects/123456789/locations/global/workloadIdentityPools/gh-pool/providers/gh-provider
          service_account: vertex-prod-deployer@demo-prod.iam.gserviceaccount.com
      - uses: google-github-actions/setup-gcloud@v2
      - run: >
          gcloud ai endpoints deploy-model ENDPOINT_ID --region=asia-south1
          --model=MODEL_ID --display-name=green --machine-type=n1-standard-4
          --min-replica-count=1 --max-replica-count=2
```

**Output (my run):** `python -I` with pyyaml. pyyaml reads `on:` as boolean True, handled in the script. actionlint is not installed here, so this is a small custom lint, not a full GitHub schema check. Nothing was deployed, no OIDC token was issued, no federation was configured. Action versions (`@v2`, `@v4`) are examples; check current docs.
```text
$ python -I q25_lint_workflows.py
azure_ml_deploy.yml | trigger: {'push': {'branches': ['main']}}
   lint: OK
vertex_deploy.yml | trigger: {'push': {'branches': ['main']}}
   lint: OK
bad.yml | 3 findings
   - workflow lacks permissions.id-token: write (OIDC login would fail)
   - long-lived credential pattern: creds: ${{ secrets.AZURE_CREDENTIALS }}
   - job deploy-prod: deploy job without an environment (no approval gate)
```

**Follow-ups:**
- *Subject claim?* Scope the trust to repo plus environment or branch, not the whole organisation.
- *Where do approvals live?* On the prod environment, not in a script.
- *Part 7 difference?* Part 7 owns the pipeline design and the AWS version; here it is only the two clouds.

**Common mistakes:**
- Saving a service principal secret or JSON key in repository secrets.
- Giving the deployer Owner or Contributor on the whole subscription or project.
- Letting pull requests from forks trigger the prod login.

### Q26 ⭐⭐ 🟡 Responsible-AI tooling: Azure ML Responsible AI dashboard (error analysis, interpretability, counterfactuals, causal analysis, fairness) and its pipeline components and scorecard, versus Vertex AI Explainable AI and model evaluation. When does a bank or an insurer in India need these artefacts attached to a model version, and what do they not prove? Show how you would record dashboard output as registry tags or metadata and validate the record schema in Python. Not executed: no dashboard was generated. Book 1 owns fairness and explainability theory.
**Asked at:** Azure ML interview question lists (javainuse 'azure ml' list incl. managed online endpoints and MLOps in Azure ML, a Medium scenario-based Azure ML post by mihirpopat covering registry-then-promote across dev, staging and prod; search snippets only, not opened; WebFetch of learn.microsoft.com failed with getaddrinfo ENOTFOUND); editorial prep sites, not verified candidate reports; ML engineer and MLOps roles at Azure-heavy IT-services firms and GCCs | Microsoft Learn Azure Machine Learning pages as returned by search (MLOps model management and deployment, managed online endpoints, managed network isolation, enterprise security, online-endpoint YAML reference, SDK v1 to v2 migration; search snippets and mirrors on docs.azure.cn and mintlify, none opened; details hedged 'check current docs') | Google Cloud Vertex AI documentation pages as returned by search (MLOps on Vertex AI, feature management and online serving types, deprecations page, VPC Service Controls, Private Service Connect interface for training; search snippets only, not opened; details hedged 'check current docs') | Certification-style question families (Microsoft DP-100 study guide and its replacement AI-300 as reported by third-party sites, Google Cloud Professional Machine Learning Engineer exam-prep listings; mentioned as a source type only, no exam questions reproduced; skills lists conflicted between sources, so verify on the vendor pages)
**Say this first (1 line):** Azure ML's Responsible AI dashboard (error analysis, interpretability, counterfactuals, causal analysis, fairness) and Vertex Explainable AI plus model evaluation produce evidence; I attach a small, validated summary and a link to the model version and I never say it proves the model is fair.

**Then explain:**
- **Azure ML RAI dashboard:** built by a pipeline of components (a constructor and gather components, as the snippets describe) from a registered model and datasets. Pieces include error analysis, feature importance, counterfactual what-ifs, causal analysis. A scorecard is a shareable summary.
- **Vertex AI:** Explainable AI gives feature attributions for predictions (sampled Shapley, integrated gradients, XRAI depending on model type), and model evaluation gives metrics and, for some tasks, slices. Check current docs for which model types are supported.
- **When a bank or insurer needs it:** model risk reviews for credit, claims or pricing, regulator or internal audit asks for the reason of a decision, and customer-impacting decisions. Which Indian rules apply is a legal question, I do not state them here.
- **What it does not prove:** that the data is unbiased, that the metric you picked is the right one, that fairness holds on groups you did not slice, or that it holds next quarter. Attributions explain the model, not the world.
- **Recording it:** keep the dashboard artefact in storage and put flat summary tags on the registry entry (Azure tags are string key-values): link, metric, value, threshold, method, reviewer, date, limitations. Validate before tagging.
- **Failure modes:** dashboard built on a dev dataset, never rebuilt after retraining, protected attribute not available at all, and tags edited by hand.

**Example:** model `credit-risk` v7, demographic parity difference 0.04 against threshold 0.05: gate passes. The validator rejects fairness 1.7 (out of range), method `none`, a 3-character limitations text and a `file://` link. Hand check: 0.04 is at most 0.05, so passes; it says nothing about intersectional groups, which the limitations text must say.

**Code:** pydantic schema with tags, plus a Vertex explanation parameter proto.
```python
# ---- q26_rai_record.py ----
"""Q26: record RAI evidence as flat string tags on an Azure ML Model (offline) and validate the schema with pydantic.
No dashboard was generated; the numbers in the sample are made up for the schema test."""
import warnings; warnings.filterwarnings("ignore")
import importlib.metadata as md, json
from typing import Literal
from pydantic import BaseModel, Field, ValidationError, field_validator
from azure.ai.ml.entities import Model
print("azure-ai-ml", md.version("azure-ai-ml"), "| pydantic", md.version("pydantic"))

class RaiEvidence(BaseModel):
    model_name: str
    model_version: str
    dashboard_uri: str = Field(pattern=r"^(azureml|gs|https)://")   # where the full artefact lives
    protected_attribute: str                                           # e.g. gender (only if legally and ethically usable)
    fairness_metric: Literal["demographic_parity_difference", "equalized_odds_difference"]
    fairness_value: float = Field(ge=0, le=1)
    threshold: float = Field(gt=0, le=1)
    explainability_method: Literal["shap", "mimic", "integrated_gradients", "sampled_shapley", "none"]
    reviewer: str
    reviewed_on: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    limitations: str = Field(min_length=20)                            # what the evidence does NOT prove

    @field_validator("explainability_method")
    @classmethod
    def not_none(cls, v):
        if v == "none": raise ValueError("explainability_method 'none' needs a written exception, not a tag")
        return v
    def to_tags(self) -> dict[str, str]:                               # registry tags are flat strings
        return {f"rai.{k}": str(v) for k, v in self.model_dump().items() if k not in ("model_name", "model_version")}
    @property
    def passed(self): return self.fairness_value <= self.threshold

good = dict(model_name="credit-risk", model_version="7", dashboard_uri="azureml://registries/r/rai/dash1",
            protected_attribute="gender", fairness_metric="demographic_parity_difference", fairness_value=0.04,
            threshold=0.05, explainability_method="shap", reviewer="model-risk@example.com", reviewed_on="2026-10-20",
            limitations="Tested on 2025 applicant data only; no intersectional slices.")
ev = RaiEvidence(**good)
m = Model(name=ev.model_name, version=ev.model_version, path="./model", tags=ev.to_tags())
print("tags on Model entity:", len(m.tags), "e.g.", {k: m.tags[k] for k in list(m.tags)[:3]})
print("gate passed:", ev.passed, "(a pass is a threshold check, not proof of fairness)")
for label, patch in [("fairness out of range", {"fairness_value": 1.7}), ("method none", {"explainability_method": "none"}),
                     ("short limitations", {"limitations": "n/a"}), ("bad uri", {"dashboard_uri": "file:///tmp/x"})]:
    try: RaiEvidence(**{**good, **patch}); print(label, "-> accepted (BUG)")
    except ValidationError as e: print(label, "-> rejected:", e.errors()[0]["loc"][0])

# ---- q26_vertex_explain.py ----
"""Q26 Vertex: ExplanationParameters proto (sampled Shapley) built offline; nothing sent."""
import warnings; warnings.filterwarnings("ignore")
import importlib.metadata as md
from google.cloud.aiplatform_v1.types import ExplanationParameters, SampledShapleyAttribution
print("google-cloud-aiplatform", md.version("google-cloud-aiplatform"))
p = ExplanationParameters(sampled_shapley_attribution=SampledShapleyAttribution(path_count=10), top_k=3)
print(ExplanationParameters.to_json(p, indent=None))
```

**Output (my run):** azure-ai-ml 1.35.2, pydantic 2.14.1 and google-cloud-aiplatform 1.165.1, `python -I`. The Model entity and proto were built in memory. The numbers are made up for the schema test. Not executed: the RAI dashboard pipeline, scorecard, Explainable AI calls and model evaluation; no dashboard was generated. Book 1 owns fairness theory.
```text
$ python -I q26_rai_record.py
azure-ai-ml 1.35.2 | pydantic 2.14.1
tags on Model entity: 9 e.g. {'rai.dashboard_uri': 'azureml://registries/r/rai/dash1', 'rai.protected_attribute': 'gender', 'rai.fairness_metric': 'demographic_parity_difference'}
gate passed: True (a pass is a threshold check, not proof of fairness)
fairness out of range -> rejected: fairness_value
method none -> rejected: explainability_method
short limitations -> rejected: limitations
bad uri -> rejected: dashboard_uri

$ python -I q26_vertex_explain.py
google-cloud-aiplatform 1.165.1
{"sampledShapleyAttribution": {"pathCount": 10}, "topK": 3}
```

**Follow-ups:**
- *Who signs off?* A named reviewer field and date; the gate is a person plus a check.
- *Rebuild when?* On every new model version or data refresh.
- *Is passing a fairness threshold enough?* No: it is one metric on the groups you chose.

**Common mistakes:**
- Treating dashboard output as a certificate.
- Storing evidence in a slide, not next to the model version.
- Running it once and never again after retraining.

### Q27 ⭐⭐ 🟡 BigQuery ML boundary on Vertex AI: when to train inside the warehouse (CREATE MODEL, remote models, importing and exporting models, registering to Vertex Model Registry) versus a Vertex custom job; what the Azure counterpart would be (warehouse or Fabric and Synapse features versus Azure ML) at the boundary only. Give a decision rule and the portability cost of SQL-defined models. Book 3 owns SQL. Write a decision function and test it; no BigQuery call was made.
**Asked at:** GCP Vertex AI interview question list (javainuse 'gcp vertex ai' 2026 list: Vertex Pipelines, Feature Store, Model Registry, model monitoring, MLOps, model versioning; search snippet only, not opened); editorial prep site, not verified candidate reports; ML engineer and MLOps roles at GCP-using product companies and cloud-consulting firms | Cross-cloud comparison articles (TechTarget 'Compare Google Vertex AI vs Amazon SageMaker vs Azure ML', cloudoptimo, gmicloud, superwise, a redresscompliance licensing piece; search snippets only, not opened; several authors sell competing services or advice, so conclusions treated as opinion) | Certification-style question families (Microsoft DP-100 study guide and its replacement AI-300 as reported by third-party sites, Google Cloud Professional Machine Learning Engineer exam-prep listings; mentioned as a source type only, no exam questions reproduced; skills lists conflicted between sources, so verify on the vendor pages)
**Say this first (1 line):** If the data is already in the warehouse, the model family is built in and scoring is batch, train with BigQuery ML; if I need custom code, GPUs, custom features or tight online latency, I use a Vertex custom job, and I count the portability cost of a model defined in SQL.

**Then explain:**
- **BigQuery ML:** `CREATE MODEL` trains inside the warehouse, `ML.PREDICT` scores in SQL, no data movement. There are also remote models that call a Vertex endpoint, import of some external model formats, and export of some models (check current docs which types). A BigQuery ML model can be registered to the Vertex Model Registry so governance sits in one place (check current docs).
- **Vertex custom job:** your code in a container, any framework, GPUs, your features, full control, more to operate.
- **Azure counterpart at the boundary only:** train in the warehouse or lakehouse side (Fabric or Synapse features, check current docs) versus Azure ML for custom training. I do not know the exact feature parity, so I say so in an interview.
- **Portability cost:** a SQL-defined model lives in the warehouse. Moving clouds means retraining from the data in another system, the model file may not export, and the SQL dialect differs. Keep the training SQL in git and the feature logic documented.
- **Failure modes:** a model that cannot be explained or exported when audit asks, SQL features that differ from online serving features, a big table scanned on every retrain (cost depth is Part 12), and scoring in SQL for a 50 ms API.

**Example:** weekly churn scores from a BigQuery table with logistic regression: BigQuery ML. An image model needs GPUs: custom job. A 50 ms fraud score with no export plan: custom job. Same fraud case with a plan to export and host: BigQuery ML is possible. Data in Blob storage, not in BigQuery: custom job by default. Hand check: five cases, expected `bqml`, `vertex_custom_job`, `vertex_custom_job`, `bqml`, `vertex_custom_job`, asserted in the script.

**Code:** the decision function with tests. The SQL syntax is shown in prose only, no SQL ran.
```python
# ---- q27_bqml_decision.py ----
"""Q27: decision rule BigQuery ML vs Vertex custom job. Pure Python; no BigQuery call was made."""
def decide(p: dict) -> tuple[str, list[str]]:
    why = []
    # hard blockers for in-warehouse training first
    if p["needs_custom_framework_or_gpu"]: return "vertex_custom_job", ["needs custom code, framework or GPU beyond built-in model types"]
    if p["needs_custom_features_in_python"]: return "vertex_custom_job", ["feature logic does not fit SQL"]
    if p["strict_realtime_latency_ms"] is not None and not p["will_export_model"]:
        return "vertex_custom_job", ["tight online latency: score outside the warehouse (or export and host)"]
    if p["data_in_warehouse"] and p["model_family_supported_in_bqml"]:
        why.append("data already in the warehouse, model family is built in")
        if p["batch_scoring_only"]: why.append("batch scoring in SQL is enough")
        if p["must_register_in_vertex"]: why.append("register to Vertex Model Registry so governance is shared (check current docs)")
        return "bqml", why
    return "vertex_custom_job", ["default: data not in warehouse or model family unsupported"]

base = dict(needs_custom_framework_or_gpu=False, needs_custom_features_in_python=False, strict_realtime_latency_ms=None,
            will_export_model=False, data_in_warehouse=True, model_family_supported_in_bqml=True, batch_scoring_only=True,
            must_register_in_vertex=False)
cases = {
 "weekly churn scores, data in BQ, logistic regression": base,
 "image model on GPUs": {**base, "needs_custom_framework_or_gpu": True},
 "fraud score at 50 ms online, no export plan": {**base, "strict_realtime_latency_ms": 50, "batch_scoring_only": False},
 "same fraud case but plan to export model": {**base, "strict_realtime_latency_ms": 50, "will_export_model": True, "batch_scoring_only": False, "must_register_in_vertex": True},
 "data lives in Blob storage, not BQ": {**base, "data_in_warehouse": False},
}
expected = ["bqml", "vertex_custom_job", "vertex_custom_job", "bqml", "vertex_custom_job"]
for (name, p), exp in zip(cases.items(), expected):
    got, why = decide(p); assert got == exp, (name, got)
    print(f"{got:17s} <- {name}: {'; '.join(why)}")
print("5 cases, all as expected")
```

**Output (my run):** Python 3.13 `python -I`, pure Python. No BigQuery call was made, no `CREATE MODEL` was run and no model was registered; the rule is my judgement, not a vendor rule. Book 3 owns SQL.
```text
$ python -I q27_bqml_decision.py
bqml              <- weekly churn scores, data in BQ, logistic regression: data already in the warehouse, model family is built in; batch scoring in SQL is enough
vertex_custom_job <- image model on GPUs: needs custom code, framework or GPU beyond built-in model types
vertex_custom_job <- fraud score at 50 ms online, no export plan: tight online latency: score outside the warehouse (or export and host)
bqml              <- same fraud case but plan to export model: data already in the warehouse, model family is built in; register to Vertex Model Registry so governance is shared (check current docs)
vertex_custom_job <- data lives in Blob storage, not BQ: default: data not in warehouse or model family unsupported
5 cases, all as expected
```

**Follow-ups:**
- *Why not always BigQuery ML?* Limited model families and control, and SQL models are harder to move.
- *Why not always a custom job?* More engineering and data movement for simple models.
- *How do you serve a BigQuery ML model online?* Export or register and deploy where supported, or call remote models; check current docs.

**Common mistakes:**
- Choosing by habit (always SQL, always Python).
- Ignoring that online features must match the SQL training features.
- Forgetting an exit path for a model that exists only in the warehouse.
