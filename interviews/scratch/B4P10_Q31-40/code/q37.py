# Q37: CloudWatch alarm in moto + pure-Python 'M of N datapoints breaching' evaluator.
import os
os.environ.update(AWS_ACCESS_KEY_ID="testing", AWS_SECRET_ACCESS_KEY="testing", AWS_DEFAULT_REGION="us-east-1")
import boto3
from moto import mock_aws

@mock_aws
def moto_part():
    cw = boto3.client("cloudwatch")
    cw.put_metric_alarm(AlarmName="ep-model-latency-high", Namespace="AWS/SageMaker", MetricName="ModelLatency",
        Dimensions=[{"Name": "EndpointName", "Value": "risk-ep"}, {"Name": "VariantName", "Value": "AllTraffic"}],
        ExtendedStatistic="p99", Period=60, EvaluationPeriods=5, DatapointsToAlarm=3, Threshold=100000,
        ComparisonOperator="GreaterThanThreshold", TreatMissingData="notBreaching")
    a = cw.describe_alarms(AlarmNames=["ep-model-latency-high"])["MetricAlarms"][0]
    print({k: a[k] for k in ("AlarmName", "MetricName", "Period", "EvaluationPeriods", "DatapointsToAlarm", "ComparisonOperator", "TreatMissingData", "StateValue")})
    print("(ModelLatency is reported in microseconds by SageMaker per current docs; threshold above is a placeholder, not advice)")
moto_part()

def evaluate(points, threshold, m, n, op="gt", treat_missing="notBreaching"):
    """Last n datapoints (None = missing). ALARM if >= m breach; INSUFFICIENT_DATA if missing treated as 'missing' and not enough data."""
    window = points[-n:]
    def breach(v):
        if v is None: return {"breaching": True, "notBreaching": False, "ignore": None, "missing": None}[treat_missing]
        return v > threshold if op == "gt" else v < threshold
    flags = [breach(v) for v in window]
    if treat_missing in ("ignore", "missing"): flags = [f for f in flags if f is not None]
    if treat_missing == "missing" and len(flags) == 0: return "INSUFFICIENT_DATA", flags
    return ("ALARM" if sum(1 for f in flags if f) >= m else "OK"), flags
cases = [
  ("3 of 5, exactly 3 breach",     [10, 120, 130, 20, 140], dict(m=3, n=5)),
  ("3 of 5, only 2 breach",        [10, 120, 130, 20, 30],  dict(m=3, n=5)),
  ("1 of 1 single spike",          [10, 10, 10, 10, 500],   dict(m=1, n=1)),
  ("missing, notBreaching",        [None, None, 130, 140, None], dict(m=3, n=5)),
  ("missing, breaching",           [None, None, 130, 140, None], dict(m=3, n=5, treat_missing="breaching")),
  ("all missing, 'missing' mode",  [None] * 5,              dict(m=3, n=5, treat_missing="missing")),
]
for name, pts, kw in cases:
    state, flags = evaluate(pts, 100, **kw)
    print(f"{name:32s} {state:18s} flags={flags}")
