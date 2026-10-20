"""Cross-platform `make` replacement.

Usage: python tasks.py <setup|data|train|evaluate|app|test|lint|all>
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PY = sys.executable

TASKS: dict[str, list[list[str]]] = {
    "setup": [[PY, "-m", "pip", "install", "-r", "requirements.txt"],
              [PY, "-m", "pip", "install", "-e", ".", "--no-deps"]],
    "data": [[PY, "-m", "crm.data"]],
    "train": [[PY, "-m", "crm.train"]],
    "evaluate": [[PY, "analysis/run_analysis.py"]],
    "app": [[PY, "-m", "streamlit", "run", "app/streamlit_app.py"]],
    "test": [[PY, "-m", "pytest", "-q"]],
    "lint": [[PY, "-m", "ruff", "check", "."]],
}
TASKS["all"] = TASKS["data"] + TASKS["train"] + TASKS["evaluate"] + TASKS["lint"] + TASKS["test"]


def run(name: str) -> int:
    """Run a named task list; return the first non-zero exit code."""
    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT / "src") + os.pathsep + env.get("PYTHONPATH", "")
    env.setdefault("PYTHONWARNINGS", "ignore")
    for cmd in TASKS[name]:
        print(">>", " ".join(cmd), flush=True)
        code = subprocess.call(cmd, cwd=ROOT, env=env)
        if code != 0:
            return code
    return 0


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "all"
    if target not in TASKS:
        sys.exit(f"unknown task {target!r}; choose from {sorted(TASKS)}")
    sys.exit(run(target))
