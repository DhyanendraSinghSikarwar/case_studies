import subprocess, os, shutil, glob
ROOT = "/home/user/case_studies/interviews"
D = f"{ROOT}/scratch/B5P03_Q31-40"
part = open(f"{ROOT}/Book5_DSA/Book5_DSA_Part03.md", encoding="utf-8").read().split("\n")
def head(n):
    i = next(k for k, l in enumerate(part) if l.startswith(f"### Q{n} "))
    assert part[i + 1].startswith("**Asked at:**")
    return part[i], part[i + 1]
res, done = [], []
for n in range(31, 41):
    bf, cf = f"{D}/body/q{n}.md", f"{D}/code/q{n}.py"
    if not (os.path.exists(bf) and os.path.exists(cf)): continue
    r = subprocess.run(["python3", "-I", cf], capture_output=True, text=True, cwd=f"{D}/code")
    o = (r.stdout + r.stderr).strip()
    assert r.returncode == 0, (n, o)
    body = open(bf, encoding="utf-8").read().replace("@@CODE@@", "```python\n" + open(cf, encoding="utf-8").read().rstrip() + "\n```").replace("@@OUT@@", "```text\n" + o + "\n```")
    h, a = head(n)
    res.append(f"{h}\n{a}\n{body.strip()}\n"); done.append(n)
open(f"{D}/answers.md", "w", encoding="utf-8").write("\n---\n\n".join(res))
shutil.rmtree(f"{D}/code/__pycache__", ignore_errors=True)
print("built", done)
