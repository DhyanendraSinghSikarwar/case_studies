import sys; sys.path.insert(0, "/home/user/case_studies/interviews/scratch/B4P09_Q19-27/code")
from spark_common import get_spark
from pyspark.sql import functions as F
spark, _ = get_spark("q21")
print("pyspark", __import__("pyspark").__version__, "| AQE off for stable plans")

labels = spark.range(0, 20000).select((F.col("id") % 5000).alias("user_id"), (F.col("id") % 2).alias("label"))
feats  = spark.range(0, 5000).select(F.col("id").alias("user_id"), (F.col("id") * 3 % 100).alias("f_score"))
dim    = spark.createDataFrame([(i, f"seg{i%3}") for i in range(5)], ["bucket", "segment"])
labels = labels.withColumn("bucket", F.col("user_id") % 5)

def show(title, df):
    print("==", title)
    lines = df._jdf.queryExecution().executedPlan().toString().split("\n")
    for l in lines:
        if any(k in l for k in ("Join", "Exchange", "BroadcastExchange", "Sort", "Scan", "Range")):
            print(l.rstrip()[:110])

# A: large x small dim, broadcast hint
a = labels.join(F.broadcast(dim), "bucket")
show("A. large x small, broadcast() hint", a)
# B: same join, broadcast disabled and no hint
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", "-1")
b = labels.join(dim, "bucket")
show("B. large x small, autoBroadcastJoinThreshold=-1", b)
# C: large x large (both sides too big to broadcast): sort-merge
c = labels.join(feats, "user_id")
show("C. large x large, broadcast off", c)
# D: shuffle hash join by hint
d = labels.join(feats.hint("shuffle_hash"), "user_id")
show("D. large x large, hint shuffle_hash", d)
print("row counts equal across strategies (A,B):", a.count() == b.count(), a.count(), "| C,D:", c.count() == d.count(), c.count())
spark.stop()
