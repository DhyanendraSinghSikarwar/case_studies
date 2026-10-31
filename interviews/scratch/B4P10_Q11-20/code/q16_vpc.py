import os
for k, v in {"AWS_ACCESS_KEY_ID": "testing", "AWS_SECRET_ACCESS_KEY": "testing", "AWS_DEFAULT_REGION": "us-east-1"}.items():
    os.environ[k] = v
import boto3
from moto import mock_aws

# ---- part 1: moto API shapes
with mock_aws():
    ec2 = boto3.client("ec2")
    vpc = ec2.create_vpc(CidrBlock="10.0.0.0/16")["Vpc"]["VpcId"]
    sub = ec2.create_subnet(VpcId=vpc, CidrBlock="10.0.1.0/24")["Subnet"]
    sg = ec2.create_security_group(GroupName="train-sg", Description="training", VpcId=vpc)["GroupId"]
    ec2.authorize_security_group_ingress(GroupId=sg, IpPermissions=[{"IpProtocol": "tcp", "FromPort": 443, "ToPort": 443, "IpRanges": [{"CidrIp": "10.0.0.0/16"}]}])
    rt = ec2.create_route_table(VpcId=vpc)["RouteTable"]["RouteTableId"]
    ec2.associate_route_table(RouteTableId=rt, SubnetId=sub["SubnetId"])
    ep = ec2.create_vpc_endpoint(VpcId=vpc, ServiceName="com.amazonaws.us-east-1.s3", VpcEndpointType="Gateway", RouteTableIds=[rt])["VpcEndpoint"]
    print("subnet cidr:", sub["CidrBlock"], "| endpoint:", ep["ServiceName"], ep["VpcEndpointType"], ep["State"])
    rules = ec2.describe_security_group_rules(Filters=[{"Name": "group-id", "Values": [sg]}])["SecurityGroupRules"]
    print("sg rules:", [(r["IsEgress"], r["IpProtocol"], r["FromPort"], r["CidrIpv4"]) for r in rules])
    print("API shape only: no packet was routed, no ENI attached to anything.")

# ---- part 2: stateful (SG) versus stateless (NACL) in pure Python
class SG:  # allow-only rules, default deny, remembers connections it admitted
    def __init__(self, ingress, egress): self.ingress, self.egress, self.conns = ingress, egress, set()
    def inbound(self, pkt):
        if any(r["proto"] == pkt["proto"] and r["port"] == pkt["dport"] for r in self.ingress):
            self.conns.add((pkt["proto"], pkt["sport"], pkt["dport"]))
            return True
        return False
    def outbound(self, pkt):
        if (pkt["proto"], pkt["dport"], pkt["sport"]) in self.conns:  # reply to a tracked connection
            return True
        return any(r["proto"] == pkt["proto"] and r["port"] == pkt["dport"] for r in self.egress)

def nacl_allows(rules, pkt, direction):  # ordered, first match wins, final implicit deny
    for r in sorted(rules[direction], key=lambda r: r["num"]):
        lo, hi = r["ports"]
        if r["proto"] == pkt["proto"] and lo <= pkt["dport"] <= hi:
            return r["action"] == "allow"
    return False

req = {"proto": "tcp", "sport": 51000, "dport": 443}
resp = {"proto": "tcp", "sport": 443, "dport": 51000}      # reply travels back to ephemeral port
sg = SG(ingress=[{"proto": "tcp", "port": 443}], egress=[])  # NO egress rules at all
print("\nSG  request in:", sg.inbound(req), "| reply out with zero egress rules:", sg.outbound(resp))
print("SG  fresh outbound connection to 443 with zero egress rules:", sg.outbound({"proto": "tcp", "sport": 40000, "dport": 443}))
print("SG  request to closed port 22:", sg.inbound({"proto": "tcp", "sport": 50000, "dport": 22}))

nacl_bad = {"in": [{"num": 100, "proto": "tcp", "ports": (443, 443), "action": "allow"}], "out": []}
nacl_ok  = {"in": [{"num": 100, "proto": "tcp", "ports": (443, 443), "action": "allow"}],
            "out": [{"num": 100, "proto": "tcp", "ports": (1024, 65535), "action": "allow"}]}
nacl_deny = {"in": [{"num": 90, "proto": "tcp", "ports": (443, 443), "action": "deny"},
                    {"num": 100, "proto": "tcp", "ports": (0, 65535), "action": "allow"}], "out": []}
for name, n in (("NACL missing outbound ephemeral", nacl_bad), ("NACL with ephemeral outbound", nacl_ok)):
    print(f"{name}: request in={nacl_allows(n, req, 'in')}, reply out={nacl_allows(n, resp, 'out')}")
print("NACL rule 90 deny 443 beats rule 100 allow all:", nacl_allows(nacl_deny, req, "in"))
