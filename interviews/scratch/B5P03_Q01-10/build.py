"""Assemble answers.md from the part file headings + text/qNN.md + code/qNN.py.
Runs every code file with python3 -I and pastes the real output. Safe to re-run."""
import re, subprocess, sys, pathlib, shutil

ROOT = pathlib.Path(__file__).resolve().parent
PART = ROOT.parent.parent / "Book5_DSA" / "Book5_DSA_Part03.md"
part = PART.read_text(encoding="utf-8")
out_parts, status = [], []
for n in range(1, 11):
    m = re.search(r"^### Q%d .*\n\*\*Asked at:\*\*.*\n" % n, part, re.M)
    assert m, n
    head = m.group(0).rstrip("\n")
    code = (ROOT / "code" / f"q{n:02d}.py").read_text(encoding="utf-8").rstrip("\n")
    r = subprocess.run([sys.executable, "-I", str(ROOT / "code" / f"q{n:02d}.py")],
                       capture_output=True, text=True, timeout=300, cwd=str(ROOT / "out"))
    ok = r.returncode == 0
    status.append((n, ok))
    if not ok:
        print(r.stderr)
    output = r.stdout.rstrip("\n")
    text = (ROOT / "text" / f"q{n:02d}.md").read_text(encoding="utf-8").rstrip("\n")
    assert "@@CODE@@" in text and "@@OUTPUT@@" in text, n
    text = text.replace("@@CODE@@", "```python\n" + code + "\n```")
    text = text.replace("@@OUTPUT@@", "```\n" + output + "\n```")
    out_parts.append(head + "\n\n" + text)
    (ROOT / "out" / f"q{n:02d}.out").write_text(output + "\n", encoding="utf-8")
(ROOT / "answers.md").write_text("\n\n".join(out_parts) + "\n", encoding="utf-8")
for p in ROOT.rglob("__pycache__"):
    shutil.rmtree(p, ignore_errors=True)
print("built answers.md;", ", ".join(f"Q{n}:{'ok' if ok else 'FAIL'}" for n, ok in status))
sys.exit(0 if all(ok for _, ok in status) else 1)
