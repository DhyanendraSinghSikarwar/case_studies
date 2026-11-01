"""Assemble answers.md: heading + Asked-at copied verbatim from the part file,
body from parts/qNN.md with @@CODE@@ / @@OUTPUT@@ filled from code/qNN.py and its real run (python3 -I)."""
import os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
PART = os.path.join(HERE, "..", "..", "Book5_DSA", "Book5_DSA_Part04.md")
text = open(PART, encoding="utf-8").read().split("\n")
out, done = [], []
for n in range(1, 11):
    pf = os.path.join(HERE, "parts", f"q{n:02d}.md")
    cf = os.path.join(HERE, "code", f"q{n:02d}.py")
    if not (os.path.exists(pf) and os.path.exists(cf)):
        continue
    idx = next(i for i, l in enumerate(text) if l.startswith(f"### Q{n} "))
    head, asked = text[idx], text[idx + 1]
    assert asked.startswith("**Asked at:**")
    r = subprocess.run([sys.executable, "-I", cf], capture_output=True, text=True, timeout=300, cwd="/")
    if r.returncode != 0:
        print(f"Q{n} FAILED\n{r.stderr}"); sys.exit(1)
    body = open(pf, encoding="utf-8").read()
    assert "@@CODE@@" in body and "@@OUTPUT@@" in body
    body = body.replace("@@CODE@@", "```python\n" + open(cf, encoding="utf-8").read().rstrip("\n") + "\n```")
    body = body.replace("@@OUTPUT@@", "```\n" + r.stdout.rstrip("\n") + "\n```")
    out.append(head + "\n" + asked + "\n\n" + body.strip("\n") + "\n")
    done.append(n)
open(os.path.join(HERE, "answers.md"), "w", encoding="utf-8").write("\n".join(out))
for root, ds, fs in os.walk(HERE):
    for d in ds:
        if d == "__pycache__":
            import shutil; shutil.rmtree(os.path.join(root, d))
print("built questions:", done)
