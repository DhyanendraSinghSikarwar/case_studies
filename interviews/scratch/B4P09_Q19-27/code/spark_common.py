import os, sys, tempfile
from pyspark.sql import SparkSession

def get_spark(name, extra=None):
    os.environ["PYSPARK_PYTHON"] = sys.executable   # workers must use the venv python (has pyarrow)
    base = os.path.join("/tmp/claude-0/b9_q19_27/work", name)
    os.makedirs(base, exist_ok=True)
    b = (SparkSession.builder.master("local[2]").appName(name)
         .config("spark.ui.enabled", "false").config("spark.ui.showConsoleProgress", "false")
         .config("spark.sql.shuffle.partitions", "4")
         .config("spark.default.parallelism", "4")
         .config("spark.local.dir", os.path.join(base, "local"))
         .config("spark.sql.warehouse.dir", os.path.join(base, "warehouse"))
         .config("spark.driver.bindAddress", "127.0.0.1").config("spark.driver.host", "127.0.0.1")
         .config("spark.sql.adaptive.enabled", "false"))   # fixed plans for teaching; AQE can change them
    for k, v in (extra or {}).items(): b = b.config(k, v)
    s = b.getOrCreate(); s.sparkContext.setLogLevel("ERROR")
    return s, base
