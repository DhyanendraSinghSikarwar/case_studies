"""Cross-platform task runner (make alternative).

Usage: python tasks.py <setup|data|train|evaluate|app|test|lint|all>
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PY = sys.executable
TASKS = {
    "setup": [[PY, "-m", "pip", "install", "-r", "requirements.txt"]],
    "data": [[PY, "-m", "promo.data"]],
    "train": [[PY, "-m", "promo.train"]],
    "evaluate": [[PY, "analysis/run_analysis.py"]],
    "app": [[PY, "-m", "streamlit", "run", "app/streamlit_app.py"]],
    "test": [[PY, "-m", "pytest", "-q"]],
    "lint": [[PY, "-m", "ruff", "check", "."]],
}
TASKS["all"] = TASKS["data"] + TASKS["train"] + TASKS["evaluate"] + TASKS["test"] + TASKS["lint"]


def env() -> dict:
    """Environment with PYTHONPATH=src and an interim dir outside OneDrive when available."""
    e = dict(os.environ)
    e["PYTHONPATH"] = str(ROOT / "src") + os.pathsep + e.get("PYTHONPATH", "")
    if "AMPBA_INTERIM_DIR" not in e and Path("C:/ampba_data").exists():
        e["AMPBA_INTERIM_DIR"] = "C:/ampba_data/05_interim"
    return e


if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "all"
    if name not in TASKS:
        sys.exit(f"unknown task {name!r}; choose from {', '.join(TASKS)}")
    for cmd in TASKS[name]:
        print(">>", " ".join(cmd), flush=True)
        if subprocess.call(cmd, cwd=ROOT, env=env()) != 0:
            sys.exit(1)
