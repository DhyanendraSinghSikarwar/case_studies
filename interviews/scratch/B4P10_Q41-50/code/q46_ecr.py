"""Q46: ECR repo (immutable tags, scan on push, lifecycle) in moto + deployment-manifest image-ref validator. No images built or pulled."""
import os, re, json, hashlib
os.environ.update(AWS_ACCESS_KEY_ID="testing", AWS_SECRET_ACCESS_KEY="testing", AWS_DEFAULT_REGION="us-east-1")
import boto3
from moto import mock_aws

REF = re.compile(r"^(?P<host>\d{12}\.dkr\.ecr\.[a-z0-9-]+\.amazonaws\.com)/(?P<repo>[a-z0-9._/-]+)(?::(?P<tag>[\w.-]{1,128}))?(?:@(?P<digest>sha256:[0-9a-f]{64}))?$")

def check_ref(ref):
    """Return (ok, why). Deploy rule: must be pinned by digest; tag alone is mutable unless the repo is immutable, and 'latest' is never allowed."""
    m = REF.match(ref)
    if not m: return False, "not an ECR image reference"
    if m["digest"]: return True, "pinned by digest"
    if m["tag"] in (None, "latest"): return False, "untagged or :latest"
    return False, f"tag only (:{m['tag']}); resolve to a digest before deploy"

manifest = json.dumps({"schemaVersion": 2, "mediaType": "application/vnd.docker.distribution.manifest.v2+json", "config": {"digest": "sha256:" + "0" * 64}, "layers": []})
digest = "sha256:" + hashlib.sha256(manifest.encode()).hexdigest()
acct = "123456789012"; host = f"{acct}.dkr.ecr.us-east-1.amazonaws.com"

with mock_aws():
    ecr = boto3.client("ecr")
    repo = ecr.create_repository(repositoryName="ml/pd-model", imageTagMutability="IMMUTABLE",
                                 imageScanningConfiguration={"scanOnPush": True})["repository"]
    print("repo:", repo["repositoryName"], "| mutability:", repo["imageTagMutability"], "| scanOnPush:", repo["imageScanningConfiguration"]["scanOnPush"])
    print("repositoryUri:", repo["repositoryUri"])
    rules = {"rules": [{"rulePriority": 1, "description": "keep last 10 tagged v*",
                        "selection": {"tagStatus": "tagged", "tagPrefixList": ["v"], "countType": "imageCountMoreThan", "countNumber": 10},
                        "action": {"type": "expire"}},
                       {"rulePriority": 2, "description": "expire untagged after 14 days",
                        "selection": {"tagStatus": "untagged", "countType": "sinceImagePushed", "countUnit": "days", "countNumber": 14},
                        "action": {"type": "expire"}}]}
    ecr.put_lifecycle_policy(repositoryName="ml/pd-model", lifecyclePolicyText=json.dumps(rules))
    got = json.loads(ecr.get_lifecycle_policy(repositoryName="ml/pd-model")["lifecyclePolicyText"])
    print("lifecycle rules read back:", [(r["rulePriority"], r["selection"]["tagStatus"]) for r in got["rules"]])

    ecr.put_image(repositoryName="ml/pd-model", imageManifest=manifest, imageTag="v1")
    try:
        ecr.put_image(repositoryName="ml/pd-model", imageManifest=manifest + " ", imageTag="v1")
    except Exception as e:
        print("re-push v1 with different content:", type(e).__name__)
    imgs = ecr.describe_images(repositoryName="ml/pd-model")["imageDetails"]
    print("images:", [(i["imageTags"], i["imageDigest"][:19] + "...") for i in imgs])
    # cross-account pull policy (resource-based policy on the repo); read back only
    pol = {"Version": "2012-10-17", "Statement": [{"Sid": "ProdPull", "Effect": "Allow",
           "Principal": {"AWS": "arn:aws:iam::999999999999:role/prod-sagemaker-exec"},
           "Action": ["ecr:BatchGetImage", "ecr:GetDownloadUrlForLayer"]}]}
    ecr.set_repository_policy(repositoryName="ml/pd-model", policyText=json.dumps(pol))
    print("repo policy principal:", json.loads(ecr.get_repository_policy(repositoryName="ml/pd-model")["policyText"])["Statement"][0]["Principal"]["AWS"])

print("\n== image reference validator ==")
for r in [f"{host}/ml/pd-model@{digest}", f"{host}/ml/pd-model:v1", f"{host}/ml/pd-model:latest", f"{host}/ml/pd-model", "python:3.12", f"{host}/ml/pd-model:v1@{digest}"]:
    ok, why = check_ref(r)
    print(f"{'PASS' if ok else 'FAIL'}  {r[:60]:60s} {why}")
