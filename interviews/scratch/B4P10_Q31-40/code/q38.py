# Q38: KMS envelope encryption. moto for the KMS API, `cryptography` AES-GCM for the local data encryption.
import os
os.environ.update(AWS_ACCESS_KEY_ID="testing", AWS_SECRET_ACCESS_KEY="testing", AWS_DEFAULT_REGION="us-east-1")
import boto3
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from moto import mock_aws

@mock_aws
def main():
    kms = boto3.client("kms")
    key = kms.create_key(Description="ml-data-cmk", KeyUsage="ENCRYPT_DECRYPT")["KeyMetadata"]
    kid = key["KeyId"]
    print("key         :", key["KeyManager"], key["KeyState"], key["Enabled"], "| arn region:", key["Arn"].split(":")[3])
    ctx = {"project": "risk", "dataset": "train-v3"}
    dk = kms.generate_data_key(KeyId=kid, KeySpec="AES_256", EncryptionContext=ctx)
    print("data key    : plaintext", len(dk["Plaintext"]), "bytes | wrapped copy", len(dk["CiphertextBlob"]), "bytes | KeyId matches:", dk["KeyId"] == key["Arn"])
    nonce = os.urandom(12)
    ct = AESGCM(dk["Plaintext"]).encrypt(nonce, b"customer rows: fake data", None)     # local encryption with the plaintext data key
    del dk["Plaintext"]                                                                  # store only (nonce, ct, wrapped key)
    back = kms.decrypt(CiphertextBlob=dk["CiphertextBlob"], EncryptionContext=ctx)["Plaintext"]   # unwrap the data key
    print("decrypted   :", AESGCM(back).decrypt(nonce, ct, None).decode())
    try:
        kms.decrypt(CiphertextBlob=dk["CiphertextBlob"], EncryptionContext={"project": "other"})
        print("wrong context: accepted")
    except Exception as e:
        print("wrong context:", type(e).__name__)
    g = kms.create_grant(KeyId=kid, GranteePrincipal="arn:aws:iam::123456789012:role/sm-train", Operations=["Decrypt", "GenerateDataKey"])
    print("grant       :", sorted(g.keys() - {"ResponseMetadata"}), "| listed:", len(kms.list_grants(KeyId=kid)["Grants"]))
    kms.enable_key_rotation(KeyId=kid); print("rotation    :", kms.get_key_rotation_status(KeyId=kid)["KeyRotationEnabled"])
    kms.disable_key(KeyId=kid)
    try:
        kms.decrypt(CiphertextBlob=dk["CiphertextBlob"], EncryptionContext=ctx); print("after disable: decrypt still worked in moto (real KMS is documented to refuse; check current docs)")
    except Exception as e: print("after disable: decrypt ->", type(e).__name__)
    d = kms.schedule_key_deletion(KeyId=kid, PendingWindowInDays=7)
    print("deletion    :", {k: str(v)[:19] for k, v in d.items() if k != "ResponseMetadata"}, "| state now:", kms.describe_key(KeyId=kid)["KeyMetadata"]["KeyState"])
main()
print("Real key-policy and IAM enforcement NOT executed; moto does not check who may call kms:Decrypt.")
