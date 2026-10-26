import os, base64
for k, v in {"AWS_ACCESS_KEY_ID": "testing", "AWS_SECRET_ACCESS_KEY": "testing", "AWS_DEFAULT_REGION": "us-east-1"}.items():
    os.environ[k] = v
import boto3
from moto import mock_aws
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

with mock_aws():
    kms = boto3.client("kms")
    key = kms.create_key(Description="ml-data-key")["KeyMetadata"]
    arn = key["Arn"]
    s3 = boto3.client("s3")
    s3.create_bucket(Bucket="ml-secure-data")
    s3.put_bucket_encryption(Bucket="ml-secure-data", ServerSideEncryptionConfiguration={"Rules": [
        {"ApplyServerSideEncryptionByDefault": {"SSEAlgorithm": "aws:kms", "KMSMasterKeyID": arn}, "BucketKeyEnabled": True}]})
    print("default encryption:", s3.get_bucket_encryption(Bucket="ml-secure-data")["ServerSideEncryptionConfiguration"]["Rules"][0]["ApplyServerSideEncryptionByDefault"]["SSEAlgorithm"])
    s3.put_object(Bucket="ml-secure-data", Key="train/a.csv", Body=b"a,b\n1,2\n")  # no encryption args
    h = s3.head_object(Bucket="ml-secure-data", Key="train/a.csv")
    print("head_object ServerSideEncryption:", h["ServerSideEncryption"], "| key id matches:", h["SSEKMSKeyId"] == arn)

    # envelope encryption: KMS only protects a small data key
    ctx = {"dataset": "train-v1"}
    dk = kms.generate_data_key(KeyId=arn, KeySpec="AES_256", EncryptionContext=ctx)
    print("plaintext data key bytes:", len(dk["Plaintext"]), "| wrapped key bytes (opaque blob):", len(dk["CiphertextBlob"]) > 32)
    nonce = os.urandom(12)
    ct = AESGCM(dk["Plaintext"]).encrypt(nonce, b"big training file contents", None)
    del dk["Plaintext"]  # real code wipes the plaintext key after use
    stored = (dk["CiphertextBlob"], nonce, ct)   # what you store beside the object
    plain_key = kms.decrypt(CiphertextBlob=stored[0], EncryptionContext=ctx)["Plaintext"]
    print("round trip:", AESGCM(plain_key).decrypt(stored[1], stored[2], None))
    # grants
    g = kms.create_grant(KeyId=arn, GranteePrincipal="arn:aws:iam::123456789012:role/sm-exec", Operations=["Decrypt", "GenerateDataKey"])
    print("grant created:", bool(g["GrantId"]), "| list_grants:", len(kms.list_grants(KeyId=arn)["Grants"]))
    print("NOT shown: key-policy / IAM / grant enforcement; this script never tested a caller without kms:Decrypt.")
