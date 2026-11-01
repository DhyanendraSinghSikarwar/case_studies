import re, subprocess, textwrap, importlib.util, sys
D = "/home/user/case_studies/interviews/scratch/B3P08_Q01-11/"
part = open("/home/user/case_studies/interviews/Book3_SQL/Book3_SQL_Part08.md", encoding="utf-8").read()
T = {}
for n in ("texts1", "texts2", "texts3"):
    spec = importlib.util.spec_from_file_location(n, D + n + ".py"); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); T.update(m.T)
out = []
for q in range(1, 12):
    blk = re.search(r"(?ms)^### Q%d .*?\n\*\*Asked at:\*\*[^\n]*\n" % q, part).group(0)
    code = open(D + "q%02d.py" % q, encoding="utf-8").read().rstrip("\n")
    res = subprocess.run(["python3", "-I", D + "q%02d.py" % q], capture_output=True, text=True, cwd="/tmp")
    assert res.returncode == 0, (q, res.stderr)
    o = res.stdout.rstrip("\n")
    pdm = re.search(r"(?ms)^[ \t]*# pd:main\n(.*?)^[ \t]*# pd:end", code)
    pd_txt = textwrap.dedent(pdm.group(1)).rstrip("\n")
    t = T[q]
    def sqlsub(mm):
        s = re.search(r'(?ms)^%s = """\n?(.*?)"""' % mm.group(1), code).group(1).strip("\n")
        return s
    t = re.sub(r"\{SQL:(\w+)\}", sqlsub, t)
    t = t.replace("{PD}", pd_txt).replace("{CODE}", code).replace("{OUT}", o)
    out.append(blk + t.rstrip("\n") + "\n")
open(D + "answers.md", "w", encoding="utf-8").write("\n".join(out))
print("built")
