"""Regenerate every figure and outputs/summary.json (stage 3). Thin wrapper over churnx.report."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from churnx.report import main  # noqa: E402

if __name__ == "__main__":
    main()
