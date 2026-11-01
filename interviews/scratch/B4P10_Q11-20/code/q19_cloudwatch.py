import os, time
for k, v in {"AWS_ACCESS_KEY_ID": "testing", "AWS_SECRET_ACCESS_KEY": "testing", "AWS_DEFAULT_REGION": "us-east-1"}.items():
    os.environ[k] = v
import boto3
from moto import mock_aws

with mock_aws():
    cw = boto3.client("cloudwatch")
    cw.put_metric_data(Namespace="MLApp", MetricData=[{"MetricName": "FraudScoreLatencyMs", "Value": 42.0, "Unit": "Milliseconds",
                                                       "Dimensions": [{"Name": "Endpoint", "Value": "fraud-v3"}]}])
    cw.put_metric_alarm(AlarmName="fraud-latency-high", Namespace="MLApp", MetricName="FraudScoreLatencyMs",
                        Dimensions=[{"Name": "Endpoint", "Value": "fraud-v3"}], Statistic="Average", Period=60,
                        EvaluationPeriods=3, DatapointsToAlarm=2, Threshold=100.0, ComparisonOperator="GreaterThanThreshold",
                        TreatMissingData="notBreaching")
    a = cw.describe_alarms(AlarmNames=["fraud-latency-high"])["MetricAlarms"][0]
    print({k: a[k] for k in ("AlarmName", "StateValue", "Period", "EvaluationPeriods", "DatapointsToAlarm", "Threshold", "ComparisonOperator")})
    print("metrics listed:", [(m["Namespace"], m["MetricName"]) for m in cw.list_metrics(Namespace="MLApp")["Metrics"]])

    logs = boto3.client("logs")
    logs.create_log_group(logGroupName="/ml/train")
    logs.create_log_stream(logGroupName="/ml/train", logStreamName="job-1")
    now = int(time.time() * 1000)
    logs.put_log_events(logGroupName="/ml/train", logStreamName="job-1", logEvents=[
        {"timestamp": now, "message": "epoch=1 loss=0.9"},
        {"timestamp": now + 1, "message": "ERROR AccessDenied reading s3://ml-data/train/"},
        {"timestamp": now + 2, "message": "epoch=2 loss=0.7"}])
    ev = logs.filter_log_events(logGroupName="/ml/train", filterPattern="ERROR")["events"]
    print("filter 'ERROR' ->", [e["message"] for e in ev])

    ct = boto3.client("cloudtrail")
    try:
        ct.lookup_events(LookupAttributes=[{"AttributeKey": "EventName", "AttributeValue": "DeleteBucket"}])
        print("cloudtrail lookup_events worked")
    except Exception as e:
        print("cloudtrail lookup_events:", type(e).__name__, str(e)[:90])
    cfg = boto3.client("config")
    try:
        cfg.describe_configuration_recorders()
        print("config describe_configuration_recorders: call accepted")
    except Exception as e:
        print("config:", type(e).__name__, str(e)[:90])
