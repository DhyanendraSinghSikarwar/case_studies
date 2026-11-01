import os
os.environ.update(AWS_ACCESS_KEY_ID="testing", AWS_SECRET_ACCESS_KEY="testing", AWS_DEFAULT_REGION="us-east-1")
import json, boto3
from moto import mock_aws

with mock_aws():
    iam = boto3.client("iam")
    role = iam.create_role(RoleName="sm-exec", AssumeRolePolicyDocument=json.dumps({"Version": "2012-10-17", "Statement": [
        {"Effect": "Allow", "Principal": {"Service": "sagemaker.amazonaws.com"}, "Action": "sts:AssumeRole"}]}))["Role"]["Arn"]
    sm = boto3.client("sagemaker")
    req = dict(
        TrainingJobName="churn-xgb-001",
        RoleArn=role,
        AlgorithmSpecification={"TrainingImage": "123456789012.dkr.ecr.us-east-1.amazonaws.com/train-img:1.0",
                                "TrainingInputMode": "File"},
        InputDataConfig=[{"ChannelName": "train",
            "DataSource": {"S3DataSource": {"S3DataType": "S3Prefix", "S3Uri": "s3://ml-data/train/", "S3DataDistributionType": "FullyReplicated"}}},
            {"ChannelName": "validation",
            "DataSource": {"S3DataSource": {"S3DataType": "S3Prefix", "S3Uri": "s3://ml-data/val/"}}}],
        OutputDataConfig={"S3OutputPath": "s3://ml-data/models/"},
        ResourceConfig={"InstanceType": "ml.m5.xlarge", "InstanceCount": 1, "VolumeSizeInGB": 30},
        StoppingCondition={"MaxRuntimeInSeconds": 3600},
        HyperParameters={"max_depth": "6", "eta": "0.1"},   # all values are strings
    )
    print("request keys:", list(req))
    r = sm.create_training_job(**req)
    print("response keys:", [k for k in r if k != "ResponseMetadata"])
    print("TrainingJobArn:", r["TrainingJobArn"])
    d = sm.describe_training_job(TrainingJobName="churn-xgb-001")
    print("status:", d["TrainingJobStatus"], "| secondary:", d.get("SecondaryStatus"))
    print("hyperparameters:", d["HyperParameters"])
    print("channels:", [c["ChannelName"] for c in d["InputDataConfig"]])
    print("ModelArtifacts:", d.get("ModelArtifacts"))
    print("NOTE: no container ran, nothing was written to S3, no logs exist.")
