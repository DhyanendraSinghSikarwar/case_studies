# Q34: SageMaker Feature Store at the service boundary, moto API shape only.
import os, json
os.environ.update(AWS_ACCESS_KEY_ID="testing", AWS_SECRET_ACCESS_KEY="testing", AWS_DEFAULT_REGION="us-east-1")
import boto3
from moto import mock_aws

@mock_aws
def main():
    s3 = boto3.client("s3"); s3.create_bucket(Bucket="ml-features")
    sm = boto3.client("sagemaker")
    r = sm.create_feature_group(
        FeatureGroupName="customer-risk", RecordIdentifierFeatureName="customer_id", EventTimeFeatureName="event_time",
        FeatureDefinitions=[{"FeatureName": "customer_id", "FeatureType": "String"},
                            {"FeatureName": "event_time", "FeatureType": "Fractional"},
                            {"FeatureName": "txn_count_7d", "FeatureType": "Integral"}],
        OnlineStoreConfig={"EnableOnlineStore": True},
        OfflineStoreConfig={"S3StorageConfig": {"S3Uri": "s3://ml-features/offline/"}, "DisableGlueTableCreation": False},
        RoleArn="arn:aws:iam::123456789012:role/sm-featurestore")
    d = sm.describe_feature_group(FeatureGroupName="customer-risk")
    print("status      :", d["FeatureGroupStatus"])
    print("record id   :", d["RecordIdentifierFeatureName"], "| event time:", d["EventTimeFeatureName"])
    print("online      :", d.get("OnlineStoreConfig"))
    print("offline     :", d.get("OfflineStoreConfig", {}).get("S3StorageConfig"))
    print("features    :", [f["FeatureName"] for f in d["FeatureDefinitions"]])
    try: sm.list_feature_groups(); print("list_feature_groups: returned")
    except Exception as e: print("list_feature_groups ->", type(e).__name__, str(e)[:70])
    rt = boto3.client("sagemaker-featurestore-runtime")
    for name, fn in [("put_record", lambda: rt.put_record(FeatureGroupName="customer-risk", Record=[
            {"FeatureName": "customer_id", "ValueAsString": "c1"}, {"FeatureName": "event_time", "ValueAsString": "1700000000.0"},
            {"FeatureName": "txn_count_7d", "ValueAsString": "4"}])),
            ("get_record", lambda: rt.get_record(FeatureGroupName="customer-risk", RecordIdentifierValueAsString="c1"))]:
        try: print(name, "-> returned", fn())
        except Exception as e: print(name, "->", type(e).__name__, str(e)[:100].replace("\n", " "))
    print("NOTE: I sent EnableOnlineStore=True but moto's describe did not echo it (online: None above), so the mock cannot show the online-store flag.")
    # review rule on the REQUEST we hold (sample inventory), not on the mock's answer:
    inventory = [{"name": "customer-risk", "online": True, "last_read_days_ago": 45}, {"name": "txn-agg", "online": False, "last_read_days_ago": 1}]
    print("online stores not read for 30+ days:", [g["name"] for g in inventory if g["online"] and g["last_read_days_ago"] >= 30])
main()
