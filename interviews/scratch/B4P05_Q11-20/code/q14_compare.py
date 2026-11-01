"""Same 3-step pipeline in four tools: load each declaration for real where the tool is installed,
count code lines, and note how dependencies are declared."""
import ast
import pathlib
import subprocess
import sys

BASE = pathlib.Path(__file__).parent / "q14"
VENV = "/tmp/claude-0/b5p05"
rows = [
    ("Airflow 3", "af_pipe.py", f"{VENV}/af/bin/python",
     "import runpy; ns=runpy.run_path('{f}'); print('ok')", "data-flow in function calls (TaskFlow)"),
    ("Prefect 3", "pf_pipe.py", f"{VENV}/pf/bin/python",
     "import runpy; ns=runpy.run_path('{f}'); print('ok, flow =', ns['ml_pipe'].name)", "plain function calls inside a flow"),
    ("KFP 2", "kfp_pipe.py", f"{VENV}/kf/bin/python",
     "import runpy; from kfp import compiler; ns=runpy.run_path('{f}'); compiler.Compiler().compile(ns['ml_pipe'], '/tmp/claude-0/b5p05_q11_20/q14.yaml'); print('compiled')",
     ".output of one step passed into the next"),
    ("Dagster", "dagster_pipe.py.txt", None, None, "asset names as function arguments"),
]
print(f"{'tool':10} {'code lines':>10} {'decorators':>10}  {'loaded/compiled':18} dependency style")
for tool, fname, py, snippet, style in rows:
    src = (BASE / fname).read_text()
    lines = [l for l in src.splitlines() if l.strip() and not l.strip().startswith("#")]
    deco = sum(1 for l in lines if l.lstrip().startswith("@"))
    if py:
        r = subprocess.run([py, "-I", "-c", snippet.format(f=BASE / fname)], capture_output=True, text=True)
        status = r.stdout.strip().splitlines()[-1] if r.returncode == 0 and r.stdout.strip() else f"FAILED rc={r.returncode}"
    else:
        status = "not executed"
    print(f"{tool:10} {len(lines):>10} {deco:>10}  {status[:18]:18} {style}")
