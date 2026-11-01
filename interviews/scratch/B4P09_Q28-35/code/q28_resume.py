"""Q28: Spark Structured Streaming resumes from a checkpoint. Run: python q28_resume.py <workdir>"""
import json, os, sys, shutil
from pyspark.sql import SparkSession, functions as F

work = sys.argv[1]
for d in ("in", "ckpt", "out", "warehouse", "local"):
    shutil.rmtree(f"{work}/{d}", ignore_errors=True)
os.makedirs(f"{work}/in")

spark = (SparkSession.builder.master("local[2]").appName("q28")
         .config("spark.ui.enabled", "false")
         .config("spark.sql.shuffle.partitions", "2")
         .config("spark.sql.warehouse.dir", f"{work}/warehouse")
         .config("spark.local.dir", f"{work}/local")
         .getOrCreate())
spark.sparkContext.setLogLevel("ERROR")

def drop_file(name, rows):
    with open(f"{work}/in/{name}.json", "w") as f:
        for k, v in rows:
            f.write(json.dumps({"user": k, "amount": v}) + "\n")

def process_batch(df, batch_id):
    # runs once per micro-batch; prints what THIS batch saw and the running state
    rows = sorted((r["user"], r["count"]) for r in df.collect())
    print(f"  batch_id={batch_id} updated running counts: {rows}")

def run_once(label):
    print(f"--- {label}")
    stream = (spark.readStream.schema("user string, amount int").json(f"{work}/in")
              .groupBy("user").count())
    q = (stream.writeStream.outputMode("update").foreachBatch(process_batch)
         .option("checkpointLocation", f"{work}/ckpt")
         .trigger(availableNow=True).start())
    q.awaitTermination()
    print(f"  checkpoint offsets files: {sorted(x for x in os.listdir(work + "/ckpt/offsets") if not x.startswith("."))}")

drop_file("f1", [("a", 10), ("a", 20), ("b", 5)])
run_once("run 1: file f1 (a,a,b)")
drop_file("f2", [("a", 1), ("c", 7)])
run_once("run 2 after restart: file f2 added (a,c); f1 must NOT be re-read")
run_once("run 3 after restart: no new files")
shutil.rmtree(f"{work}/ckpt")
run_once("run 4: checkpoint deleted, so everything is read again from scratch")
spark.stop()
