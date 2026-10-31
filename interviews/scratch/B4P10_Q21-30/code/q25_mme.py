import os
os.environ.update(AWS_ACCESS_KEY_ID="testing",AWS_SECRET_ACCESS_KEY="testing",AWS_DEFAULT_REGION="us-east-1")
import boto3
from moto import mock_aws

with mock_aws():
    sm = boto3.client("sagemaker")
    img = "123456789012.dkr.ecr.us-east-1.amazonaws.com/xgb-infer:1"
    role = "arn:aws:iam::123456789012:role/sm"
    sm.create_model(ModelName="tenants-mme", ExecutionRoleArn=role,
        PrimaryContainer={"Image": img, "Mode": "MultiModel", "ModelDataUrl": "s3://ml-models/tenants/"})
    d = sm.describe_model(ModelName="tenants-mme")
    print("MME container:", d["PrimaryContainer"]["Mode"], d["PrimaryContainer"]["ModelDataUrl"])
    sm.create_model(ModelName="pipe", ExecutionRoleArn=role, InferenceExecutionConfig={"Mode": "Serial"},
        Containers=[{"Image": img, "ContainerHostname": "pre"}, {"Image": img, "ContainerHostname": "model"}])
    d = sm.describe_model(ModelName="pipe")
    print("multi-container: containers =", [c["ContainerHostname"] for c in d["Containers"]], "| InferenceExecutionConfig echoed:", d.get("InferenceExecutionConfig"))
    sm.create_endpoint_config(EndpointConfigName="mme-cfg", ProductionVariants=[{"VariantName": "v", "ModelName": "tenants-mme", "InstanceType": "ml.m5.large", "InitialInstanceCount": 1}])
    sm.create_endpoint(EndpointName="mme-ep", EndpointConfigName="mme-cfg")
    print("endpoint:", sm.describe_endpoint(EndpointName="mme-ep")["EndpointStatus"])
    rt = boto3.client("sagemaker-runtime")
    r = rt.invoke_endpoint(EndpointName="mme-ep", TargetModel="tenant-17.tar.gz", Body=b"1,2,3", ContentType="text/csv")
    print("invoke with TargetModel returned:", r["Body"].read(), "-> canned; nothing loaded from S3, no cold load, no eviction")
