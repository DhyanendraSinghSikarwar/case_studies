import re, os
ROOT = "/home/user/case_studies/interviews"
part = open(f"{ROOT}/Book4_MLOps/Book4_MLOps_Part12.md").read().split("\n")
C = f"{ROOT}/scratch/B4P12_Q12-22/code"
def head(n):
    i = next(k for k, l in enumerate(part) if l.startswith(f"### Q{n} "))
    assert part[i + 1].startswith("**Asked at:**")
    return part[i], part[i + 1]
def code(fn, lang="python"): return f"```{lang}\n{open(f'{C}/{fn}').read().rstrip()}\n```"
def out(n): return "```\n" + open(f"{C}/out/q{n}.txt").read().rstrip() + "\n```"
B = {}
exec(open(f"{ROOT}/scratch/B4P12_Q12-22/bodies.py").read())
res = []
for n in range(12, 23):
    h, a = head(n)
    body = B[n]
    body = re.sub(r"@@CODE (\S+) ?(\w*)@@", lambda m: code(m.group(1), m.group(2) or "python"), body)
    body = re.sub(r"@@OUT (\d+)@@", lambda m: out(m.group(1)), body)
    res.append(f"{h}\n{a}\n{body.strip()}\n")
open(f"{ROOT}/scratch/B4P12_Q12-22/answers.md", "w").write("\n---\n\n".join(res))
print("built", len(res))
