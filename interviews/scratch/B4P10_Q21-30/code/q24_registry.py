import os
os.environ.update(AWS_ACCESS_KEY_ID="testing",AWS_SECRET_ACCESS_KEY="testing",AWS_DEFAULT_REGION="us-east-1")
import boto3
from moto import mock_aws

with mock_aws():
    sm = boto3.client("sagemaker")
    sm.create_model_package_group(ModelPackageGroupName="churn-model", ModelPackageGroupDescription="demo")
    arn = sm.create_model_package(ModelPackageGroupName="churn-model", ModelPackageDescription="v1", ModelApprovalStatus="PendingManualApproval",
        InferenceSpecification={"Containers": [{"Image": "123456789012.dkr.ecr.us-east-1.amazonaws.com/infer:1", "ModelDataUrl": "s3://ml-artifacts/churn/model.tar.gz"}],
            "SupportedContentTypes": ["text/csv"], "SupportedResponseMIMETypes": ["text/csv"]},
        CustomerMetadataProperties={"git_sha": "abc123", "auc": "0.91"})["ModelPackageArn"]
    print("arn tail:", arn.split(":", 5)[-1])
    d = sm.describe_model_package(ModelPackageName=arn)
    print("status before:", d["ModelApprovalStatus"], "| version:", d.get("ModelPackageVersion"))
    sm.update_model_package(ModelPackageArn=arn, ModelApprovalStatus="Approved", ApprovalDescription="reviewed by ds-lead")
    d = sm.describe_model_package(ModelPackageName=arn)
    print("status after:", d["ModelApprovalStatus"], "| metadata:", d.get("CustomerMetadataProperties"))
    print("containers:", [c["ModelDataUrl"] for c in d["InferenceSpecification"]["Containers"]])
    pk = sm.list_model_packages(ModelPackageGroupName="churn-model", ModelApprovalStatus="Approved")["ModelPackageSummaryList"]
    print("approved in group:", len(pk))
    # EventBridge rule shape for the approval event (rule is just stored; nothing fires)
    import json
    ev = boto3.client("events")
    ev.put_rule(Name="on-approved", EventPattern=json.dumps({"source": ["aws.sagemaker"], "detail-type": ["SageMaker Model Package State Change"], "detail": {"ModelApprovalStatus": ["Approved"]}}))
    print("rule stored:", ev.describe_rule(Name="on-approved")["Name"], "(no event is ever delivered in moto)")
