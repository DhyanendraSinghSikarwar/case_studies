# Q36: request counting, no timings. Part 1 pure arithmetic simulation; part 2 real boto3 calls into moto with a call counter.
import os, math
os.environ.update(AWS_ACCESS_KEY_ID="testing", AWS_SECRET_ACCESS_KEY="testing", AWS_DEFAULT_REGION="us-east-1")
import boto3
from collections import Counter
from moto import mock_aws

LIST_PAGE = 1000                     # ListObjectsV2 returns up to 1000 keys per call (check current docs)
def small_files(n_files):            # 1 LIST page per 1000 keys + 1 GET per file
    return {"LIST": math.ceil(n_files / LIST_PAGE), "GET": n_files}
def shards(total_mb, shard_mb, range_mb):   # LIST of a few keys + ranged GETs inside each shard
    n = math.ceil(total_mb / shard_mb)
    return {"LIST": math.ceil(n / LIST_PAGE), "GET": n * math.ceil(shard_mb / range_mb), "shards": n}
n_files, file_kb = 1_000_000, 100
total_mb = n_files * file_kb / 1024
print(f"dataset: {n_files:,} files x {file_kb} KB = {total_mb:,.0f} MB (about the same bytes in both layouts)")
print("1M small files, one GET each :", small_files(n_files))
print("shards of 256 MB, 64 MB ranges :", shards(total_mb, 256, 64))
print("shards of 256 MB, whole-shard GET:", shards(total_mb, 256, 256))

@mock_aws
def moto_counts():
    s3 = boto3.client("s3"); s3.create_bucket(Bucket="train-data")
    calls = Counter()
    s3.meta.events.register("before-call.s3.*", lambda model, **kw: calls.update([model.name]))
    for i in range(200): s3.put_object(Bucket="train-data", Key=f"small/{i:05d}.bin", Body=b"x" * 100)
    s3.put_object(Bucket="train-data", Key="shards/shard-000.tar", Body=b"x" * 100 * 200)  # same 20,000 bytes in one object
    calls.clear()
    for k in [o["Key"] for o in s3.list_objects_v2(Bucket="train-data", Prefix="small/")["Contents"]]:
        s3.get_object(Bucket="train-data", Key=k)["Body"].read()
    print("moto, 200 small objects :", dict(calls)); calls.clear()
    s3.list_objects_v2(Bucket="train-data", Prefix="shards/")
    got = b"".join(s3.get_object(Bucket="train-data", Key="shards/shard-000.tar", Range=f"bytes={a}-{a+9999}")["Body"].read() for a in (0, 10000))
    print("moto, 1 shard, 2 ranged GETs:", dict(calls), "| bytes read:", len(got))
moto_counts()
print("timings deliberately not printed: a mock on localhost says nothing about S3 latency")
