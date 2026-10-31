"""Q43: validate the cluster spec (pyyaml + hand checks) and probe moto for placement groups / launch templates."""
import os, sys, re
os.environ.update(AWS_ACCESS_KEY_ID="testing", AWS_SECRET_ACCESS_KEY="testing", AWS_DEFAULT_REGION="ap-south-1")
import yaml, boto3
from moto import mock_aws
here = os.path.dirname(os.path.abspath(__file__))
spec = yaml.safe_load(open(os.path.join(here, "q43_cluster_spec.yaml")))

errs = []
pg, lt, c, io = spec["placement_group"], spec["launch_template"], spec["cluster"], spec["training_io"]
if pg["strategy"] not in ("cluster", "partition", "spread"): errs.append("bad placement strategy")
if not c["availability_zone"].startswith(c["region"]): errs.append("AZ not in Region")
if lt["efa"] and pg["strategy"] != "cluster": errs.append("EFA multi-node training normally wants a cluster placement group")
if lt["capacity"]["market"] == "spot" and lt["capacity"]["nodes"] > 1: errs.append("spot + tightly coupled multi-node: one reclaim kills the job")
if not re.match(r"^ami-[0-9a-f]{8,17}$", lt["image_id"]): errs.append("image_id format")
for k in ("data_prefix", "checkpoint_prefix"):
    if not io[k].startswith("s3://") or not io[k].endswith("/"): errs.append(f"{k} must be s3://.../")
print("YAML parsed; sections:", sorted(spec))
print("spec errors:", errs or "none")

# negative test: break the spec and make sure the checker notices
bad = yaml.safe_load(yaml.safe_dump(spec)); bad["placement_group"]["strategy"] = "spread"
print("EFA with spread group flagged:", bad["launch_template"]["efa"] and bad["placement_group"]["strategy"] != "cluster")

with mock_aws():
    ec2 = boto3.client("ec2")
    try:
        ec2.create_placement_group(GroupName=pg["name"], Strategy=pg["strategy"])
        print("create_placement_group: ok")
    except Exception as e:
        print("create_placement_group:", type(e).__name__, str(e)[:90])
    r = ec2.create_launch_template(LaunchTemplateName=lt["name"], LaunchTemplateData={
        "ImageId": lt["image_id"], "InstanceType": lt["instance_type"],
        "NetworkInterfaces": [{"DeviceIndex": 0, "InterfaceType": "efa"}],
        "Placement": {"GroupName": pg["name"], "AvailabilityZone": c["availability_zone"]}})
    print("launch template:", r["LaunchTemplate"]["LaunchTemplateName"], "version", r["LaunchTemplate"]["LatestVersionNumber"])
    d = ec2.describe_launch_template_versions(LaunchTemplateName=lt["name"])["LaunchTemplateVersions"][0]["LaunchTemplateData"]
    print("read back: type", d["InstanceType"], "| NIC", d["NetworkInterfaces"][0]["InterfaceType"], "| placement", d.get("Placement"))
    it = ec2.describe_instance_types(InstanceTypes=[lt["instance_type"]])["InstanceTypes"][0]
    print("describe_instance_types:", it["InstanceType"], "| GPUs:", [(g["Name"], g["Count"]) for g in it.get("GpuInfo", {}).get("Gpus", [])],
          "| EfaSupported:", it.get("NetworkInfo", {}).get("EfaSupported"))
