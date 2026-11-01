# Q35: Athena, Glue, Redshift records in moto + tiny partition-pruning illustration. No query actually ran.
import os
os.environ.update(AWS_ACCESS_KEY_ID="testing", AWS_SECRET_ACCESS_KEY="testing", AWS_DEFAULT_REGION="us-east-1")
import boto3
from moto import mock_aws

@mock_aws
def main():
    glue = boto3.client("glue")
    glue.create_database(DatabaseInput={"Name": "ml_lake"})
    glue.create_table(DatabaseName="ml_lake", TableInput={"Name": "txns", "PartitionKeys": [{"Name": "dt", "Type": "string"}],
        "StorageDescriptor": {"Columns": [{"Name": "txn_id", "Type": "string"}, {"Name": "amount", "Type": "double"}],
        "Location": "s3://ml-lake/curated/txns/", "InputFormat": "org.apache.hadoop.mapred.TextInputFormat",
        "OutputFormat": "org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat",
        "SerdeInfo": {"SerializationLibrary": "org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe"}}, "TableType": "EXTERNAL_TABLE"})
    t = glue.get_table(DatabaseName="ml_lake", Name="txns")["Table"]
    print("glue table  :", t["Name"], "| partition keys:", [p["Name"] for p in t["PartitionKeys"]], "|", t["StorageDescriptor"]["Location"])
    boto3.client("s3").create_bucket(Bucket="ml-athena-out")
    a = boto3.client("athena")
    q = a.start_query_execution(QueryString="SELECT count(*) FROM ml_lake.txns WHERE dt = '2026-10-01'",
        QueryExecutionContext={"Database": "ml_lake"}, ResultConfiguration={"OutputLocation": "s3://ml-athena-out/"})
    st = a.get_query_execution(QueryExecutionId=q["QueryExecutionId"])["QueryExecution"]["Status"]["State"]
    print("athena      : query id present:", bool(q["QueryExecutionId"]), "| state:", st, "(mock; no data scanned)")
    rs = boto3.client("redshift")
    c = rs.create_cluster(ClusterIdentifier="dw", NodeType="ra3.xlplus", MasterUsername="admin", MasterUserPassword="Fake1234Pass",
                          ClusterType="single-node", DBName="analytics")["Cluster"]
    print("redshift    :", c["ClusterIdentifier"], c["ClusterStatus"], c["DBName"], "(record only; no warehouse, no SQL)")
main()

# Partition pruning, hand-checkable: a Hive-style layout dt=YYYY-MM-DD; a query with dt filter reads only matching prefixes.
days = [f"2026-10-{d:02d}" for d in range(1, 31)]
files_per_day = 4
keys = [f"curated/txns/dt={d}/part-{i}.parquet" for d in days for i in range(files_per_day)]
def prune(keys, want): return [k for k in keys if f"dt={want}/" in k]
print("\nobjects in table:", len(keys), "| objects a dt='2026-10-01' query must read:", len(prune(keys, "2026-10-01")))
print("same query without a partition filter reads:", len(keys))
