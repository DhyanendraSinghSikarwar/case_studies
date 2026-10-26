import os, tempfile, shutil, time
from pyspark.sql import SparkSession, functions as F
W = tempfile.mkdtemp(prefix="q14_", dir="/tmp/claude-0/b9_q10_18")
spark = (SparkSession.builder.master("local[2]").appName("q14")
         .config("spark.ui.enabled", "false").config("spark.ui.showConsoleProgress", "false")
         .config("spark.sql.shuffle.partitions", "4").config("spark.sql.adaptive.enabled", "false")
         .config("spark.local.dir", os.path.join(W, "local")).config("spark.sql.warehouse.dir", os.path.join(W, "wh"))
         .getOrCreate())
spark.sparkContext.setLogLevel("ERROR")
print("spark", spark.version, "| AQE disabled on purpose for the demo")

# 100,000 events: 80% belong to merchant 'm_hot', the rest spread over 99 merchants (seeded, deterministic)
n = 100_000
df = (spark.range(n).withColumn("r", F.rand(42))
      .withColumn("merchant", F.when(F.col("r") < 0.8, F.lit("m_hot")).otherwise(F.concat(F.lit("m"), (F.col("id") % 99).cast("string"))))
      .withColumn("amt", F.col("id") % 50).drop("r"))

def per_part(d, label):
    rows = d.withColumn("p", F.spark_partition_id()).groupBy("p").count().orderBy("p").collect()
    print(f"{label:34s}", {r["p"]: r["count"] for r in rows})

per_part(df.repartition(4, "merchant"), "repartition by merchant (hash)")
# salting: spread the hot key over 8 salt values, aggregate partially, then combine
SALTS = 8
salted = df.withColumn("salt", (F.rand(7) * SALTS).cast("int")).withColumn("skey", F.concat_ws("#", "merchant", "salt"))
per_part(salted.repartition(4, "skey"), "repartition by merchant#salt")

t = salted.groupBy("merchant", "salt").agg(F.count("*").alias("c"), F.sum("amt").alias("s"))
two_stage = t.groupBy("merchant").agg(F.sum("c").alias("count"), F.sum("s").alias("sum_amt")).orderBy(F.desc("count")).limit(3).collect()
direct = df.groupBy("merchant").agg(F.count("*").alias("count"), F.sum("amt").alias("sum_amt")).orderBy(F.desc("count")).limit(3).collect()
print("salted two-stage top3:", [tuple(r) for r in two_stage])
print("plain groupBy   top3:", [tuple(r) for r in direct])
print("same answer:", [tuple(r) for r in two_stage] == [tuple(r) for r in direct])

# broadcast the small side of a join instead of shuffling the big skewed side
dim = spark.createDataFrame([(f"m{i}", i % 5) for i in range(99)] + [("m_hot", 9)], "merchant string, category int")
j = df.join(F.broadcast(dim), "merchant")
print("broadcast join plan has BroadcastHashJoin:", "BroadcastHashJoin" in j._jdf.queryExecution().executedPlan().toString())
print("joined rows:", j.count())
print("defaults:", {k: spark.conf.get(k) for k in ("spark.sql.adaptive.skewJoin.enabled", "spark.sql.adaptive.skewJoin.skewedPartitionFactor")})
spark.stop(); shutil.rmtree(W, ignore_errors=True)
