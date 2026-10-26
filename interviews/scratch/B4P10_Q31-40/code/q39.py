# Q39: required-endpoints checklist as data, run against a moto VPC with and without endpoints.
import os
os.environ.update(AWS_ACCESS_KEY_ID="testing", AWS_SECRET_ACCESS_KEY="testing", AWS_DEFAULT_REGION="us-east-1")
import boto3
from moto import mock_aws
REGION = "us-east-1"
# kind: Gateway endpoints go into route tables; Interface endpoints live as ENIs in subnets. List varies by job features: check current docs.
CHECKLIST = [
  {"service": "s3",         "kind": "Gateway",   "why": "training data in, model artifacts out, image layers are served from S3"},
  {"service": "ecr.api",    "kind": "Interface", "why": "ECR API calls (auth token, image manifest lookup)"},
  {"service": "ecr.dkr",    "kind": "Interface", "why": "docker registry protocol to pull the image"},
  {"service": "logs",       "kind": "Interface", "why": "job writes CloudWatch Logs"},
  {"service": "sts",        "kind": "Interface", "why": "role credentials / assume-role calls from inside the job"},
  {"service": "sagemaker.api", "kind": "Interface", "why": "only if code in the job calls the SageMaker API"},
]
def audit(ec2, vpc_id, subnet_route_tables):
    eps = ec2.describe_vpc_endpoints(Filters=[{"Name": "vpc-id", "Values": [vpc_id]}])["VpcEndpoints"]
    have = {e["ServiceName"].removeprefix(f"com.amazonaws.{REGION}."): e for e in eps}
    missing = []
    for item in CHECKLIST:
        e = have.get(item["service"])
        if e is None: missing.append((item["service"], "no endpoint")); continue
        if e["VpcEndpointType"] != item["kind"]: missing.append((item["service"], f"wrong type {e['VpcEndpointType']}"))
        elif item["kind"] == "Gateway" and not set(subnet_route_tables) <= set(e.get("RouteTableIds", [])):
            missing.append((item["service"], "not attached to the subnet's route table"))
    return missing

@mock_aws
def main():
    ec2 = boto3.client("ec2", region_name=REGION)
    vpc = ec2.create_vpc(CidrBlock="10.0.0.0/16")["Vpc"]["VpcId"]
    sn = ec2.create_subnet(VpcId=vpc, CidrBlock="10.0.1.0/24")["Subnet"]["SubnetId"]
    rt = ec2.create_route_table(VpcId=vpc)["RouteTable"]["RouteTableId"]
    ec2.associate_route_table(RouteTableId=rt, SubnetId=sn)
    sg = ec2.create_security_group(GroupName="sm-job", Description="job", VpcId=vpc)["GroupId"]
    print("A) empty VPC, missing:", audit(ec2, vpc, [rt]))
    ec2.create_vpc_endpoint(VpcId=vpc, ServiceName=f"com.amazonaws.{REGION}.s3", VpcEndpointType="Gateway")  # forgot route table
    for svc in ("ecr.api", "ecr.dkr"):
        ec2.create_vpc_endpoint(VpcId=vpc, ServiceName=f"com.amazonaws.{REGION}.{svc}", VpcEndpointType="Interface", SubnetIds=[sn], SecurityGroupIds=[sg])
    print("B) s3 (no route table) + ecr only, missing:", audit(ec2, vpc, [rt]))
    ep = ec2.describe_vpc_endpoints(Filters=[{"Name": "service-name", "Values": [f"com.amazonaws.{REGION}.s3"]}])["VpcEndpoints"][0]["VpcEndpointId"]
    ec2.modify_vpc_endpoint(VpcEndpointId=ep, AddRouteTableIds=[rt])
    for svc in ("logs", "sts", "sagemaker.api"):
        ec2.create_vpc_endpoint(VpcId=vpc, ServiceName=f"com.amazonaws.{REGION}.{svc}", VpcEndpointType="Interface", SubnetIds=[sn], SecurityGroupIds=[sg])
    print("C) all endpoints + route table, missing:", audit(ec2, vpc, [rt]))
main()
print("Not executed: DNS resolution to endpoint ENIs, routing, the actual hang/timeout a missing endpoint causes.")
