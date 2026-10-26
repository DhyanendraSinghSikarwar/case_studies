import re
ROOT = "/home/user/case_studies/interviews"
part = open(f"{ROOT}/Book3_SQL/Book3_SQL_Part11.md").read().split("\n")
def head(n):
    i = next(k for k, l in enumerate(part) if l.startswith(f"### Q{n} "))
    j = next(k for k in range(i, len(part)) if part[k].startswith("**Asked at:**"))
    return part[i] + "\n" + part[j]
def code(n): return open(f"{ROOT}/scratch/B3P11_Q28-35/code/q{n}.py").read().rstrip()
def out(n): return open(f"{ROOT}/scratch/B3P11_Q28-35/out/q{n}.txt").read().rstrip()
def s5():
    t = out(29); return t[t.index("/* S5 covering"):].rstrip()

P = {}
exec(open(f"{ROOT}/scratch/B3P11_Q28-35/prose.py").read())
blocks = []
for n in range(28, 36):
    p = P[n]
    p = p.replace("{{S5}}", s5() if n == 29 else "")
    body = p.replace("{{CODE}}", "```python\n" + code(n) + "\n```").replace("{{OUT}}", "```text\n" + out(n) + "\n```")
    blocks.append(head(n) + "\n" + body.strip() + "\n")
open(f"{ROOT}/scratch/B3P11_Q28-35/answers.md", "w").write("\n".join(blocks))
