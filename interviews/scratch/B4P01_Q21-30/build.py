import re, pathlib
ROOT = pathlib.Path(__file__).parent
part = pathlib.Path("/home/user/case_studies/interviews/Book4_MLOps/Book4_MLOps_Part01.md").read_text().splitlines()
def head(n):
    i = next(k for k, l in enumerate(part) if l.startswith(f"### Q{n} "))
    assert part[i + 1].startswith("**Asked at:**")
    return part[i] + "\n" + part[i + 1]
def rd(p): return (ROOT / "code" / p).read_text().rstrip("\n")
def files(lang, *ps, hdr="#"):
    out = []
    for p in ps:
        body = rd(p)
        out.append(f"{hdr} ===== file: {p.split('/')[-1]} =====\n{body}" if len(ps) > 1 else body)
    return f"```{lang}\n" + "\n\n".join(out) + "\n```"
def out(*ps): return "```text\n" + "\n\n".join(rd(p) for p in ps) + "\n```"
def sub(text):
    def r(m):
        kind, args = m.group(1), m.group(2).split("|")
        if kind == "PY": return files("python", *args)
        if kind == "SH": return files("bash", *args)
        if kind == "YAML": return files("yaml", *args)
        if kind == "OUT": return out(*args)
    return re.sub(r"\{\{(PY|SH|YAML|OUT):([^}]*)\}\}", r, text)
exec((ROOT / "texts.py").read_text())     # defines T = {21: "...", ...}
res = []
for n in range(21, 31):
    res.append(head(n) + "\n" + sub(T[n]).strip("\n") + "\n")
(ROOT / "answers.md").write_text("\n".join(res))
print("written", sum(len(x) for x in res), "chars")
