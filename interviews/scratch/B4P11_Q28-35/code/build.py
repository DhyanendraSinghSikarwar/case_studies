# build.py - assemble answers.md: heading and Asked-at lines copied verbatim from the part file, bodies from bodies/, code/output spliced in.
import re, os
H = os.path.dirname(os.path.abspath(__file__))
part = open("/home/user/case_studies/interviews/Book4_MLOps/Book4_MLOps_Part11.md").read().split("\n")
OUT = "/tmp/claude-0/b11_q28_35/out/"
lang = {".py": "python", ".yaml": "yaml"}
def sub(m):
    kind, name = m.group(1), m.group(2)
    if kind == "OUT": return open(OUT + name).read().rstrip("\n")
    names = name.split(",")
    ext = os.path.splitext(names[0])[1]
    return f"```{lang[ext]}\n" + "\n\n".join(f"# ---- {x} ----\n" + open(f"{H}/{x}").read().rstrip("\n") for x in names) + "\n```"
res = []
for n in range(28, 36):
    i = next(k for k, l in enumerate(part) if l.startswith(f"### Q{n} "))
    assert part[i + 1].startswith("**Asked at:**")
    body = open(f"{H}/bodies/q{n}.md").read()
    body = re.sub(r"@@(CODE|OUT):([\w.,\-]+)@@", sub, body)
    res.append(part[i] + "\n" + part[i + 1] + "\n" + body.rstrip("\n") + "\n")
open(f"{H}/../answers.md", "w").write("\n".join(res))
