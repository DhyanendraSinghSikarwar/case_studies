"""Assemble answers.md from qN.md templates + code/qN.py; re-run every code file with python3 -I.
Usage: python3 build.py   (run from anywhere)"""
import re, subprocess, sys, shutil
from pathlib import Path
HERE = Path(__file__).resolve().parent
PART = HERE.parent.parent / "Book5_DSA" / "Book5_DSA_Part04.md"
text = PART.read_text(encoding="utf-8").split("\n")
heads = {}
for i, ln in enumerate(text):
    m = re.match(r"### Q(\d+) ", ln)
    if m:
        heads[int(m.group(1))] = (ln, text[i + 1])
(HERE / "out").mkdir(exist_ok=True)
parts, done, failed = [], [], []
for n in range(11, 21):
    md, code = HERE / f"q{n}.md", HERE / "code" / f"q{n}.py"
    if not (md.exists() and code.exists()):
        continue
    r = subprocess.run([sys.executable, "-I", str(code)], capture_output=True, text=True, cwd=str(HERE / "code"))
    if r.returncode != 0:
        failed.append(n); print(f"Q{n} FAILED\n{r.stderr[-1500:]}"); continue
    (HERE / "out" / f"q{n}.out").write_text(r.stdout, encoding="utf-8")
    body = md.read_text(encoding="utf-8")
    body = body.replace("{{CODE}}", code.read_text(encoding="utf-8").rstrip("\n"))
    body = body.replace("{{OUTPUT}}", r.stdout.rstrip("\n"))
    h, asked = heads[n]
    assert asked.startswith("**Asked at:**")
    parts.append(f"{h}\n{asked}\n\n{body.strip()}\n")
    done.append(n)
(HERE / "answers.md").write_text("\n".join(parts), encoding="utf-8")
shutil.rmtree(HERE / "code" / "__pycache__", ignore_errors=True)
print("assembled:", done, "failed:", failed)
