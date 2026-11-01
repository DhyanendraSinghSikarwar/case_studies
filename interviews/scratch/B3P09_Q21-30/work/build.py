import re, subprocess, sys
PART = "/home/user/case_studies/interviews/Book3_SQL/Book3_SQL_Part09.md"
OUT = "/home/user/case_studies/interviews/scratch/B3P09_Q21-30/answers.md"
W = "/home/user/case_studies/interviews/scratch/B3P09_Q21-30/work/"
lines = open(PART).read().split("\n")
def head(n):
    i = next(k for k, l in enumerate(lines) if l.startswith(f"### Q{n} "))
    assert lines[i + 1].startswith("**Asked at:**")
    return lines[i] + "\n" + lines[i + 1]
def const(src, name):
    m = re.search(r'^' + name + r' = """(.*?)"""', src, re.S | re.M)
    return m.group(1).strip("\n")
def pdblock(src):
    m = re.search(r'# pd:main\n(.*?)# pd:end', src, re.S)
    return m.group(1).rstrip("\n")
parts = []
for n in range(21, 31):
    src = open(W + f"q{n}.py").read()
    out = open(W + f"out{n}.txt").read().rstrip("\n")
    body = open(W + f"q{n}.md").read().strip("\n")
    def sub(m):
        kind, name = m.group(1), m.group(2)
        if kind == "SQL":
            return "```sql\n" + const(src, name) + "\n```"
        if kind == "PD":
            return "```py\n" + pdblock(src) + "\n```"
        if kind == "CODE":
            return "```python\n" + src.rstrip("\n") + "\n```"
        if kind == "OUT":
            return "```text\n" + out + "\n```"
        raise SystemExit("bad placeholder " + m.group(0))
    body = re.sub(r"\{\{(SQL|PD|CODE|OUT)(?::(\w+))?\}\}", sub, body)
    parts.append(head(n) + "\n" + body)
open(OUT, "w").write("\n\n".join(parts) + "\n")
print("written", len(parts))
