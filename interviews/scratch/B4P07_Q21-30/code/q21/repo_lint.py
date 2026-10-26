"""Repository linter: required files, versioned gate thresholds, no secret-like strings in workflows."""
import re
import sys
from pathlib import Path

import yaml

REQUIRED = [
    ".github/workflows/ci.yml",
    "Dockerfile",
    "configs/gates.yaml",
    "serving/deployment.yaml",
    "CODEOWNERS",
]
REQUIRED_GATE_KEYS = {"min_auc", "max_auc_drop", "max_p95_ms"}
SECRET_PATTERNS = [
    re.compile(r"AKIA[0-9A-Z]{16}"),                       # AWS access key id shape
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),                   # GitHub token shape
    re.compile(r"(?i)(password|secret|token|api[_-]?key)\s*[:=]\s*['\"]?[A-Za-z0-9/+_\-]{12,}"),
]


def lint(root):
    root = Path(root)
    problems = []
    for rel in REQUIRED:
        if not (root / rel).is_file():
            problems.append(f"missing required file: {rel}")
    gates = root / "configs/gates.yaml"
    if gates.is_file():
        data = yaml.safe_load(gates.read_text()) or {}
        missing = REQUIRED_GATE_KEYS - set(data)
        if missing:
            problems.append(f"configs/gates.yaml missing keys: {sorted(missing)}")
    wf_dir = root / ".github/workflows"
    for wf in sorted(wf_dir.glob("*.yml")) if wf_dir.is_dir() else []:
        text = wf.read_text()
        for n, line in enumerate(text.splitlines(), 1):
            if "${{ secrets." in line:
                continue  # a reference, not a value
            if any(p.search(line) for p in SECRET_PATTERNS):
                problems.append(f"{wf.relative_to(root)}:{n}: secret-like string")
            # thresholds hard-coded in the workflow instead of configs/gates.yaml
            if re.search(r"(?i)(min_auc|max_auc_drop|--threshold)\s*[=: ]\s*0?\.\d+", line):
                problems.append(f"{wf.relative_to(root)}:{n}: gate threshold hard-coded in workflow")
    return problems


if __name__ == "__main__":
    probs = lint(sys.argv[1])
    for p in probs:
        print("FAIL", p)
    print("result:", "FAIL" if probs else "PASS", f"({len(probs)} problem(s))")
    sys.exit(1 if probs else 0)
