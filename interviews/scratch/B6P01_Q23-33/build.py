import re, subprocess, sys, pathlib, shutil
here = pathlib.Path(__file__).resolve().parent
part = (here.parent.parent / "Book6_Scenarios" / "Book6_Scenarios_Part01.md").read_text(encoding="utf-8").splitlines()
out = []
missing = []
for n in range(23, 34):
    idx = next(i for i, l in enumerate(part) if l.startswith(f"### Q{n} "))
    head, asked = part[idx], part[idx + 1]
    assert asked.startswith("**Asked at:**")
    body_f, code_f = here / f"q{n}.md", here / f"q{n}.py"
    if not body_f.exists():
        missing.append(n); continue
    body = body_f.read_text(encoding="utf-8").strip()
    code = code_f.read_text(encoding="utf-8").rstrip()
    r = subprocess.run([sys.executable, "-I", str(code_f)], capture_output=True, text=True, cwd=str(here))
    if r.returncode != 0:
        print("CODE FAILED Q", n, r.stderr); sys.exit(1)
    body = body.replace("{{CODE}}", "```python\n" + code + "\n```").replace("{{OUTPUT}}", "```text\n" + r.stdout.rstrip() + "\n```")
    out.append(head + "\n" + asked + "\n" + body + "\n")
(here / "answers.md").write_text("\n".join(out), encoding="utf-8")
shutil.rmtree(here / "__pycache__", ignore_errors=True)
print("built", len(out), "missing", missing)
