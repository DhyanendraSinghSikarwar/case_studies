import re, pathlib, subprocess, sys
root = pathlib.Path(__file__).resolve().parent
part = (root.parent.parent / "Book4_MLOps/Book4_MLOps_Part12.md").read_text().splitlines()
def block(n):
    for i, l in enumerate(part):
        if l.startswith(f"### Q{n} "):
            assert part[i + 1].startswith("**Asked at:**"); return l, part[i + 1]
fence = {"CODE": "python", "OUT": "text", "YAML": "yaml"}
out = ["# Book 4 Part 12, Q23-Q33 answers (Wave B)\n"]
for n in range(23, 34):
    h, a = block(n)
    body = (root / "parts" / f"q{n}.md").read_text()
    def sub(m):
        kind, f = m.group(1), m.group(2)
        txt = (root / "code" / f).read_text().rstrip("\n")
        return f"```{fence[kind]}\n{txt}\n```"
    body = re.sub(r"@@(CODE|OUT|YAML):([^@]+)@@", sub, body)
    out.append(h + "\n" + a + "\n" + body.rstrip() + "\n")
(root / "answers.md").write_text("\n".join(out))
