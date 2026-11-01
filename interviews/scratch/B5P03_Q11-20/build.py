"""Assemble answers.md from prose/qNN.md + code/qNN.py; re-runs every code file with python3 -I.
Headings and Asked-at lines are copied verbatim from the part file. Run: python3 build.py"""
import re, subprocess, sys, pathlib, shutil
here = pathlib.Path(__file__).resolve().parent
part = here.parents[1] / "Book5_DSA" / "Book5_DSA_Part03.md"
lines = part.read_text(encoding="utf-8").split("\n")
heads = {}
for i, ln in enumerate(lines):
    m = re.match(r"### Q(\d+) ", ln)
    if m:
        heads[int(m.group(1))] = (ln, lines[i + 1])
out, done, bad = [], [], []
for n in range(11, 21):
    prose = here / "prose" / f"q{n:02d}.md"
    code = here / "code" / f"q{n:02d}.py"
    if not (prose.exists() and code.exists()):
        continue
    r = subprocess.run([sys.executable, "-I", str(code)], capture_output=True, text=True, timeout=300)
    if r.returncode != 0:
        bad.append(n); print("FAIL", n, r.stderr[-400:]); continue
    body = prose.read_text(encoding="utf-8")
    body = body.replace("{{CODE}}", code.read_text(encoding="utf-8").rstrip("\n"))
    body = body.replace("{{OUTPUT}}", r.stdout.rstrip("\n"))
    h, a = heads[n]
    out.append(f"{h}\n{a}\n\n{body.strip()}\n")
    done.append(n)
(here / "answers.md").write_text("\n".join(out), encoding="utf-8")
print("built", done, "failed", bad)
for p in here.rglob("__pycache__"):
    shutil.rmtree(p, ignore_errors=True)
