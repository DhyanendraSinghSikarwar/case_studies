import sys, time; sys.path.insert(0, "/home/user/case_studies/interviews/scratch/B4P09_Q19-27/code")
from spark_common import get_spark
from pyspark.sql import functions as F
from pyspark.sql.functions import udf, pandas_udf
from pyspark.sql.types import DoubleType
import pandas as pd

spark, _ = get_spark("q22", {"spark.sql.execution.arrow.maxRecordsPerBatch": "10000"})
print("pyspark", __import__("pyspark").__version__, "pandas", pd.__version__)
N = 400_000
df = spark.range(N).select(F.col("id"), ((F.col("id") * 7919) % 1000 / 10.0).alias("amount"))
# Feature: log-ish squash  amount / (amount + 50)
builtin = df.withColumn("f", F.col("amount") / (F.col("amount") + F.lit(50.0)))

def _f(x): return x / (x + 50.0)
py_udf = udf(_f, DoubleType(), useArrow=False)     # classic row-at-a-time pickled Python UDF
py_arrow_udf = udf(_f, DoubleType(), useArrow=True)  # Arrow-optimised Python UDF (default in recent Spark; check your version)

@pandas_udf(DoubleType())
def vec_udf(x: pd.Series) -> pd.Series: return x / (x + 50.0)

py = df.withColumn("f", py_udf("amount"))
vec = df.withColumn("f", vec_udf("amount"))
pya = df.withColumn("f", py_arrow_udf("amount"))

def bench(label, d):
    d.agg(F.sum("f")).collect()               # warm up (JVM + Python worker start)
    ts = []
    for _ in range(5):
        t = time.perf_counter(); r = d.agg(F.sum("f").alias("s"), F.count("f").alias("n")).collect()[0]
        ts.append(time.perf_counter() - t)
    dt = sorted(ts)[2]                        # median of 5
    return label, r["s"], r["n"], dt

res = [bench("built-in", builtin), bench("python udf (row)", py), bench("python udf (arrow)", pya), bench("pandas (arrow) udf", vec)]
base = res[0][1]
for label, s, n, dt in res:
    print(f"{label:21s} sum={s:.6f} n={n} match_builtin={abs(s-base)<1e-6} median_of_5={dt:.2f}s (sandbox only)")

def plan_lines(d, keys):
    for l in d._jdf.queryExecution().executedPlan().toString().split("\n"):
        if any(k in l for k in keys): print("  ", l.strip()[:120])
print("-- plan, built-in:");   plan_lines(builtin, ("Project", "Range"))
print("-- plan, python udf:"); plan_lines(py, ("EvalPython", "Project", "Range"))
print("-- plan, python udf (arrow):"); plan_lines(pya, ("EvalPython", "Project", "Range"))
print("-- plan, pandas udf:"); plan_lines(vec, ("EvalPython", "Project", "Range"))
spark.stop()
