import sys, os, glob, json, shutil; sys.path.insert(0, "/home/user/case_studies/interviews/scratch/B4P09_Q19-27/code")
from pyspark.sql import SparkSession, functions as F
from delta import configure_spark_with_delta_pip
import delta
base = "/tmp/claude-0/b9_q19_27/work/q23d"; os.makedirs(base, exist_ok=True)
os.environ["PYSPARK_PYTHON"] = sys.executable
b = (SparkSession.builder.master("local[2]").appName("q23d").config("spark.ui.enabled", "false")
     .config("spark.ui.showConsoleProgress", "false").config("spark.sql.shuffle.partitions", "4")
     .config("spark.local.dir", base + "/local").config("spark.sql.warehouse.dir", base + "/wh")
     .config("spark.driver.bindAddress", "127.0.0.1").config("spark.driver.host", "127.0.0.1")
     .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
     .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog"))
spark = configure_spark_with_delta_pip(b).getOrCreate(); spark.sparkContext.setLogLevel("ERROR")
print("pyspark", __import__("pyspark").__version__, "delta-spark", delta.__version__ if hasattr(delta, "__version__") else "see pip")
path = base + "/tbl"; shutil.rmtree(path, ignore_errors=True)
for i in range(4):   # four small appends = four commits of small files
    (spark.range(i * 500, (i + 1) * 500).select("id", (F.col("id") % 7).alias("f"))
          .repartition(3).write.format("delta").mode("append").save(path))
nf = lambda: len([f for f in glob.glob(path + "/*.parquet")])
print("after 4 appends: data files on disk =", nf(), "| log files =", sorted(os.path.basename(f) for f in glob.glob(path + "/_delta_log/*.json")))
spark.sql(f"OPTIMIZE delta.`{path}`").collect()
log = sorted(glob.glob(path + "/_delta_log/*.json"))[-1]
acts = [list(json.loads(l).keys())[0] for l in open(log)]
print("latest commit", os.path.basename(log), "actions:", {a: acts.count(a) for a in sorted(set(acts))})
live = spark.sql(f"DESCRIBE DETAIL delta.`{path}`").select("numFiles").first()[0]
print("live files after OPTIMIZE (numFiles) =", live, "| files still on disk (old ones await VACUUM) =", nf())
print("rows:", spark.read.format("delta").load(path).count(), "(expected 2000)")
spark.stop()
