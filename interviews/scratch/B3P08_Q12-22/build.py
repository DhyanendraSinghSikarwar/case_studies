import re, subprocess, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
PART = "/home/user/case_studies/interviews/Book3_SQL/Book3_SQL_Part08.md"
part = open(PART, encoding="utf-8").read().split("\n")
def head(n):
    for i, l in enumerate(part):
        if l.startswith(f"### Q{n} "):
            assert part[i+1].startswith("**Asked at:**")
            return l, part[i+1]
    raise KeyError(n)
def const(src, name):
    m = re.search(r'^' + name + r' = """\n(.*?)"""', src, re.S | re.M)
    assert m, name
    return m.group(1).rstrip("\n")
def pdblock(src, name):
    m = re.search(r'^# pd:' + name + r'\n(.*?)^# pd:end', src, re.S | re.M)
    assert m, name
    return m.group(1).rstrip("\n")
out = []
for n in range(12, 23):
    py = open(f"{HERE}/q{n}.py", encoding="utf-8").read()
    md = open(f"{HERE}/q{n}.md", encoding="utf-8").read()
    run = subprocess.run([sys.executable, "-I", f"{HERE}/q{n}.py"], capture_output=True, text=True, cwd="/tmp")
    if run.returncode != 0:
        print(run.stdout, run.stderr); raise SystemExit(f"Q{n} failed")
    open(f"{HERE}/q{n}.out", "w").write(run.stdout)
    md = re.sub(r"\{\{SQL:(\w+)\}\}", lambda m: "```sql\n" + const(py, m.group(1)) + "\n```", md)
    md = re.sub(r"\{\{PD:(\w+)\}\}", lambda m: "```py\n" + pdblock(py, m.group(1)) + "\n```", md)
    md = md.replace("{{CODE}}", "```python\n" + py.rstrip("\n") + "\n```")
    md = md.replace("{{OUTPUT}}", "```text\n" + run.stdout.rstrip("\n") + "\n```")
    h, a = head(n)
    out.append(h + "\n" + a + "\n" + md.strip("\n") + "\n")
open(f"{HERE}/answers.md", "w", encoding="utf-8").write("\n".join(out))
print("built", len(out))
