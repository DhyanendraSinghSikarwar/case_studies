# assemble.py: copies each heading and Asked-at line verbatim from the part file, appends the body with FILE/OUT placeholders resolved.
import re, pathlib
S = pathlib.Path(__file__).parent; code = S / "code"
part = pathlib.Path("/home/user/case_studies/interviews/Book4_MLOps/Book4_MLOps_Part06.md").read_text().splitlines()
out = []
for n in range(13, 24):
    i = next(k for k, l in enumerate(part) if re.match(rf"### Q{n} ", l))
    head, asked = part[i], part[i + 1]
    assert asked.startswith("**Asked at:**"), (n, asked[:30])
    body = (S / "bodies" / f"q{n}.md").read_text()
    def fil(m):
        names = m.group(1).split(",")
        if len(names) == 1: return (code / names[0]).read_text().rstrip("\n")
        return "\n\n".join(f"# ===== {nm} =====\n" + (code / nm).read_text().rstrip("\n") for nm in names)
    body = re.sub(r"\{\{FILE:([^}]+)\}\}", fil, body)
    body = re.sub(r"\{\{OUT:(q\d+)\}\}", lambda m: (code / m.group(1) / "out.txt").read_text().rstrip("\n"), body)
    out += [head, asked, body.rstrip("\n"), "", "---", ""]
(S / "answers.md").write_text("\n".join(out))
print("wrote", len(out), "lines")
