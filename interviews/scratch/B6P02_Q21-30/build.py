import re, subprocess, sys, pathlib
here = pathlib.Path(__file__).resolve().parent
part = (here.parent.parent / "Book6_Scenarios" / "Book6_Scenarios_Part02.md").read_text().split("\n")
out_all = []
for n in range(21, 31):
    i = next(k for k, l in enumerate(part) if l.startswith(f"### Q{n} "))
    head = part[i]; asked = part[i + 1]
    assert asked.startswith("**Asked at:**")
    d = here / f"q{n}"
    code = (d / "code.py").read_text().rstrip("\n")
    r = subprocess.run([sys.executable, "-I", str(d / "code.py")], capture_output=True, text=True, cwd=d)
    assert r.returncode == 0, r.stderr
    (d / "out.txt").write_text(r.stdout)
    block = "\n".join([head, asked, (d / "a.md").read_text().rstrip("\n"), "```python", code, "```", "",
                       "**Output (my run):**", "```text", r.stdout.rstrip("\n"), "```", "",
                       (d / "b.md").read_text().rstrip("\n"), ""])
    (here / f"q{n}.md").write_text(block + "\n")
    out_all.append(block)
(here / "answers.md").write_text("\n".join(out_all))
print("built", len(out_all))
