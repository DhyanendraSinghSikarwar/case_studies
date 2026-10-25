import re, subprocess, sys, pathlib
W = pathlib.Path(__file__).parent / "work"
PART = pathlib.Path("/home/user/case_studies/interviews/Book3_SQL/Book3_SQL_Part09.md").read_text().split("\n")
def head(n):
    for i, l in enumerate(PART):
        if l.startswith(f"### Q{n} "):
            assert PART[i+1].startswith("**Asked at:**")
            return l + "\n" + PART[i+1]
out = []
N=int(sys.argv[1]) if len(sys.argv)>1 else 10
for n in range(1, N+1):
    code = (W / f"q{n:02d}.py").read_text().rstrip("\n")
    r = subprocess.run([sys.executable, "-I", str(W / f"q{n:02d}.py")], capture_output=True, text=True)
    if r.returncode != 0:
        print(f"Q{n} FAILED\n{r.stdout[-1500:]}\n{r.stderr[-2500:]}"); sys.exit(1)
    prose = (W / f"q{n:02d}.md").read_text().rstrip("\n")
    def sql(m):
        mm = re.search(r'^%s = """\n?(.*?)"""' % m.group(1), code, re.S | re.M)
        return mm.group(1).strip("\n")
    prose = re.sub(r"\{\{SQL:(\w+)\}\}", sql, prose)
    mm = re.search(r"# pd:main\n(.*?)# pd:end", code, re.S)
    prose = prose.replace("{{PD}}", mm.group(1).rstrip("\n") if mm else "NO_PD")
    prose = prose.replace("{{CODE}}", code).replace("{{OUT}}", r.stdout.rstrip("\n"))
    out.append(head(n) + "\n" + prose)
text = "\n\n".join(out) + "\n"
assert "```" not in re.sub(r"```(sql|py|python|text)\n.*?\n```", "", text, flags=re.S), "stray fence"
(W.parent / "answers.md").write_text(text)
print("built", len(text), "chars")
