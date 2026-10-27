import re, subprocess, os, glob
ROOT = "/home/user/case_studies/interviews"
D = f"{ROOT}/scratch/B5P02_Q34-45"
part = open(f"{ROOT}/Book5_DSA/Book5_DSA_Part02.md").read().split("\n")
def head(n):
    i = next(k for k, l in enumerate(part) if l.startswith(f"### Q{n} "))
    assert part[i + 1].startswith("**Asked at:**")
    return part[i], part[i + 1]
res, done = [], []
for n in range(34, 46):
    bf, cf = f"{D}/body/q{n}.md", f"{D}/code/q{n}.py"
    if not (os.path.exists(bf) and os.path.exists(cf)): continue
    r = subprocess.run(["python3", "-I", cf], capture_output=True, text=True, cwd=f"{D}/code")
    o = (r.stdout + r.stderr).strip()
    assert r.returncode == 0, (n, o)
    body = open(bf).read().replace("@@CODE@@", "```python\n" + open(cf).read().rstrip() + "\n```").replace("@@OUT@@", "```text\n" + o + "\n```")
    h, a = head(n)
    res.append(f"{h}\n{a}\n{body.strip()}\n"); done.append(n)
open(f"{D}/answers.md", "w").write("\n---\n\n".join(res))
for p in glob.glob(f"{D}/code/__pycache__"): 
    import shutil; shutil.rmtree(p)
print("built", done)
