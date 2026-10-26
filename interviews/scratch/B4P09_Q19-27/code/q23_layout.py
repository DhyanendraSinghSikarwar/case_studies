import sys, os, glob, shutil; sys.path.insert(0, "/home/user/case_studies/interviews/scratch/B4P09_Q19-27/code")
from spark_common import get_spark
from pyspark.sql import functions as F
spark, base = get_spark("q23")
print("pyspark", __import__("pyspark").__version__)
out = os.path.join(base, "feat"); shutil.rmtree(out, ignore_errors=True)

# 6 days x 2000 users, one feature value per user per day (seeded, deterministic)
df = (spark.range(12000).select((F.col("id") % 2000).alias("user_id"),
        F.expr("date_add(DATE'2025-03-01', cast(id div 2000 as int))").alias("day"),
        (F.rand(23) * 100).alias("txn_30d")))

def nfiles(path): return len(glob.glob(path + "/**/*.parquet", recursive=True))
def ndirs(path):  return len(glob.glob(path + "/day=*"))

# tiny files: 24 write tasks, each holds rows of every day -> up to 24 files per day
df.repartition(24).write.partitionBy("day").mode("overwrite").parquet(out + "_tiny")
print("tiny    : partitions(dirs)=", ndirs(out + "_tiny"), " parquet files=", nfiles(out + "_tiny"))

# compacted: shuffle by the partition column so each day lands in one task -> about 1 file per day
df.repartition("day").write.partitionBy("day").mode("overwrite").parquet(out + "_compact")
print("compact : partitions(dirs)=", ndirs(out + "_compact"), " parquet files=", nfiles(out + "_compact"))

# same answer either way
a = spark.read.parquet(out + "_tiny"); b = spark.read.parquet(out + "_compact")
print("row counts:", a.count(), b.count(), "| sum of feature equal:",
      abs(a.agg(F.sum("txn_30d")).first()[0] - b.agg(F.sum("txn_30d")).first()[0]) < 1e-6)

# partition pruning: filter on the partition column
q = b.filter(F.col("day") == "2025-03-04")
print("-- scan line for day = 2025-03-04")
for l in q._jdf.queryExecution().executedPlan().toString().split("\n"):
    if "FileScan" in l: print("  ", l.strip().split("Location:")[0][:90], "...", "PartitionFilters:", l.split("PartitionFilters:")[1].split(", PushedFilters")[0][:120])
print("rows for that day:", q.count(), "(expected 2000)")
# a filter on a NON-partition column cannot prune directories
q2 = b.filter(F.col("user_id") == 7)
for l in q2._jdf.queryExecution().executedPlan().toString().split("\n"):
    if "FileScan" in l: print("-- filter on user_id (not a partition column): PartitionFilters:", l.split("PartitionFilters:")[1].split(", PushedFilters")[0][:60], "| DataFilters:", l.split("DataFilters:")[1].split(", Format")[0])
spark.stop()
