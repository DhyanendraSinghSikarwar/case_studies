"""Builds answers.md: headings and Asked-at lines copied verbatim from the part file; bodies from A below; code/outputs pasted from files."""
import pathlib, re
ROOT = pathlib.Path(__file__).resolve().parents[2]
HERE = pathlib.Path(__file__).resolve().parent
part = (ROOT / "Book4_MLOps" / "Book4_MLOps_Part03.md").read_text().splitlines()
CODE = HERE / "code"

def fence(lang, parts):
    body = []
    for p in parts:
        t = (CODE / p).read_text().rstrip("\n")
        body.append(t if len(parts) == 1 else f"# ===== {p} =====\n{t}")
    return f"```{lang}\n" + "\n".join(body) + "\n```"

def fill(s):
    s = re.sub(r"\{\{YAML:([^}]*)\}\}", lambda m: fence("yaml", m.group(1).split(",")), s)
    s = re.sub(r"\{\{PY:([^}]*)\}\}", lambda m: fence("python", m.group(1).split(",")), s)
    s = re.sub(r"\{\{OUT:([^}]*)\}\}", lambda m: "```text\n" + "\n".join((CODE / "out" / f).read_text().rstrip("\n") for f in m.group(1).split(",")) + "\n```", s)
    return s

exec((HERE / "bodies.py").read_text())   # defines A = {31: "...", ...}
out = []
for n in range(31, 41):
    i = next(k for k, l in enumerate(part) if l.startswith(f"### Q{n} "))
    assert part[i + 1].startswith("**Asked at:**")
    out += [part[i], part[i + 1], fill(A[n]).strip(), "", "---", ""]
(HERE / "answers.md").write_text("\n".join(out))
print("written", len(out), "lines")
