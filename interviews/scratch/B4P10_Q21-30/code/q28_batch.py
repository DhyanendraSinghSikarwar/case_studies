import os
os.environ.update(AWS_ACCESS_KEY_ID="testing",AWS_SECRET_ACCESS_KEY="testing",AWS_DEFAULT_REGION="us-east-1")
import boto3
from moto import mock_aws

with mock_aws():
    ec2 = boto3.client("ec2"); iam = boto3.client("iam"); b = boto3.client("batch")
    vpc = ec2.create_vpc(CidrBlock="10.0.0.0/16")["Vpc"]["VpcId"]
    sn = ec2.create_subnet(VpcId=vpc, CidrBlock="10.0.1.0/24")["Subnet"]["SubnetId"]
    sg = ec2.create_security_group(GroupName="batch-sg", Description="d", VpcId=vpc)["GroupId"]
    role = iam.create_role(RoleName="batch-svc", AssumeRolePolicyDocument="{}")["Role"]["Arn"]
    prof = iam.create_instance_profile(InstanceProfileName="ecsInst")["InstanceProfile"]["Arn"]
    def step(name, fn):
        try: r = fn(); print(f"{name}: OK"); return r
        except Exception as e: print(f"{name}: FAILED {type(e).__name__}: {str(e)[:110]}")
    step("compute env (EC2)", lambda: b.create_compute_environment(computeEnvironmentName="ml-ce", type="MANAGED", state="ENABLED", serviceRole=role,
        computeResources={"type": "EC2", "minvCpus": 0, "maxvCpus": 16, "desiredvCpus": 0, "instanceTypes": ["m5.large"], "subnets": [sn], "securityGroupIds": [sg], "instanceRole": prof}))
    step("compute env (SPOT)", lambda: b.create_compute_environment(computeEnvironmentName="ml-spot", type="MANAGED", state="ENABLED", serviceRole=role,
        computeResources={"type": "SPOT", "allocationStrategy": "SPOT_CAPACITY_OPTIMIZED", "minvCpus": 0, "maxvCpus": 16, "instanceTypes": ["m5.large"], "subnets": [sn], "securityGroupIds": [sg], "instanceRole": prof, "spotIamFleetRole": role}))
    step("job queue", lambda: b.create_job_queue(jobQueueName="ml-queue", priority=10, state="ENABLED", computeEnvironmentOrder=[{"order": 1, "computeEnvironment": "ml-ce"}]))
    step("job definition", lambda: b.register_job_definition(jobDefinitionName="embed-job", type="container",
        containerProperties={"image": "123456789012.dkr.ecr.us-east-1.amazonaws.com/embed:1", "vcpus": 2, "memory": 4096, "command": ["python", "embed.py"]}))
    print("queues:", [q["jobQueueName"] for q in b.describe_job_queues()["jobQueues"]])
    print("job defs:", [d["jobDefinitionName"] + ":" + str(d["revision"]) for d in b.describe_job_definitions()["jobDefinitions"]])
    print("(no submit_job attempted: nothing would run)")
