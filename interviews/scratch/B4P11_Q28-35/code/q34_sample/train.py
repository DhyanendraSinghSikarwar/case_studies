import os, boto3
import sagemaker
DATA = "s3://acme-ml-data/churn/train/"
OUT = os.environ.get("SM_MODEL_DIR", "/opt/ml/model")
s3 = boto3.client("s3", region_name="ap-south-1")
role = "arn:aws:iam::123456789012:role/SageMakerExecRole"
