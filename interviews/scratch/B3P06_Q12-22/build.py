import re, subprocess, runpy, sys, os
W = os.path.dirname(os.path.abspath(__file__)) + "/w"
part = open("/home/user/case_studies/interviews/Book3_SQL/Book3_SQL_Part06.md", encoding="utf-8").read().split("\n")
heads = {}
for i, l in enumerate(part):
    m = re.match(r"### Q(\d+) ", l)
    if m: heads[int(m.group(1))] = (l, part[i + 1])
out = []
for n in range(12, 23):
    code = open(f"{W}/q{n}.py", encoding="utf-8").read()
    r = subprocess.run([sys.executable, "-I", f"{W}/q{n}.py"], capture_output=True, text=True, cwd="/tmp")
    assert r.returncode == 0, (n, r.stderr)
    g = runpy.run_path(f"{W}/q{n}.py") if False else None
    md = open(f"{W}/q{n}.md", encoding="utf-8").read()
    ns = {}
    # exec for variable access, output suppressed
    import io, contextlib
    with contextlib.redirect_stdout(io.StringIO()):
        ns = runpy.run_path(f"{W}/q{n}.py")
    def sql(m):
        return "```sql\n" + ns[m.group(1)].strip() + "\n```"
    md = re.sub(r"\{\{SQL:(\w+)\}\}", sql, md)
    def pd_(m):
        mm = re.search(r"# pd:%s\n(.*?)# pd:end" % m.group(1), code, re.S)
        return "```py\n" + mm.group(1).rstrip() + "\n```"
    md = re.sub(r"\{\{PD:(\w+)\}\}", pd_, md)
    md = md.replace("{{CODE}}", "```python\n" + code.rstrip() + "\n```")
    md = md.replace("{{OUT}}", "```text\n" + r.stdout.rstrip() + "\n```")
    h, a = heads[n]
    out.append(h + "\n" + a + "\n" + md.strip() + "\n")
open(os.path.dirname(W) + "/answers.md", "w", encoding="utf-8").write("\n".join(out))
print("built")
