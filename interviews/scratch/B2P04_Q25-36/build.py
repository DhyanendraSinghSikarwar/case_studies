import re, subprocess, sys
base = "/home/user/case_studies/interviews/"
part = open(base + "Book2_GenAI/Book2_GenAI_Part04.md").read().split("\n")
heads = {}
for i, l in enumerate(part):
    m = re.match(r"### Q(\d+) ", l)
    if m: heads[int(m.group(1))] = (l, part[i+1])
here = base + "scratch/B2P04_Q25-36/"
src = open(here + "bodies.md").read()
blocks = re.split(r"^=====Q(\d+)\n", src, flags=re.M)[1:]
out = []
cache = {}
def run(f):
    if f not in cache:
        r = subprocess.run(["python3", "-I", here + "code/" + f], capture_output=True, text=True, timeout=120)
        assert r.returncode == 0, (f, r.stderr)
        cache[f] = r.stdout.rstrip("\n")
    return cache[f]
for n, body in zip(blocks[::2], blocks[1::2]):
    n = int(n)
    body = re.sub(r"@@CODE (\S+)@@", lambda m: open(here + "code/" + m.group(1)).read().rstrip("\n"), body)
    body = re.sub(r"@@OUT (\S+)@@", lambda m: run(m.group(1)), body)
    h, a = heads[n]
    out.append(h + "\n" + a + "\n" + body.strip("\n"))
open(here + "answers.md", "w").write("\n\n".join(out) + "\n")
