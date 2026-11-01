import re, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
part = pathlib.Path("/home/user/case_studies/interviews/Book4_MLOps/Book4_MLOps_Part06.md").read_text().splitlines()
lang = {"PY": "python", "YAML": "yaml", "PROTO": "protobuf"}
def expand(m):
    kind, files = m.group(1), m.group(2).split()
    parts = []
    for f in files:
        txt = (root / "code" / f).read_text().rstrip("\n")
        parts.append(f"# ===== {f} =====\n{txt}" if kind == "PY" else (f"# ===== {f} =====\n{txt}" if kind == "YAML" else f"// ===== {f} =====\n{txt}"))
    return f"```{lang[kind]}\n" + "\n\n".join(parts) + "\n```"
out = []
for n in range(1, 13):
    i = next(k for k, l in enumerate(part) if l.startswith(f"### Q{n} "))
    out.append(part[i]); out.append(part[i + 1]); assert part[i + 1].startswith("**Asked at:**")
    body = (root / "bodies" / f"q{n:02d}.md").read_text().rstrip("\n")
    out.append(re.sub(r"@@(\w+) ([^@]+)@@", expand, body)); out.append("\n---\n")
(root / "answers.md").write_text("\n".join(out))
