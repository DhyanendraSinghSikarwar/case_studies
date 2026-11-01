import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).parent))
from q44_serverless import Workload, choose
cases = {"small tabular model, spiky, lax latency": Workload(50, False, 0.5, 10, 2000, 600, 0.7),
         "image model 900 MB, low traffic": Workload(900, False, 1, 8, 3000, 1500, 0.5),
         "fraud scorer, strict p99, bursty": Workload(80, False, 2, 6, 150, 600, 0.2),
         "ranking model, steady 50 rps": Workload(200, False, 50, 2, 100, 400, 0.0),
         "large transformer needing GPU": Workload(4000, True, 3, 5, 800, 20000, 0.3)}
for n, w in cases.items():
    c, why = choose(w); print(f"{n:42s} -> {c}\n    {why[0]}")
