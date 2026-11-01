import os
os.environ.update(AWS_ACCESS_KEY_ID="testing",AWS_SECRET_ACCESS_KEY="testing",AWS_DEFAULT_REGION="us-east-1")
import boto3
from moto import mock_aws

with mock_aws():
    ec2 = boto3.client("ec2"); asg = boto3.client("autoscaling")
    ami = ec2.describe_images()["Images"][0]["ImageId"]
    vpc = ec2.create_vpc(CidrBlock="10.0.0.0/16")["Vpc"]["VpcId"]
    sn = ec2.create_subnet(VpcId=vpc, CidrBlock="10.0.1.0/24")["Subnet"]["SubnetId"]
    ec2.create_launch_template(LaunchTemplateName="infer-lt", LaunchTemplateData={"ImageId": ami, "InstanceType": "g5.xlarge"})
    asg.create_auto_scaling_group(AutoScalingGroupName="infer-asg", LaunchTemplate={"LaunchTemplateName": "infer-lt", "Version": "$Latest"},
        MinSize=1, MaxSize=6, DesiredCapacity=2, VPCZoneIdentifier=sn, HealthCheckType="EC2", HealthCheckGracePeriod=300)
    asg.put_scaling_policy(AutoScalingGroupName="infer-asg", PolicyName="cpu50", PolicyType="TargetTrackingScaling",
        TargetTrackingConfiguration={"PredefinedMetricSpecification": {"PredefinedMetricType": "ASGAverageCPUUtilization"}, "TargetValue": 50.0})
    asg.put_scheduled_update_group_action(AutoScalingGroupName="infer-asg", ScheduledActionName="nightly-up", Recurrence="0 20 * * *", MinSize=2, MaxSize=6, DesiredCapacity=4)
    g = asg.describe_auto_scaling_groups(AutoScalingGroupNames=["infer-asg"])["AutoScalingGroups"][0]
    print("min/max/desired:", g["MinSize"], g["MaxSize"], g["DesiredCapacity"], "health:", g["HealthCheckType"], g["HealthCheckGracePeriod"])
    print("launch template:", g.get("LaunchTemplate", {}).get("LaunchTemplateName"))
    p = asg.describe_policies(AutoScalingGroupName="infer-asg")["ScalingPolicies"][0]
    print("policy:", p["PolicyName"], p["PolicyType"], p["TargetTrackingConfiguration"]["TargetValue"])
    print("scheduled:", [a["ScheduledActionName"] for a in asg.describe_scheduled_actions(AutoScalingGroupName="infer-asg")["ScheduledUpdateGroupActions"]])
    print("instances in group (moto creates records, no real boot):", len(g["Instances"]))
    try:
        asg.set_instance_protection(AutoScalingGroupName="infer-asg", InstanceIds=[g["Instances"][0]["InstanceId"]], ProtectedFromScaleIn=True)
        print("scale-in protection set OK")
    except Exception as e: print("scale-in protection:", type(e).__name__, str(e)[:80])
