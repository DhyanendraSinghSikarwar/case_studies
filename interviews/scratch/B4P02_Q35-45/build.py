import os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); CODE = os.path.join(HERE, "code")
PART = "/home/user/case_studies/interviews/Book4_MLOps/Book4_MLOps_Part02.md"
sys.path.insert(0, HERE)
A = {}
import build_part1, build_part2
A.update(build_part1.A); A.update(build_part2.A)

def heads():
    out, lines = {}, open(PART, encoding="utf-8").read().split("\n")
    for i, l in enumerate(lines):
        m = re.match(r"### Q(\d+) ", l)
        if m and 35 <= int(m.group(1)) <= 45:
            assert lines[i+1].startswith("**Asked at:**")
            out[int(m.group(1))] = (l, lines[i+1])
    return out

def fence(lang, files):
    parts = []
    for f in files:
        body = open(os.path.join(CODE, f)).read().rstrip("\n")
        parts.append(f"# ===== {f.split('/', 1)[1]} =====\n{body}")
    return f"```{lang}\n" + "\n\n".join(parts) + "\n```"

def sanitize(s):
    s = re.sub(r"\x1b\[[0-9;]*m", "", s)
    return s.replace(CODE, "<code>").replace("/tmp/claude-0/v35/bin/", "").replace("/tmp/claude-0/", "/tmp/")

def run(spec):
    d, cmds = spec.split("|", 1)
    out = []
    for c in cmds.split("||"):
        r = subprocess.run(["bash", "-c", c], cwd=os.path.join(CODE, d), capture_output=True, text=True, timeout=200,
                           env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
        out.append("$ " + sanitize(c) + "\n" + sanitize((r.stdout + r.stderr).rstrip("\n")))
    return "```text\n" + "\n\n".join(out) + "\n```\n"

def expand(t):
    t = re.sub(r"@@F:(\w+):([^@]+)@@", lambda m: fence(m.group(1), m.group(2).split(",")), t)
    t = re.sub(r"@@R:([^@]+)@@", lambda m: run(m.group(1)), t)
    return t

h = heads(); res = []
for q in range(35, 46):
    res.append(h[q][0] + "\n" + h[q][1] + "\n" + expand(A[q]).strip() + "\n")
open(os.path.join(HERE, "answers.md"), "w").write("\n".join(res))
print("written", len(res))
