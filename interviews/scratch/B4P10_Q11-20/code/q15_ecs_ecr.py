import os, json
for k, v in {"AWS_ACCESS_KEY_ID": "testing", "AWS_SECRET_ACCESS_KEY": "testing", "AWS_DEFAULT_REGION": "us-east-1"}.items():
    os.environ[k] = v
import boto3
from moto import mock_aws
with mock_aws():
    ecr = boto3.client("ecr")
    repo = ecr.create_repository(repositoryName="fraud-scorer", imageTagMutability="IMMUTABLE",
                                 imageScanningConfiguration={"scanOnPush": True})["repository"]
    print({k: repo[k] for k in ("repositoryName", "repositoryUri", "imageTagMutability")}, repo["imageScanningConfiguration"])
    ecs = boto3.client("ecs")
    ecs.create_cluster(clusterName="ml")
    td = ecs.register_task_definition(
        family="fraud-scorer", requiresCompatibilities=["FARGATE"], networkMode="awsvpc", cpu="1024", memory="2048",
        executionRoleArn="arn:aws:iam::123456789012:role/ecsTaskExecutionRole",
        taskRoleArn="arn:aws:iam::123456789012:role/fraud-scorer-task",
        containerDefinitions=[{"name": "app", "image": repo["repositoryUri"] + ":1.4.0", "essential": True,
                               "portMappings": [{"containerPort": 8080}],
                               "environment": [{"name": "MODEL_URI", "value": "s3://ml-data/models/m1/"}]}])["taskDefinition"]
    print({k: td[k] for k in ("family", "revision", "status", "requiresCompatibilities", "networkMode", "cpu", "memory")})
    print("container image:", td["containerDefinitions"][0]["image"])
    print("clusters:", ecs.list_clusters()["clusterArns"])
    print("Not run: no service, no task, no container, no image pushed (API shape only).")
