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
