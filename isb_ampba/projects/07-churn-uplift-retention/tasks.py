"""Cross-platform task runner (make alternative).

Usage: python tasks.py <setup|data|train|evaluate|app|test|lint|all>
No venv/install needed: PYTHONPATH is pointed at ./src.
"""
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PY = sys.executable
TASKS = {
    "setup": [f"{PY} -m pip install -r requirements.txt", f"{PY} -m pip install -e ."],
    "data": [f"{PY} -m churnx.data"],
    "train": [f"{PY} -m churnx.train"],
    "evaluate": [f"{PY} analysis/run_analysis.py"],
    "app": [f"{PY} -m streamlit run app/streamlit_app.py"],
    "test": [f"{PY} -m pytest -q"],
    "lint": [f"{PY} -m ruff check ."],
}
TASKS["all"] = TASKS["data"] + TASKS["train"] + TASKS["evaluate"] + TASKS["lint"] + TASKS["test"]


def main(name: str) -> int:
    """Run the commands of one task; stop at the first failure."""
    env = {**os.environ, "PYTHONPATH": str(ROOT / "src") + os.pathsep + os.environ.get("PYTHONPATH", "")}
    for cmd in TASKS[name]:
        print(">>", cmd, flush=True)
        if subprocess.call(cmd, shell=True, cwd=ROOT, env=env) != 0:
            return 1
    return 0


if __name__ == "__main__":
    task = sys.argv[1] if len(sys.argv) > 1 else "all"
    if task not in TASKS:
        sys.exit(f"unknown task {task}; choose from {sorted(TASKS)}")
    sys.exit(main(task))
