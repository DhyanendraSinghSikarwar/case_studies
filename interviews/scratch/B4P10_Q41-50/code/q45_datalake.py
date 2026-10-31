"""Q45: data lake layout tree, naming regex checker, versioned replication-ready bucket in moto (API shape only)."""
import os, re, json
os.environ.update(AWS_ACCESS_KEY_ID="testing", AWS_SECRET_ACCESS_KEY="testing", AWS_DEFAULT_REGION="us-east-1")
import boto3
from moto import mock_aws

TREE = """s3://acme-ml-prod-lake/            (one bucket per environment; bucket names are global, so prefix with org)
  raw/<source>/ingest_date=YYYY-MM-DD/   immutable, append-only, never edited in place
  curated/<domain>/<table>/dt=YYYY-MM-DD/   Parquet, partitioned by date
  snapshots/<dataset>/v<NNN>/            frozen training sets, one prefix per version
  models/<model>/<run_id>/               artifacts written by training jobs
  tmp/                                   short lifecycle expiry"""
print(TREE, "\n")

BUCKET = re.compile(r"^[a-z0-9]+-ml-(dev|stage|prod)-[a-z0-9-]+$")
KEY = re.compile(r"^(raw/[a-z0-9_]+/ingest_date=\d{4}-\d{2}-\d{2}/.+|"
                 r"curated/[a-z0-9_]+/[a-z0-9_]+/dt=\d{4}-\d{2}-\d{2}/.+|"
                 r"snapshots/[a-z0-9_]+/v\d{3}/.+|models/[a-z0-9_-]+/[a-z0-9-]+/.+|tmp/.+)$")
for b in ["acme-ml-prod-lake", "acme-ml-qa-lake", "Acme_ML_prod", "ab"]:
    print(f"bucket {b!r:22} ->", "ok" if BUCKET.match(b) else "REJECT")
for k in ["raw/upi/ingest_date=2026-10-01/part-0.parquet", "curated/risk/features/dt=2026-10-01/p0.parquet",
          "snapshots/pd_train/v003/train.parquet", "raw/upi/2026-10-01/part-0.parquet", "snapshots/pd_train/v3/x", "Models/x/y/z"]:
    print(f"key    {k!r:55} ->", "ok" if KEY.match(k) else "REJECT")

with mock_aws():
    s3 = boto3.client("s3")
    # replication needs versioning on BOTH sides
    s3.create_bucket(Bucket="acme-ml-prod-lake", ObjectLockEnabledForBucket=True)   # lock can be enabled at create (also enables versioning)
    s3.create_bucket(Bucket="acme-ml-prod-lake-dr")
    s3.put_bucket_versioning(Bucket="acme-ml-prod-lake-dr", VersioningConfiguration={"Status": "Enabled"})
    print("\nsource versioning:", s3.get_bucket_versioning(Bucket="acme-ml-prod-lake").get("Status"))
    s3.put_bucket_replication(Bucket="acme-ml-prod-lake", ReplicationConfiguration={
        "Role": "arn:aws:iam::123456789012:role/s3-replication",
        "Rules": [{"ID": "snapshots-dr", "Status": "Enabled", "Priority": 1, "Filter": {"Prefix": "snapshots/"},
                   "DeleteMarkerReplication": {"Status": "Disabled"},
                   "Destination": {"Bucket": "arn:aws:s3:::acme-ml-prod-lake-dr"}}]})
    r = s3.get_bucket_replication(Bucket="acme-ml-prod-lake")["ReplicationConfiguration"]
    rule = r["Rules"][0]
    print("replication rule read back (we sent Filter Prefix 'snapshots/'):", json.dumps({k: rule.get(k) for k in ("ID", "Status", "Priority", "Filter", "Prefix", "Destination")}))
    try:
        print("object lock config:", s3.get_object_lock_configuration(Bucket="acme-ml-prod-lake")["ObjectLockConfiguration"])
    except Exception as e: print("object lock:", type(e).__name__, str(e)[:80])
    try:
        s3.create_bucket(Bucket="no-versioning-src"); 
        s3.put_bucket_replication(Bucket="no-versioning-src", ReplicationConfiguration={"Role": "arn:aws:iam::123456789012:role/s3-replication",
            "Rules": [{"ID": "x", "Status": "Enabled", "Priority": 1, "Filter": {"Prefix": ""}, "DeleteMarkerReplication": {"Status": "Disabled"}, "Destination": {"Bucket": "arn:aws:s3:::acme-ml-prod-lake-dr"}}]})
        print("replication without source versioning: accepted by moto")
    except Exception as e: print("replication without source versioning:", type(e).__name__, str(e)[:90])
