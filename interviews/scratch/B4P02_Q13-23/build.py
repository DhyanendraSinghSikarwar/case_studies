import re, os
C = "code/"
def rd(p): return open(C + p).read().rstrip("\n")
src = open("/home/user/case_studies/interviews/Book4_MLOps/Book4_MLOps_Part02.md").read()
blocks = {}
for m in re.finditer(r"^### Q(\d+) .*\n\*\*Asked at:\*\*.*$", src, re.M):
    blocks[int(m.group(1))] = m.group(0).split("\n")
def fence(lang, body): return f"```{lang}\n{body}\n```"
def out(*items):
    s = []
    for lab, f in items:
        s.append(f"$ {lab}" if lab else "")
        s.append(rd(f) if f.endswith(".out") or "/" in f else f)
    return fence("text", "\n".join(s).strip())

A = {}
exec(open("answers_text.py").read())
res = ["# Book 4 Part 2, Q13-Q23 answers (Wave B agent)\n"]
for n in range(13, 24):
    h, a = blocks[n]
    res.append(h); res.append(a); res.append(A[n].strip() + "\n")
open("answers.md", "w").write("\n".join(res))
print("written", len("\n".join(res)))
