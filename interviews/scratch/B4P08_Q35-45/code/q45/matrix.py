import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from monitors import MONITORS, clean_batch, inject
faults = ["none", "null_spike", "unit_change", "mean_shift", "dropped_partition"]
print(f"{'fault':18s}" + "".join(f"{m:>9s}" for m in MONITORS) + "   (fraction of 200 seeds where the monitor fired)")
for fault in faults:
    row = {m: 0 for m in MONITORS}
    for s in range(200):
        rng = np.random.default_rng(s)
        ref, cur = clean_batch(rng), inject(clean_batch(rng), fault, rng)
        for m, f in MONITORS.items(): row[m] += bool(f(ref, cur))
    print(f"{fault:18s}" + "".join(f"{row[m]/200:9.2f}" for m in MONITORS))
