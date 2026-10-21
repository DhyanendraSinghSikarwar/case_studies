"""Consistency checks for the case-study book.

    python tools/check_book.py

For every case in case_studies/ it checks that:
  - README.md, a notebook, a deck, src/generate_data.py and src/build_presentation.py exist;
  - the notebook has been executed (every code cell has an execution count), has no error outputs and
    no stderr/warning streams;
  - no markdown cell contains placeholder text such as "TODO" or "(Written after";
  - the deck is newer than the notebook's figures or at least exists, and the outputs folder has figures and tables;
  - PROGRESS.md lists the case as COMPLETE.
It also checks the three files of final_summary/. Exit status is 1 if anything fails.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLACEHOLDERS = ("TODO", "(Written after", "TBD", "FIXME", "lorem ipsum")


def check_case(case: Path, progress: dict[str, str]) -> list[str]:
    problems: list[str] = []
    num = case.name[:2]
    for rel in ("README.md", "src/generate_data.py", "src/build_presentation.py", "notebooks/01_analysis.ipynb",
                "presentation/case_study_presentation.pptx"):
        if not (case / rel).exists():
            problems.append(f"missing {rel}")
    if not any((case / "outputs" / "figures").glob("*.png")):
        problems.append("no figures in outputs/figures")
    if not any((case / "outputs" / "tables").glob("*.csv")):
        problems.append("no tables in outputs/tables")
    nb_path = case / "notebooks" / "01_analysis.ipynb"
    if nb_path.exists():
        nb = json.loads(nb_path.read_text(encoding="utf8"))
        code = [c for c in nb["cells"] if c["cell_type"] == "code"]
        if any(c.get("execution_count") is None for c in code):
            problems.append("notebook has unexecuted code cells")
        if any(o.get("output_type") == "error" for c in code for o in c.get("outputs", [])):
            problems.append("notebook has error outputs")
        if any(o.get("output_type") == "stream" and o.get("name") == "stderr" for c in code for o in c.get("outputs", [])):
            problems.append("notebook has stderr/warning output")
        for i, c in enumerate(nb["cells"]):
            text = "".join(c["source"])
            if c["cell_type"] == "markdown" and any(p.lower() in text.lower() for p in PLACEHOLDERS):
                problems.append(f"placeholder text in markdown cell {i}")
    if progress.get(num) != "COMPLETE":
        problems.append(f"PROGRESS.md status is {progress.get(num, 'missing')!r}, not COMPLETE")
    return problems


def read_progress() -> dict[str, str]:
    status: dict[str, str] = {}
    for line in (ROOT / "PROGRESS.md").read_text(encoding="utf8").splitlines():
        m = re.match(r"\|\s*(\d{2})\s*\|[^|]*\|\s*([A-Z ]+?)\s*\|", line)
        if m:
            status[m.group(1)] = m.group(2).strip()
    return status


def main() -> int:
    progress = read_progress()
    failures = 0
    for case in sorted((ROOT / "case_studies").iterdir()):
        if not case.is_dir() or not re.match(r"\d{2}_", case.name):
            continue
        problems = check_case(case, progress)
        print(f"{'FAIL' if problems else 'ok  '} {case.name}")
        for p in problems:
            print(f"       - {p}")
        failures += bool(problems)
    for rel in ("final_summary/statistics_cheat_sheet.md", "final_summary/decision_framework.md", "final_summary/presentation/statistics_playbook.pptx"):
        ok = (ROOT / rel).exists()
        print(f"{'ok  ' if ok else 'FAIL'} {rel}")
        failures += not ok
    print(f"\n{failures} problem area(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
