import os, sys, time, json, shutil, tempfile
from datetime import datetime, timedelta, timezone
from pyspark.sql import SparkSession, functions as F

W = tempfile.mkdtemp(prefix="q13_", dir="/tmp/claude-0/b9_q10_18")
src = os.path.join(W, "src"); os.makedirs(src)
spark = (SparkSession.builder.master("local[2]").appName("q13")
         .config("spark.ui.enabled", "false").config("spark.ui.showConsoleProgress", "false").config("spark.sql.shuffle.partitions", "2")
         .config("spark.sql.session.timeZone", "UTC")
         .config("spark.local.dir", os.path.join(W, "local")).config("spark.sql.warehouse.dir", os.path.join(W, "wh"))
         .getOrCreate())
spark.sparkContext.setLogLevel("ERROR")

def drop(name, rows):
    with open(os.path.join(src, name), "w") as f:
        for ts, card in rows: f.write(json.dumps({"ts": ts, "card": card}) + "\n")

schema = "ts timestamp, card string"
df = spark.readStream.schema(schema).json(src)
agg = (df.withWatermark("ts", "1 minute").groupBy(F.window("ts", "1 minute")).count())
q = (agg.writeStream.outputMode("update").format("memory").queryName("win")
     .trigger(processingTime="1 second").start())

seen = 0
def show(label, wait_batches):
    global seen
    t0 = time.time()
    while time.time() - t0 < 30:
        time.sleep(0.5)
        got = [p for p in q.recentProgress if p["numInputRows"] > 0]
        if len(got) >= wait_batches: break
    time.sleep(2)                               # let the next empty batch advance the watermark
    got = [p for p in q.recentProgress if p["numInputRows"] > 0]
    p = got[-1]
    rows = spark.sql("select window.start as start, count from win").collect()
    new = rows[seen:]; seen = len(rows)
    print(f"[{label}]")
    print(f"   input rows={p['numInputRows']} max_event_time={p['eventTime'].get('max')} watermark_used={p['eventTime'].get('watermark')}")
    print("   update rows emitted this batch (window start, count):", [(r["start"].strftime("%H:%M"), r["count"]) for r in new])

drop("b1.json", [("2026-03-01T10:00:10", "c1"), ("2026-03-01T10:00:40", "c1"), ("2026-03-01T10:01:05", "c1")])
show("batch 1: three in-order events", 1)
drop("b2.json", [("2026-03-01T10:00:55", "c1"), ("2026-03-01T10:05:20", "c1")])
show("batch 2: 10:00:55 (late but inside watermark) and 10:05:20 (moves the clock)", 2)
drop("b3.json", [("2026-03-01T10:00:30", "c1"), ("2026-03-01T10:04:50", "c1")])
show("batch 3: 10:00:30 (behind watermark, dropped) and 10:04:50 (ahead of it, kept)", 3)
q.stop(); spark.stop(); shutil.rmtree(W, ignore_errors=True)
