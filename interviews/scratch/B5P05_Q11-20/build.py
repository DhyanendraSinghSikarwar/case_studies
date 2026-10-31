# Assembles answers.md from the part file's headings + text/qNN.md + code/qNN.py, re-running each code file.
# Run: python3 -I build.py   (from anywhere)
import os, re, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__))
PART = os.path.join(H, "..", "..", "Book5_DSA", "Book5_DSA_Part05.md")
lines = open(PART, encoding="utf-8").read().split("\n")
out = []
done = []
for q in range(11, 21):
    start = next(i for i, l in enumerate(lines) if re.match(r"### Q%d " % q, l))
    head, asked = lines[start], lines[start + 1]
    assert asked.startswith("**Asked at:**"), q
    tp = os.path.join(H, "text", "q%d.md" % q)
    cp = os.path.join(H, "code", "q%d.py" % q)
    if not (os.path.exists(tp) and os.path.exists(cp)):
        print("Q%d missing" % q); continue
    code = open(cp, encoding="utf-8").read().rstrip("\n")
    r = subprocess.run([sys.executable, "-I", cp], capture_output=True, text=True, timeout=300)
    assert r.returncode == 0, (q, r.stderr[-800:])
    outp = r.stdout.rstrip("\n")
    body = open(tp, encoding="utf-8").read().rstrip("\n")
    body = body.replace("@@CODE@@", "```python\n" + code + "\n```").replace("@@OUTPUT@@", "```text\n" + outp + "\n```")
    out.append(head + "\n" + asked + "\n\n" + body + "\n")
    done.append(q)
open(os.path.join(H, "answers.md"), "w", encoding="utf-8").write("\n".join(out))
print("built Q", done)
