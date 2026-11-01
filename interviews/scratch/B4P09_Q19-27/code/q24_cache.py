import sys; sys.path.insert(0, "/home/user/case_studies/interviews/scratch/B4P09_Q19-27/code")
from spark_common import get_spark
from pyspark.sql import functions as F
from pyspark import StorageLevel
spark, _ = get_spark("q24")
sc = spark.sparkContext
print("pyspark", __import__("pyspark").__version__, "| cores (defaultParallelism) =", sc.defaultParallelism)

# A "source" that counts how many rows it produced, via an accumulator (counts re-computation).
def build(acc):
    def tag(r):
        acc.add(1); return (r.id, r.id % 10)
    return spark.range(10000).rdd.map(tag).toDF(["id", "k"])

def run(label, use_cache):
    acc = sc.accumulator(0)
    df = build(acc)
    if use_cache: df = df.persist(StorageLevel.MEMORY_AND_DISK)
    a1 = df.groupBy("k").count().count()           # action 1: 10 groups
    a2 = df.filter("k = 3").count()                # action 2: 1000 rows
    a3 = df.agg(F.sum("id")).first()[0]            # action 3
    print(f"{label:10s} actions=3 results=({a1},{a2},{a3}) source rows computed = {acc.value}")
    if use_cache:
        print("           storage level:", df.storageLevel, "| plan has InMemoryTableScan:",
              "InMemoryTableScan" in df.filter("k=3")._jdf.queryExecution().executedPlan().toString())
        df.unpersist()
run("no cache", False)
run("cache", True)
print("(accumulators inside transformations can over-count on task retries; fine as a teaching probe)")

# Partition sizing
df = spark.range(100000)
print("-- partition counts")
print("read default (range splits)         :", df.rdd.getNumPartitions())
r8 = df.repartition(8); print("repartition(8)                      :", r8.rdd.getNumPartitions())
c2 = r8.coalesce(2);    print("repartition(8).coalesce(2)          :", c2.rdd.getNumPartitions())
c16 = r8.coalesce(16);  print("repartition(8).coalesce(16)         :", c16.rdd.getNumPartitions(), "(coalesce cannot grow)")
g = df.withColumn("k", F.col("id") % 10).groupBy("k").count()
print("after groupBy (shuffle.partitions=4):", g.rdd.getNumPartitions())
sizes = r8.rdd.glom().map(len).collect(); print("repartition(8) rows per partition   :", sizes)
sk = df.coalesce(2).rdd.glom().map(len).collect(); print("coalesce(2) from 4 splits, rows/part:", sk)
print("-- plan nodes")
for name, d in [("repartition(8)", r8), ("coalesce(2)", df.coalesce(2))]:
    lines = [l.strip()[:70] for l in d._jdf.queryExecution().executedPlan().toString().split("\n") if "Exchange" in l or "Coalesce" in l]
    print(f"{name:15s}:", lines)
spark.stop()
