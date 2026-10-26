import re, sys
PART = "/home/user/case_studies/interviews/Book4_MLOps/Book4_MLOps_Part08.md"
C = "/home/user/case_studies/interviews/scratch/B4P08_Q35-45/code/"
lines = open(PART, encoding="utf-8").read().split("\n")
head = {}
for i, l in enumerate(lines):
    m = re.match(r"### Q(\d+) ", l)
    if m: head[int(m.group(1))] = (l, lines[i + 1])
def rd(f): return open(C + f, encoding="utf-8").read().rstrip("\n")
def fence(lang, body): return "```%s\n%s\n```" % (lang, body)
def code(*blocks):  # blocks: (lang, [files])
    out = []
    for lang, files in blocks:
        body = "\n\n".join((("# --- %s ---\n" % f if len(files) > 1 else "") + rd(f)) for f in files)
        out.append(fence(lang, body))
    return "\n".join(out)
def out(*items):    # items: (label, file)
    return "\n".join(("`%s`\n" % lab if lab else "") + fence("text", rd(f)) for lab, f in items)

A = {}
exec(open("/home/user/case_studies/interviews/scratch/B4P08_Q35-45/answers_body.py", encoding="utf-8").read())
res = []
for q in range(35, 46):
    h, a = head[q]
    res.append("%s\n%s\n%s\n" % (h, a, A[q].strip("\n")))
open("/home/user/case_studies/interviews/scratch/B4P08_Q35-45/answers.md", "w", encoding="utf-8").write("\n".join(res))
print("written", len(res))
