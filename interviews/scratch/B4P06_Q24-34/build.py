import re, sys, pathlib
ROOT = pathlib.Path("/home/user/case_studies/interviews")
part = (ROOT/"Book4_MLOps/Book4_MLOps_Part06.md").read_text().split("\n")
H = pathlib.Path(__file__).parent; C = H/"code"; O = pathlib.Path("/tmp/claude-0/b6_q24_34/out")
def head(n):
    for i, l in enumerate(part):
        if l.startswith(f"### Q{n} "): return l + "\n" + part[i+1]
def code(*names, lang="python"):
    parts = []
    for n in names:
        parts.append(f"# ===== {n} =====\n" + (C/n).read_text().rstrip())
    return f"```{lang}\n" + "\n\n".join(parts) + "\n```"
def sh(text): return "```bash\n" + text.strip() + "\n```"
def out(n): return "```text\n" + (O/n).read_text().rstrip() + "\n```"
sys.path.insert(0, str(H)); from bodies import BODIES
res = []
for n in range(24, 35):
    body = BODIES[n]({"code": code, "sh": sh, "out": out, "golden": (C/"golden_iris.json").read_text().strip()})
    res.append(head(n) + "\n" + body.strip() + "\n")
(H/"answers.md").write_text("\n".join(res))
print("ok", len("\n".join(res)))
