import re, pathlib
HERE = pathlib.Path(__file__).parent
part = (HERE / "../../Book4_MLOps/Book4_MLOps_Part05.md").read_text().splitlines()
heads = {}
for i, l in enumerate(part):
    m = re.match(r"### Q(\d+) ", l)
    if m:
        n = int(m.group(1))
        asked = next(x for x in part[i+1:i+4] if x.startswith("**Asked at:**"))
        heads[n] = (l, asked)

def fence(lang, text):
    return f"```{lang}\n{text.rstrip()}\n```"

def expand(line):
    m = re.match(r"@@(PY|SH|YAML|OUT) (.+)$", line)
    if not m:
        return line
    kind, files = m.group(1), m.group(2).split()
    parts = []
    for f in files:
        t = (HERE / "code" / f).read_text()
        if kind in ("PY", "SH", "YAML") and len(files) > 1:
            c = "#" if kind != "YAML" else "#"
            t = f"{c} ---- file: {f} ----\n{t.rstrip()}\n"
        parts.append(t)
    lang = {"PY": "python", "SH": "bash", "YAML": "yaml", "OUT": "text"}[kind]
    return fence(lang, "\n".join(parts))

out = ["# Book 4 Part 5, Q11-Q20 answers (Wave B)", ""]
for n in range(11, 21):
    h, a = heads[n]
    body = (HERE / "bodies" / f"q{n}.md").read_text().splitlines()
    out += [h, a] + [expand(l) for l in body] + [""]
(HERE / "answers.md").write_text("\n".join(out))
print("built", len(out))
