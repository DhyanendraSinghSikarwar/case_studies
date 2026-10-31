import re, subprocess, os, sys
ROOT = "/home/user/case_studies/interviews"
PART = f"{ROOT}/Book4_MLOps/Book4_MLOps_Part10.md"
CODE = f"{ROOT}/scratch/B4P10_Q41-50/code"
PY = "/tmp/claude-0/b10p10/v/bin/python"
env = dict(os.environ, AWS_ACCESS_KEY_ID="testing", AWS_SECRET_ACCESS_KEY="testing", AWS_DEFAULT_REGION="us-east-1")
lines = open(PART).read().split("\n")
def head(n):
    for i, l in enumerate(lines):
        if l.startswith(f"### Q{n} "):
            assert lines[i+1].startswith("**Asked at:**"); return l + "\n" + lines[i+1]
    raise KeyError(n)
def run(script):
    r = subprocess.run([PY, "-I", f"{CODE}/{script}"], capture_output=True, text=True, env=env, cwd="/tmp/claude-0/b10_q41_50")
    assert r.returncode == 0, (script, r.stderr[-500:])
    return r.stdout.rstrip()
def build(n, tmpl, runs, codes):
    out = "\n\n".join(f"$ python3 -I {s}\n" + run(s) if len(runs) > 1 else run(s) for s in runs)
    code = {}
    for lang, files in codes.items():
        parts = []
        for f in files:
            body = open(f"{CODE}/{f}").read().rstrip()
            parts.append((f"# --- {f} ---\n" if len(files) > 1 and lang == "python" else "") + body)
        code[lang] = "\n\n".join(parts)
    blocks = "\n".join(f"```{('dockerfile' if l=='dockerfile' else l)}\n{c}\n```" for l, c in code.items())
    t = tmpl.strip("\n").replace("@@CODE@@", blocks).replace("@@OUT@@", "```text\n" + out + "\n```")
    return head(n) + "\n" + t
