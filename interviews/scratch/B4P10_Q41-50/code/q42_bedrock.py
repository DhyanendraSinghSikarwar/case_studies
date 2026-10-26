"""Q42: Bedrock boundary. moto mock, fake keys. API shape only."""
import os, sys, json
os.environ.update(AWS_ACCESS_KEY_ID="testing", AWS_SECRET_ACCESS_KEY="testing", AWS_DEFAULT_REGION="us-east-1")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import boto3
from moto import mock_aws
from iam_eval_ext import evaluate

MODEL = "anthropic.claude-3-haiku-20240307-v1:0"     # example model id string only; check current docs for model ids
policy = {"Version": "2012-10-17", "Statement": [
  {"Effect": "Allow", "Action": ["bedrock:InvokeModel"],
   "Resource": [f"arn:aws:bedrock:us-east-1::foundation-model/{MODEL}"],
   "Condition": {"StringEquals": {"aws:RequestedRegion": "us-east-1"}}}]}

print("== IAM: allow one model in one Region ==")
for name, res, ctx in [
  ("approved model, us-east-1", f"arn:aws:bedrock:us-east-1::foundation-model/{MODEL}", {"aws:RequestedRegion": "us-east-1"}),
  ("other model", "arn:aws:bedrock:us-east-1::foundation-model/other.model-v1:0", {"aws:RequestedRegion": "us-east-1"}),
  ("approved model, other Region", f"arn:aws:bedrock:eu-west-1::foundation-model/{MODEL}", {"aws:RequestedRegion": "eu-west-1"}),
]:
    print(f"{name:32s}", evaluate("bedrock:InvokeModel", res, ctx=ctx, identity=[policy]))

with mock_aws():
    print("\n== bedrock-runtime invoke_model (mock) ==")
    br = boto3.client("bedrock-runtime")
    body = json.dumps({"anthropic_version": "bedrock-2023-05-31", "max_tokens": 50,
                       "messages": [{"role": "user", "content": "hello"}]})
    r = br.invoke_model(modelId=MODEL, body=body, contentType="application/json", accept="application/json")
    print("HTTP", r["ResponseMetadata"]["HTTPStatusCode"], "| contentType", r["contentType"])
    print("body:", r["body"].read().decode()[:200])

    print("\n== private call path: interface VPC endpoint (record only) ==")
    ec2 = boto3.client("ec2")
    vpc = ec2.create_vpc(CidrBlock="10.0.0.0/16")["Vpc"]["VpcId"]
    sn = ec2.create_subnet(VpcId=vpc, CidrBlock="10.0.1.0/24")["Subnet"]["SubnetId"]
    ep = ec2.create_vpc_endpoint(VpcId=vpc, ServiceName="com.amazonaws.us-east-1.bedrock-runtime",
                                 VpcEndpointType="Interface", SubnetIds=[sn], PrivateDnsEnabled=True)["VpcEndpoint"]
    print("endpoint service:", ep["ServiceName"], "| type:", ep["VpcEndpointType"], "| private DNS:", ep["PrivateDnsEnabled"])

    print("\n== invocation logging and guardrails in moto (what exists?) ==")
    b = boto3.client("bedrock")
    for label, fn in [
      ("put_model_invocation_logging_configuration", lambda: b.put_model_invocation_logging_configuration(
          loggingConfig={"cloudWatchConfig": {"logGroupName": "/bedrock/invocations", "roleArn": "arn:aws:iam::123456789012:role/br-log"},
                         "textDataDeliveryEnabled": True})),
      ("get_model_invocation_logging_configuration", lambda: b.get_model_invocation_logging_configuration()),
      ("create_guardrail", lambda: b.create_guardrail(name="g1", blockedInputMessaging="no", blockedOutputsMessaging="no",
          topicPolicyConfig={"topicsConfig": [{"name": "advice", "definition": "financial advice", "type": "DENY"}]})),
      ("list_foundation_models", lambda: b.list_foundation_models()),
    ]:
        try:
            out = fn(); out.pop("ResponseMetadata", None)
            print(f"{label}: ok -> {str(out)[:150]}")
        except Exception as e:
            print(f"{label}: {type(e).__name__}: {str(e)[:100]}")
