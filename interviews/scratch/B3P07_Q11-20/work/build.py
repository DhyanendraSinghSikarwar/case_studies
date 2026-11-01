import re, subprocess, sys, pathlib
W = pathlib.Path(__file__).parent
PART = W.parents[2] / "Book3_SQL" / "Book3_SQL_Part07.md"
lines = PART.read_text().split("\n")
def head(n):
    for i, l in enumerate(lines):
        if l.startswith(f"### Q{n} "):
            assert lines[i+1].startswith("**Asked at:**")
            return l + "\n" + lines[i+1]
    raise KeyError(n)
def triple(code, name):
    m = re.search(name + r' = """\n?(.*?)"""', code, re.S)
    assert m, name
    return m.group(1).strip("\n")
def pdblock(code, tag):
    m = re.search(r"# pd:%s\n(.*?)# pd:end" % tag, code, re.S)
    assert m, tag
    return m.group(1).rstrip("\n")
out = []
for n in range(11, 21):
    if not (W / f"q{n}.md").exists(): continue
    code = (W / f"q{n}.py").read_text().rstrip("\n")
    r = subprocess.run([sys.executable, "-I", str(W / f"q{n}.py")], capture_output=True, text=True, cwd="/tmp")
    assert r.returncode == 0, (n, r.stderr)
    tpl = (W / f"q{n}.md").read_text().rstrip("\n")
    tpl = tpl.replace("{{CODE}}", "```python\n" + code + "\n```").replace("{{OUTPUT}}", "```text\n" + r.stdout.rstrip("\n") + "\n```")
    tpl = re.sub(r"\{\{SQL:(\w+)\}\}", lambda m: triple(code, m.group(1)), tpl)
    tpl = re.sub(r"\{\{PD:(\w+)\}\}", lambda m: pdblock(code, m.group(1)), tpl)
    tpl = tpl.replace("{{SCHEMA}}", triple(code, "SCHEMA"))
    assert "{{" not in tpl, (n, re.findall(r"\{\{.*?\}\}", tpl))
    out.append(head(n) + "\n" + tpl)
(W.parent / "answers.md").write_text("\n\n".join(out) + "\n")
print("ok", len(out))
