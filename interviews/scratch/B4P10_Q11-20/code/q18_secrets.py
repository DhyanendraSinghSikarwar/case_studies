import os
for k, v in {"AWS_ACCESS_KEY_ID": "testing", "AWS_SECRET_ACCESS_KEY": "testing", "AWS_DEFAULT_REGION": "us-east-1"}.items():
    os.environ[k] = v
import boto3
from moto import mock_aws

with mock_aws():
    sm = boto3.client("secretsmanager")
    sm.create_secret(Name="prod/train/db", SecretString='{"user":"etl","password":"FAKE-not-real-pw"}')
    sm.put_secret_value(SecretId="prod/train/db", SecretString='{"user":"etl","password":"FAKE-rotated-pw"}')
    v = sm.get_secret_value(SecretId="prod/train/db")
    print("secret stages:", v["VersionStages"], "| value:", v["SecretString"])
    vers = sm.list_secret_version_ids(SecretId="prod/train/db", IncludeDeprecated=True)["Versions"]
    print("versions with stages:", sorted(str(x.get("VersionStages")) for x in vers))
    ssm = boto3.client("ssm")
    ssm.put_parameter(Name="/prod/train/api_key", Value="FAKE-api-key-123", Type="SecureString")
    raw = ssm.get_parameter(Name="/prod/train/api_key")["Parameter"]
    dec = ssm.get_parameter(Name="/prod/train/api_key", WithDecryption=True)["Parameter"]
    print("ssm without decryption: type", raw["Type"], "version", raw["Version"], "| value starts:", raw["Value"][:10])
    print("ssm with decryption   :", dec["Value"])
    print("Not emulated: IAM/KMS checks on these reads, real rotation Lambda, CloudTrail audit.")
