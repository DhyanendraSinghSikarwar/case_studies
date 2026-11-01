import re, os
ROOT = os.path.dirname(os.path.abspath(__file__))
PART = os.path.join(ROOT, "..", "..", "Book4_MLOps", "Book4_MLOps_Part02.md")
lines = open(PART, encoding="utf-8").read().split("\n")
heads = {}
for i, l in enumerate(lines):
    m = re.match(r"### Q(\d+) ", l)
    if m: heads[int(m.group(1))] = (l, lines[i + 1])
bodies = {}
cur = None
for l in open(os.path.join(ROOT, "bodies.md"), encoding="utf-8").read().split("\n"):
    m = re.match(r"=====Q(\d+)$", l)
    if m: cur = int(m.group(1)); bodies[cur] = []
    elif cur: bodies[cur].append(l)
def code(m):
    lang, files = m.group(1), m.group(2).split(",")
    parts = []
    for f in files:
        txt = open(os.path.join(ROOT, "code", f), encoding="utf-8").read().rstrip("\n")
        parts.append(txt if len(files) == 1 else f"# --- file: {os.path.basename(f)} ---\n{txt}")
    return f"```{lang}\n" + "\n\n".join(parts) + "\n```"
def out(m):
    txt = open(os.path.join(ROOT, "code", "out", m.group(1) + ".txt"), encoding="utf-8").read().rstrip("\n")
    return "```text\n" + txt + "\n```"
res = []
for q in range(24, 35):
    body = "\n".join(bodies[q]).strip("\n")
    body = re.sub(r"\{\{CODE:(\w+):([^}]+)\}\}", code, body)
    body = re.sub(r"\{\{OUT:(\w+)\}\}", out, body)
    # blank line around table blocks
    ls = body.split("\n"); fixed = []
    for i, l in enumerate(ls):
        is_t = l.startswith("|")
        prev_t = i > 0 and ls[i-1].startswith("|")
        if is_t and not prev_t and fixed and fixed[-1] != "": fixed.append("")
        if not is_t and prev_t and l != "": fixed.append("")
        fixed.append(l)
    body = "\n".join(fixed)
    res.append(heads[q][0] + "\n" + heads[q][1] + "\n" + body + "\n")
open(os.path.join(ROOT, "answers.md"), "w", encoding="utf-8").write("\n".join(res))
print("built", len(res))
