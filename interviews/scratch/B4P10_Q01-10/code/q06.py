import os
os.environ.update(AWS_ACCESS_KEY_ID="testing", AWS_SECRET_ACCESS_KEY="testing", AWS_DEFAULT_REGION="us-east-1")
import json, boto3
from moto import mock_aws

with mock_aws():
    iam = boto3.client("iam")
    role = iam.create_role(RoleName="sm-exec", AssumeRolePolicyDocument=json.dumps({"Version": "2012-10-17", "Statement": [
        {"Effect": "Allow", "Principal": {"Service": "sagemaker.amazonaws.com"}, "Action": "sts:AssumeRole"}]}))["Role"]["Arn"]
    sm = boto3.client("sagemaker")
    sm.create_model(ModelName="m1", ExecutionRoleArn=role,
        PrimaryContainer={"Image": "123456789012.dkr.ecr.us-east-1.amazonaws.com/serve:1", "ModelDataUrl": "s3://ml-data/models/m1/model.tar.gz"})
    configs = {
     "upi-realtime": dict(ProductionVariants=[{"VariantName": "AllTraffic", "ModelName": "m1",
          "InstanceType": "ml.c5.xlarge", "InitialInstanceCount": 2}]),
     "docs-async": dict(ProductionVariants=[{"VariantName": "AllTraffic", "ModelName": "m1",
          "InstanceType": "ml.m5.xlarge", "InitialInstanceCount": 1}],
          AsyncInferenceConfig={"OutputConfig": {"S3OutputPath": "s3://ml-data/async-out/"}}),
     "internal-serverless": dict(ProductionVariants=[{"VariantName": "AllTraffic", "ModelName": "m1",
          "ServerlessConfig": {"MemorySizeInMB": 2048, "MaxConcurrency": 5}}]),
    }
    for name, kw in configs.items():
        sm.create_endpoint_config(EndpointConfigName=name, **kw)
        d = sm.describe_endpoint_config(EndpointConfigName=name)
        v = d["ProductionVariants"][0]
        kind = "async" if "AsyncInferenceConfig" in d else ("serverless" if "ServerlessConfig" in v else "real-time")
        print(f"{name:20s} -> {kind:10s} variant keys: {sorted(k for k in v if k in ('InstanceType','InitialInstanceCount','ServerlessConfig'))}")
    # batch transform is a JOB, not an endpoint
    sm.create_transform_job(TransformJobName="nightly-score-001", ModelName="m1",
        TransformInput={"DataSource": {"S3DataSource": {"S3DataType": "S3Prefix", "S3Uri": "s3://ml-data/score/2026-10-25/"}}, "ContentType": "text/csv"},
        TransformOutput={"S3OutputPath": "s3://ml-data/score-out/"},
        TransformResources={"InstanceType": "ml.m5.xlarge", "InstanceCount": 2})
    t = sm.describe_transform_job(TransformJobName="nightly-score-001")
    print("batch transform job:", t["TransformJobName"], t["TransformJobStatus"], "(job, no endpoint)")
    sm.create_endpoint(EndpointName="upi-ep", EndpointConfigName="upi-realtime")
    print("endpoint status:", sm.describe_endpoint(EndpointName="upi-ep")["EndpointStatus"])
    rt = boto3.client("sagemaker-runtime")
    print("invoke_endpoint:", rt.invoke_endpoint(EndpointName="upi-ep", Body=b"1,2,3", ContentType="text/csv")["Body"].read(), "<- canned, no model ran")
