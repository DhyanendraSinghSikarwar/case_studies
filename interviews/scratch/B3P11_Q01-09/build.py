import re, subprocess, sys, pathlib
root = pathlib.Path("/home/user/case_studies/interviews")
part = (root / "Book3_SQL/Book3_SQL_Part11.md").read_text().split("\n")
here = root / "scratch/B3P11_Q01-09"
out = []
for n in range(1, 10):
    i = next(k for k, l in enumerate(part) if l.startswith(f"### Q{n} "))
    head, asked = part[i], part[i + 1]
    assert asked.startswith("**Asked at:**")
    code = (here / f"code/q{n:02d}.py").read_text().rstrip("\n")
    res = subprocess.run(["python3", "-I", str(here / f"code/q{n:02d}.py")], capture_output=True, text=True, cwd="/tmp")
    assert res.returncode == 0, res.stderr
    o = res.stdout.rstrip("\n")
    t = (here / f"tpl/q{n:02d}.md").read_text().rstrip("\n")
    t = t.replace("{{CODE}}", "```python\n" + code + "\n```").replace("{{OUT}}", "```text\n" + o + "\n```")
    out.append("\n".join([head, asked, t]) + "\n")
(here / "answers.md").write_text("\n".join(out))
print("built")
