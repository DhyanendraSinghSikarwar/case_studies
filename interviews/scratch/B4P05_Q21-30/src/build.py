"""Build answers.md: headings and Asked-at lines are copied verbatim from the part file; {{CODE}} and {{OUT}} pull real files."""
import re, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
PART = ROOT.parents[1] / "Book4_MLOps" / "Book4_MLOps_Part05.md"
lines = PART.read_text().splitlines()
heads = {}
for i, l in enumerate(lines):
    m = re.match(r"### (Q(\d+)) ", l)
    if m and 21 <= int(m.group(2)) <= 30:
        assert lines[i + 1].startswith("**Asked at:**")
        heads[m.group(1)] = (l, lines[i + 1])
bodies = dict(re.findall(r"@@(Q\d+)\n(.*?)(?=\n@@Q|\Z)", (ROOT / "src" / "bodies.md").read_text(), re.S))
assert sorted(heads) == sorted(bodies), (sorted(heads), sorted(bodies))
CODE = ROOT / "code"

def code(m):
    lang, files = m.group(1), m.group(2).split()
    out = []
    for f in files:
        t = (CODE / f).read_text().rstrip("\n")
        out.append(t if len(files) == 1 else f"# --- {f.split('/')[-1]} ---\n{t}")
    return f"```{lang}\n" + "\n\n".join(out) + "\n```"

def out(m):
    return "```text\n" + (CODE / m.group(1)).read_text().rstrip("\n") + "\n```"

res = []
for q in sorted(heads, key=lambda s: int(s[1:])):
    b = bodies[q].strip("\n")
    b = re.sub(r"\{\{CODE (\w+) ([^}]+)\}\}", code, b)
    b = re.sub(r"\{\{OUT ([^}]+)\}\}", out, b)
    res.append(heads[q][0] + "\n" + heads[q][1] + "\n" + b + "\n")
(ROOT / "answers.md").write_text("\n".join(res))
print("built", len(res), "answers")
