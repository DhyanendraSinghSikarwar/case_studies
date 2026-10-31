import sys, pandas as pd, evidently
from evidently import Report
from evidently.presets import DataDriftPreset
ref = pd.read_csv(sys.argv[1] + "/ref.csv"); cur = pd.read_csv(sys.argv[1] + "/cur.csv")
print("evidently", evidently.__version__, "pandas", pd.__version__)
snap = Report([DataDriftPreset()]).run(cur, ref)
d = snap.dict()
for m in d["metrics"]:
    print(m["metric_name"], "->", m["value"])
snap.save_html(sys.argv[1] + "/drift.html")
import os; print("html written:", os.path.getsize(sys.argv[1] + "/drift.html") > 100000)
