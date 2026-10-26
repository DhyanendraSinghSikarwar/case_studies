# Direct check of Airflow's masker (the component the real worker log path uses).
from airflow.sdk.log import mask_secret
from airflow.sdk._shared.secrets_masker import redact

line = "connecting with password=S3cretPassw0rd to db"
print("before mask_secret:", redact(line))
mask_secret("S3cretPassw0rd")
print("after  mask_secret:", redact(line))
print("by key name       :", redact({"model_api_key": "sk-demo-123456789", "region": "ap-south-1"}))
print("partial/other text:", redact("S3cretPassw0rd!"), "|", redact("s3cretpassw0rd"))
