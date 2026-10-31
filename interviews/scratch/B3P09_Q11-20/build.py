import re, subprocess, sys, pathlib
here = pathlib.Path(__file__).parent
part = (here.parent.parent / "Book3_SQL" / "Book3_SQL_Part09.md").read_text().splitlines()
def head(n):
    for i, l in enumerate(part):
        if l.startswith(f"### Q{n} "):
            return l, part[i+1]
    raise KeyError(n)
out = []
for n in range(11, 21):
    py = (here / f"q{n}.py").read_text()
    md = (here / f"q{n}.md").read_text().rstrip("\n")
    r = subprocess.run([sys.executable, "-I", str(here / f"q{n}.py")], capture_output=True, text=True, cwd="/tmp")
    if r.returncode:
        print(f"Q{n} FAILED\n", r.stderr); sys.exit(1)
    (here / f"q{n}.out").write_text(r.stdout)
    sql = re.search(r'SQL_MAIN = """\n(.*?)"""', py, re.S).group(1).rstrip("\n")
    m = re.search(r"# pd:main\n(.*?)\n[ \t]*# pd:end", py, re.S)
    pd_ = m.group(1)
    for name in re.findall(r"\{\{VAR:(\w+)\}\}", md):
        md = md.replace("{{VAR:%s}}" % name, re.search(name + r' = """\n(.*?)"""', py, re.S).group(1).rstrip("\n"))
    h, a = head(n)
    md = md.replace("{{SQL}}", sql).replace("{{PD}}", pd_).replace("{{CODE}}", py.rstrip("\n")).replace("{{OUT}}", r.stdout.rstrip("\n"))
    assert "```" not in sql + pd_ + py + r.stdout
    out.append(h + "\n" + a + "\n" + md)
(here / "answers.md").write_text("\n\n".join(out) + "\n")
print("built")
