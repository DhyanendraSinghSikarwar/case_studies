import re, subprocess, os, sys
ROOT = "/home/user/case_studies/interviews"
part = open(f"{ROOT}/Book4_MLOps/Book4_MLOps_Part10.md").read()
heads = {}
for m in re.finditer(r"^(### Q(\d+) .*)\n(\*\*Asked at:\*\*.*)$", part, re.M):
    heads[int(m.group(2))] = (m.group(1), m.group(3))
here = f"{ROOT}/scratch/B4P10_Q01-10"
py = "/tmp/claude-0/b10p10/v/bin/python"
tpl = open(f"{here}/template.md").read()
def sub_head(m):
    h, a = heads[int(m.group(1))]; return h + "\n" + a + "\n"
tpl = re.sub(r"@@HEAD (\d+)@@\n", sub_head, tpl)
def sub_code(m):
    f, lang = m.group(1), m.group(2)
    return f"```{lang}\n# {f}\n" + open(f"{here}/code/{f}").read().rstrip() + "\n```"
tpl = re.sub(r"@@CODE (\S+) (\S+)@@", sub_code, tpl)
def sub_out(m):
    f = m.group(1)
    r = subprocess.run([py, "-I", f"{here}/code/{f}"], capture_output=True, text=True, cwd="/tmp/claude-0/b10_q01_10", env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
    assert r.returncode == 0, (f, r.stderr)
    return "```\n" + r.stdout.rstrip() + "\n```"
tpl = re.sub(r"@@OUT (\S+)@@", sub_out, tpl)
open(f"{here}/answers.md", "w").write(tpl)
