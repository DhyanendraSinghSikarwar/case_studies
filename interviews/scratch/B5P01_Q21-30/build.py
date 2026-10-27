"""Assemble answers.md for Book 5 Part 1, Q21-Q30.
Runs every code/qNN.py with python3 -I and pastes the real output.
Headings and Asked-at lines are copied verbatim from the part file."""
import re, subprocess, sys, pathlib, shutil

here = pathlib.Path(__file__).resolve().parent
part = here.parents[1] / "Book5_DSA" / "Book5_DSA_Part01.md"
lines = part.read_text(encoding="utf-8").split("\n")
out = []
for q in range(21, 31):
    idx = next(i for i, l in enumerate(lines) if re.match(rf"### Q{q} ", l))
    heading, asked = lines[idx], lines[idx + 1]
    assert asked.startswith("**Asked at:**")
    code_path = here / "code" / f"q{q}.py"
    r = subprocess.run([sys.executable, "-I", str(code_path)], capture_output=True, text=True, timeout=300)
    assert r.returncode == 0, (q, r.stderr)
    body = (here / "bodies" / f"q{q}.md").read_text(encoding="utf-8")
    code = "```python\n" + code_path.read_text(encoding="utf-8").rstrip() + "\n```"
    output = "```\n" + r.stdout.rstrip() + "\n```"
    body = body.replace("@@CODE@@", code).replace("@@OUTPUT@@", output)
    out.append(f"{heading}\n{asked}\n{body.rstrip()}\n")
(here / "answers.md").write_text("\n".join(out), encoding="utf-8")
shutil.rmtree(here / "code" / "__pycache__", ignore_errors=True)
print("wrote answers.md", len(out))
