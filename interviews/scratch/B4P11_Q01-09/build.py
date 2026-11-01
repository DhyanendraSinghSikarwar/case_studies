import re, subprocess, os
ROOT = "/home/user/case_studies/interviews"
part = open(f"{ROOT}/Book4_MLOps/Book4_MLOps_Part11.md").read()
heads = {}
for m in re.finditer(r"^(### Q(\d+) .*)\n(\*\*Asked at:\*\*.*)$", part, re.M):
    heads[int(m.group(2))] = (m.group(1), m.group(3))
here = f"{ROOT}/scratch/B4P11_Q01-09"
VENV = {"az": "/tmp/claude-0/b11p11/az/bin/python", "gcp": "/tmp/claude-0/b11p11/gcp/bin/python"}
tpl = open(f"{here}/template.md").read()
tpl = re.sub(r"@@HEAD (\d+)@@\n", lambda m: heads[int(m.group(1))][0] + "\n" + heads[int(m.group(1))][1] + "\n", tpl)
tpl = re.sub(r"@@CODE (\S+) (\S+)@@", lambda m: f"```{m.group(2)}\n# {m.group(1)}\n" + open(f"{here}/code/{m.group(1)}").read().rstrip() + "\n```", tpl)
os.makedirs("/tmp/claude-0/b11_q01_09", exist_ok=True)
def out(m):
    f, v = m.group(1), m.group(2)
    r = subprocess.run([VENV[v], "-I", f"{here}/code/{f}"], capture_output=True, text=True, cwd="/tmp/claude-0/b11_q01_09",
                       env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "MLFLOW_DISABLE_TELEMETRY": "true"})
    assert r.returncode == 0, (f, r.stderr[-500:])
    return "```\n" + r.stdout.rstrip() + "\n```"
tpl = re.sub(r"@@OUT (\S+) (\S+)@@", out, tpl)
open(f"{here}/answers.md", "w").write(tpl)
print("built", len(tpl))
