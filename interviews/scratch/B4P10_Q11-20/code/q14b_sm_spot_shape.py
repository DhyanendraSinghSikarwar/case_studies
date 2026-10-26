import os
for k, v in {"AWS_ACCESS_KEY_ID": "testing", "AWS_SECRET_ACCESS_KEY": "testing", "AWS_DEFAULT_REGION": "us-east-1"}.items():
    os.environ[k] = v
import boto3
from moto import mock_aws
with mock_aws():
    iam = boto3.client("iam")
    role = iam.create_role(RoleName="sm", AssumeRolePolicyDocument="{}")["Role"]["Arn"]
    sm = boto3.client("sagemaker")
    req = dict(
        TrainingJobName="spot-demo", RoleArn=role,
        AlgorithmSpecification={"TrainingImage": "123456789012.dkr.ecr.us-east-1.amazonaws.com/trainer:1", "TrainingInputMode": "File"},
        ResourceConfig={"InstanceType": "ml.g5.xlarge", "InstanceCount": 1, "VolumeSizeInGB": 50},
        OutputDataConfig={"S3OutputPath": "s3://ml-data/models/"},
        StoppingCondition={"MaxRuntimeInSeconds": 3600, "MaxWaitTimeInSeconds": 7200},
        EnableManagedSpotTraining=True,
        CheckpointConfig={"S3Uri": "s3://ml-data/ckpt/spot-demo/", "LocalPath": "/opt/ml/checkpoints"})
    sm.create_training_job(**req)
    d = sm.describe_training_job(TrainingJobName="spot-demo")
    print({k: d[k] for k in ("TrainingJobStatus", "EnableManagedSpotTraining")}, d["CheckpointConfig"], d["StoppingCondition"])
    print("moto marks job finished instantly; no spot interruption, no checkpoint was ever written")
