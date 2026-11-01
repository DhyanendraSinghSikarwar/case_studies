import re, subprocess, sys, io, contextlib
W = "/home/user/case_studies/interviews/scratch/B3P07_Q31-40/w/"
PART = "/home/user/case_studies/interviews/Book3_SQL/Book3_SQL_Part07.md"
OUT = "/home/user/case_studies/interviews/scratch/B3P07_Q31-40/answers.md"
part = open(PART).read().split("\n")
def head(n):
    for i, l in enumerate(part):
        if l.startswith("### Q%d " % n):
            assert part[i+1].startswith("**Asked at:**")
            return l, part[i+1]
    raise KeyError(n)
parts = []
for n in range(31, 41):
    src = open(W + "q%d.py" % n).read()
    run = subprocess.run(["python3", "-I", W + "q%d.py" % n], capture_output=True, text=True, cwd="/tmp")
    assert run.returncode == 0, (n, run.stderr)
    ns = {"__name__": "x"}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(src, "q%d" % n, "exec"), ns)
    tpl = open(W + "q%d.tpl" % n).read()
    def sub(m):
        k = m.group(1)
        if k == "SCHEMA": return "```sql\n" + ns["SCHEMA"].strip() + "\n```"
        if k == "CODE": return "```python\n" + src.rstrip("\n") + "\n```"
        if k == "OUTPUT": return "```text\n" + run.stdout.rstrip("\n") + "\n```"
        if k == "PD":
            a = src.index("# pd:main\n") + len("# pd:main\n"); b = src.index("# pd:end")
            return "```py\n" + src[a:b].rstrip("\n") + "\n```"
        if k.startswith("SQL:"):
            return "```sql\n" + ns[k[4:]].strip() + "\n```"
        raise KeyError(k)
    body = re.sub(r"\{\{([A-Za-z_:0-9]+)\}\}", sub, tpl)
    h, a = head(n)
    parts.append(h + "\n" + a + "\n" + body.strip() + "\n")
open(OUT, "w").write("\n".join(parts))
print("written", len(parts))
