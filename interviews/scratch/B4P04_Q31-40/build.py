import re, pathlib
ROOT = pathlib.Path("/home/user/case_studies/interviews")
part = (ROOT / "Book4_MLOps/Book4_MLOps_Part04.md").read_text().splitlines()
O = pathlib.Path("/tmp/claude-0/b4p04")
CODE = ROOT / "scratch/B4P04_Q31-40/code"

def head(n):
    for i, l in enumerate(part):
        if l.startswith(f"### Q{n} "):
            assert part[i + 1].startswith("**Asked at:**"); return l, part[i + 1]
def out(name, maxlines=None, drop=()):
    t = (O / name).read_text().rstrip("\n").splitlines()
    t = [l for l in t if not any(d in l for d in drop)]
    if maxlines: t = t[:maxlines]
    return "\n".join(t)
def code(f, a=None, b=None):
    t = (CODE / f).read_text().splitlines()
    return "\n".join(t[(a or 1) - 1:b])

A = {}
exec((ROOT / "scratch/B4P04_Q31-40/bodies.py").read_text())
res = []
for n in range(31, 41):
    h, asked = head(n)
    res.append(f"{h}\n{asked}\n{A[n]}\n")
(ROOT / "scratch/B4P04_Q31-40/answers.md").write_text("\n".join(res))
print("ok", len(res))
