# Q33: Model Monitor / Ground Truth at the service boundary. moto API shape only.
import os, json
os.environ.update(AWS_ACCESS_KEY_ID="testing", AWS_SECRET_ACCESS_KEY="testing", AWS_DEFAULT_REGION="us-east-1")
import boto3
from moto import mock_aws

REQUIRED = {"EnableCapture": bool, "InitialSamplingPercentage": int, "DestinationS3Uri": str, "CaptureOptions": list}
def validate_capture(cfg):
    errs = [f"missing {k}" for k in REQUIRED if k not in cfg]
    errs += [f"{k} should be {t.__name__}" for k, t in REQUIRED.items() if k in cfg and not isinstance(cfg[k], t)]
    if isinstance(cfg.get("InitialSamplingPercentage"), int) and not 0 <= cfg["InitialSamplingPercentage"] <= 100:
        errs.append("InitialSamplingPercentage must be 0..100")
    if isinstance(cfg.get("DestinationS3Uri"), str) and not cfg["DestinationS3Uri"].startswith("s3://"):
        errs.append("DestinationS3Uri must start with s3://")
    modes = {o.get("CaptureMode") for o in cfg.get("CaptureOptions", []) if isinstance(o, dict)}
    if not modes <= {"Input", "Output"} or not modes: errs.append("CaptureOptions needs CaptureMode Input and/or Output")
    return errs

good = {"EnableCapture": True, "InitialSamplingPercentage": 20, "DestinationS3Uri": "s3://ml-monitor/capture/",
        "CaptureOptions": [{"CaptureMode": "Input"}, {"CaptureMode": "Output"}]}
bad = {"EnableCapture": True, "InitialSamplingPercentage": 150, "DestinationS3Uri": "ml-monitor/capture", "CaptureOptions": [{"CaptureMode": "Both"}]}
print("good ->", validate_capture(good)); print("bad  ->", validate_capture(bad))
print("missing keys ->", validate_capture({"EnableCapture": True}))

@mock_aws
def moto():
    sm = boto3.client("sagemaker")
    sm.create_model(ModelName="m", ExecutionRoleArn="arn:aws:iam::123456789012:role/sm",
                    PrimaryContainer={"Image": "123456789012.dkr.ecr.us-east-1.amazonaws.com/img:1"})
    try:
        r = sm.create_endpoint_config(EndpointConfigName="ec", ProductionVariants=[{"VariantName": "v", "ModelName": "m",
            "InitialInstanceCount": 1, "InstanceType": "ml.m5.large"}], DataCaptureConfig=good)
        print("create_endpoint_config with DataCaptureConfig: accepted ->", r["EndpointConfigArn"].split("/")[-1])
        d = sm.describe_endpoint_config(EndpointConfigName="ec")
        print("read back DataCaptureConfig:", "DataCaptureConfig" in d, d.get("DataCaptureConfig", {}).get("DestinationS3Uri"))
    except Exception as e: print("create_endpoint_config:", type(e).__name__, str(e)[:120])
    for name, call in [("create_monitoring_schedule", lambda: sm.create_monitoring_schedule(MonitoringScheduleName="s",
            MonitoringScheduleConfig={"ScheduleConfig": {"ScheduleExpression": "cron(0 * ? * * *)"}})),
        ("list_labeling_jobs", lambda: sm.list_labeling_jobs()),
        ("create_data_quality_job_definition", lambda: sm.create_data_quality_job_definition(JobDefinitionName="d"))]:
        try: call(); print(name, ": returned (unexpected)")
        except Exception as e: print(name, ":", type(e).__name__, "-", str(e)[:90].replace("\n", " "))
moto()
