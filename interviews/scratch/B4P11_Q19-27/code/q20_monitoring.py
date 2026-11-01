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
