import re, subprocess, pathlib
base = pathlib.Path("/home/user/case_studies/interviews")
part = (base / "Book3_SQL/Book3_SQL_Part02.md").read_text().splitlines()
here = pathlib.Path(__file__).parent
def head(n):
    for i, l in enumerate(part):
        if l.startswith(f"### Q{n} "):
            assert part[i+1].startswith("**Asked at:**")
            return l + "\n" + part[i+1]
    raise KeyError(n)
def run(n):
    f = here / "code" / f"q{n:02d}.py"
    r = subprocess.run(["python3", "-I", str(f)], capture_output=True, text=True, cwd="/tmp")
    assert r.returncode == 0, r.stderr
    return f.read_text().rstrip("\n"), r.stdout.rstrip("\n")
from prose import P
out = []
for n in range(1, 13):
    code, o = run(n)
    assert "```" not in code and "```" not in o
    body = P[n].replace("{CODE}", "```python\n" + code + "\n```").replace("{OUT}", "```text\n" + o + "\n```")
    out.append(head(n) + "\n" + body.strip("\n") + "\n")
(here / "answers.md").write_text("\n".join(out))
print("written", len(out))
