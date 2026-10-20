"""Cross-platform task runner (make alternative): python tasks.py setup|data|train|evaluate|app|test|lint|all."""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PKG = "credit"
ENV = {**os.environ, "PYTHONPATH": str(ROOT / "src") + os.pathsep + str(ROOT)}


def sh(*cmd: str) -> None:
    """Run a command in the project root; abort on failure."""
    print("+", " ".join(cmd), flush=True)
    r = subprocess.run(cmd, cwd=ROOT, env=ENV)
    if r.returncode:
        sys.exit(r.returncode)


def setup() -> None:
    """Install pinned requirements and the package."""
    sh(sys.executable, "-m", "pip", "install", "-r", "requirements.txt")
    sh(sys.executable, "-m", "pip", "install", "-e", ".")


def data() -> None:
    """Load/cache the raw data and write the splits."""
    sh(sys.executable, "-m", f"{PKG}.data")


def train() -> None:
    """Train all models (writes models/ and outputs/metrics.json)."""
    sh(sys.executable, "-m", f"{PKG}.train")


def evaluate() -> None:
    """Regenerate every figure, CSV and outputs/summary.json."""
    sh(sys.executable, "analysis/run_analysis.py")


def app() -> None:
    """Launch the Streamlit app."""
    sh(sys.executable, "-m", "streamlit", "run", "app/streamlit_app.py")


def test() -> None:
    """Run the test-suite."""
    sh(sys.executable, "-m", "pytest", "-q")


def lint() -> None:
    """Ruff check."""
    sh(sys.executable, "-m", "ruff", "check", ".")


def all_() -> None:
    """lint, test, data, train, evaluate."""
    lint()
    test()
    data()
    train()
    evaluate()
    sh(sys.executable, "analysis/make_docs.py")


TASKS = {"setup": setup, "data": data, "train": train, "evaluate": evaluate, "app": app, "test": test,
         "lint": lint, "all": all_}

if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "all"
    if name not in TASKS:
        sys.exit(f"unknown task {name!r}; choose from {sorted(TASKS)}")
    TASKS[name]()
