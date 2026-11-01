import os, io, zipfile
for k, v in {"AWS_ACCESS_KEY_ID": "testing", "AWS_SECRET_ACCESS_KEY": "testing", "AWS_DEFAULT_REGION": "us-east-1"}.items():
    os.environ[k] = v
import boto3
from moto import mock_aws

def zipped(src):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("app.py", src)
    return buf.getvalue()

with mock_aws():
    iam = boto3.client("iam")
    role = iam.create_role(RoleName="lam", AssumeRolePolicyDocument='{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"lambda.amazonaws.com"},"Action":"sts:AssumeRole"}]}')["Role"]["Arn"]
    lam = boto3.client("lambda")
    lam.create_function(FunctionName="score", Runtime="python3.12", Role=role, Handler="app.handler",
                        Code={"ZipFile": zipped("def handler(e, c):\n    return {'ok': 1}\n")},
                        MemorySize=1024, Timeout=30, Publish=True,
                        Environment={"Variables": {"MODEL_URI": "s3://ml-data/models/m1/"}})
    lam.put_function_concurrency(FunctionName="score", ReservedConcurrentExecutions=5)
    cfg = lam.get_function_configuration(FunctionName="score")
    print({k: cfg[k] for k in ("FunctionName", "Runtime", "MemorySize", "Timeout", "Handler", "PackageType", "State")})
    print("env:", cfg["Environment"]["Variables"])
    print("reserved concurrency:", lam.get_function_concurrency(FunctionName="score")["ReservedConcurrentExecutions"])
    layer = lam.publish_layer_version(LayerName="deps", Content={"ZipFile": zipped("x=1")}, CompatibleRuntimes=["python3.12"])
    print("layer version:", layer["Version"])
    try:
        pc = lam.put_provisioned_concurrency_config(FunctionName="score", Qualifier="1", ProvisionedConcurrentExecutions=2)
        print("provisioned:", pc.get("RequestedProvisionedConcurrentExecutions"), pc.get("Status"))
    except Exception as e:
        print("provisioned concurrency call:", type(e).__name__, str(e)[:100])
    r = lam.invoke(FunctionName="score", Payload=b"{}")
    body = r["Payload"].read().decode()
    print("invoke StatusCode:", r["StatusCode"], "| payload starts:", body[:80].replace("\n", " "))
