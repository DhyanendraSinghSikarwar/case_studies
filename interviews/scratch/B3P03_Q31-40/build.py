import re, subprocess, textwrap, sys
BASE = "/home/user/case_studies/interviews/scratch/B3P03_Q31-40"
PART = "/home/user/case_studies/interviews/Book3_SQL/Book3_SQL_Part03.md"
part = open(PART).read()
blocks = []
for n in range(31, 41):
    m = re.search(r"^(### Q%d .*)\n(\*\*Asked at:\*\*.*)\n" % n, part, re.M)
    assert m, n
    head, asked = m.group(1), m.group(2)
    code = open("%s/src/q%d.py" % (BASE, n)).read()
    out = subprocess.run(["python3", "-I", "%s/src/q%d.py" % (BASE, n)], capture_output=True, text=True, cwd="/tmp")
    assert out.returncode == 0, (n, out.stderr)
    body = open("%s/bodies/q%d.md" % (BASE, n)).read().rstrip("\n")
    def const(name):
        mm = re.search(r'^%s = """(.*?)"""' % name, code, re.S | re.M)
        assert mm, (n, name)
        return mm.group(1).strip("\n")
    def fence(lang, txt):
        assert "```" not in txt
        return "```%s\n%s\n```" % (lang, txt)
    body = re.sub(r"\{\{SQL:(\w+)\}\}", lambda m: fence("sql", const(m.group(1))), body)
    body = body.replace("{{SCHEMA}}", fence("sql", const("SCHEMA")) if "{{SCHEMA}}" in body else "")
    if "{{PD}}" in body:
        pm = re.search(r"# pd:main\n(.*?)# pd:end", code, re.S)
        pd_txt = textwrap.dedent(pm.group(1)).rstrip("\n")
        body = body.replace("{{PD}}", fence("py", pd_txt))
    body = body.replace("{{CODE}}", fence("python", code.rstrip("\n")))
    body = body.replace("{{OUT}}", fence("text", out.stdout.rstrip("\n")))
    assert "{{" not in body, n
    blocks.append("%s\n%s\n%s\n" % (head, asked, body))
open(BASE + "/answers.md", "w").write("\n".join(blocks))
print("built", len(blocks))
