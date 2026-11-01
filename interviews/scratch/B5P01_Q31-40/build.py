"""Assemble answers.md: heading + Asked-at copied verbatim from the part file, answer text from src/qNN.md,
{{CODE}} from code/qNN.py, {{OUTPUT}} = real output of `python3 -I code/qNN.py` run at build time."""
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PART = HERE.parents[1] / "Book5_DSA" / "Book5_DSA_Part01.md"
lines = PART.read_text(encoding="utf-8").split("\n")
out = ["# Book 5 Part 1: answers Q31-Q40 (Wave B)\n"]
done = []
for n in range(31, 41):
    src = HERE / "src" / f"q{n}.md"
    if not src.exists():
        continue
    idx = next(i for i, l in enumerate(lines) if l.startswith(f"### Q{n} "))
    heading, asked = lines[idx], lines[idx + 1]
    assert asked.startswith("**Asked at:**")
    code = (HERE / "code" / f"q{n}.py").read_text(encoding="utf-8").rstrip("\n")
    run = subprocess.run([sys.executable, "-I", f"q{n}.py"], cwd=HERE / "code", capture_output=True, text=True, timeout=300)
    assert run.returncode == 0, (n, run.stderr)
    body = src.read_text(encoding="utf-8").rstrip("\n")
    body = body.replace("{{CODE}}", "```python\n" + code + "\n```").replace("{{OUTPUT}}", "```text\n" + run.stdout.rstrip("\n") + "\n```")
    out.append(heading + "\n" + asked + "\n\n" + body + "\n\n---\n")
    done.append(n)
(HERE / "answers.md").write_text("\n".join(out), encoding="utf-8")
print("assembled", done)
