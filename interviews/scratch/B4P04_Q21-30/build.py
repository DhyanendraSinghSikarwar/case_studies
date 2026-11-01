import re, os
PART = "/home/user/case_studies/interviews/Book4_MLOps/Book4_MLOps_Part04.md"
HERE = os.path.dirname(os.path.abspath(__file__))
C = os.path.join(HERE, "code")
txt = open(PART, encoding="utf-8").read().splitlines()
def head(n):
    for i, l in enumerate(txt):
        if l.startswith(f"### Q{n} "):
            assert txt[i+1].startswith("**Asked at:**")
            return l + "\n" + txt[i+1]
    raise KeyError(n)
def rd(p, cut=None):
    s = open(os.path.join(C, p), encoding="utf-8").read().rstrip("\n")
    if cut:
        s = "\n".join((l[:cut] + " ...[line cut for the book]") if len(l) > cut else l for l in s.splitlines())
    return s
def code(spec):
    out = []
    for lang, files in spec:
        parts = []
        for f in files:
            body = rd(f)
            cm = "//" if lang == "json" else "#"
            parts.append(f"{cm} --- {f} ---\n{body}" if len(files) > 1 else body)
        out.append(f"```{lang}\n" + "\n\n".join(parts) + "\n```")
    return "\n".join(out)
def output(p, cut=230):
    return "```text\n" + rd(p, cut) + "\n```"
from bodies import B
res = ["# Book 4 Part 4, answers Q21-Q30 (Wave B agent output)\n"]
for n in range(21, 31):
    b = B[n]
    sec = [head(n),
           "**Say this first (1 line):** " + b["say"],
           "**Then explain:**\n" + b["explain"].strip("\n"),
           "**Example:** " + b["example"],
           "**Code:** " + b["codeintro"] + (("\n" + code(b["code"])) if b["code"] else ""),
           "**Output (my run):** " + b["outintro"] + "\n" + ("\n".join(output(o) for o in b["out"]) + ("\n" if b["out"] else "")) + (b["notexec"] if b.get("notexec") else ""),
           "**Follow-ups:**\n" + b["follow"].strip("\n"),
           "**Common mistakes:**\n" + b["mistakes"].strip("\n")]
    res.append("\n".join(sec) + "\n")
open(os.path.join(HERE, "answers.md"), "w", encoding="utf-8").write("\n".join(res))
