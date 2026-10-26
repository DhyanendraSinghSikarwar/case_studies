# Q5: lazy evaluation and the shuffle (Exchange) node, PySpark local[2]. Own warehouse and local dir.
import sys, io, contextlib
from pyspark.sql import SparkSession, functions as F
from pyspark.sql.types import BooleanType
base = sys.argv[1]
spark = (SparkSession.builder.master("local[2]").appName("q05")
         .config("spark.ui.enabled", "false").config("spark.sql.shuffle.partitions", "4")
         .config("spark.sql.adaptive.enabled", "false")
         .config("spark.local.dir", base + "/local").config("spark.sql.warehouse.dir", base + "/wh").getOrCreate())
spark.sparkContext.setLogLevel("ERROR")
print("spark", spark.version)

calls = spark.sparkContext.accumulator(0)          # counts how many rows the Python filter really saw
def keep(x): calls.add(1); return x % 2 == 0
keep_udf = F.udf(keep, BooleanType())

df = spark.range(0, 1000, numPartitions=2)                       # transformation: nothing runs
df2 = df.withColumn("k", F.col("id") % 5)                        # transformation
df3 = df2.filter(keep_udf("id"))                                 # transformation
agg = df3.groupBy("k").agg(F.count("*").alias("n"), F.sum("id").alias("s")).orderBy("k")   # wide: needs a shuffle
print("partitions of input:", df.rdd.getNumPartitions())
print("after building the pipeline, rows the filter has seen:", calls.value, "  <- nothing ran")

buf = io.StringIO()
with contextlib.redirect_stdout(buf): agg.explain()
plan = buf.getvalue()
print("\n--- explain() ---"); print(plan.strip())
print("--- lines with Exchange:", [l.strip() for l in plan.splitlines() if "Exchange" in l])

rows = agg.collect()                                              # ACTION: now it runs
print("\nafter collect(), rows the filter has seen:", calls.value)
print(rows)
spark.stop()
