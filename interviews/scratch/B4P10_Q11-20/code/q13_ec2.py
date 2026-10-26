import os
for k, v in {"AWS_ACCESS_KEY_ID": "testing", "AWS_SECRET_ACCESS_KEY": "testing", "AWS_DEFAULT_REGION": "us-east-1"}.items():
    os.environ[k] = v
import boto3
from moto import mock_aws

with mock_aws():
    ec2 = boto3.client("ec2")
    r = ec2.describe_instance_types(InstanceTypes=["p4d.24xlarge", "g5.xlarge", "m5.xlarge", "trn1.2xlarge"])
    for t in sorted(r["InstanceTypes"], key=lambda x: x["InstanceType"]):
        gpu = t.get("GpuInfo", {}).get("Gpus", [])
        print(t["InstanceType"], "vcpu", t["VCpuInfo"]["DefaultVCpus"], "mem_MiB", t["MemoryInfo"]["SizeInMiB"],
              "gpus", [(g["Name"], g["Count"]) for g in gpu])
    got = {t["InstanceType"] for t in r["InstanceTypes"]}
    print("asked 4, moto returned:", sorted(got))
    inst = ec2.run_instances(ImageId="ami-12345678", InstanceType="g5.xlarge", MinCount=1, MaxCount=1,
                             BlockDeviceMappings=[{"DeviceName": "/dev/sda1", "Ebs": {"VolumeSize": 200, "VolumeType": "gp3", "DeleteOnTermination": True}}],
                             TagSpecifications=[{"ResourceType": "instance", "Tags": [{"Key": "team", "Value": "ml"}]}])["Instances"][0]
    print("run_instances state:", inst["State"]["Name"], "type:", inst["InstanceType"])
    vols = ec2.describe_volumes()["Volumes"]
    print("volumes:", [(v["Size"], v["VolumeType"]) for v in vols])
