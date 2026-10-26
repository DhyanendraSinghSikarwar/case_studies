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
