# Assembles answers.md from texts/qNN.md (prose with {{CODE}} / {{OUTPUT}}), code/prelude.py + code/body/qNN.py.
# Re-runs every code file with python3 -I and pastes the real output. Headings and Asked-at copied verbatim from the part file.
import os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
PART = os.path.join(HERE, "..", "..", "Book5_DSA", "Book5_DSA_Part07.md")
lines = open(PART, encoding="utf-8").read().split("\n")
prelude = open(os.path.join(HERE, "code", "prelude.py"), encoding="utf-8").read().rstrip() + "\n\n"
out, done, failed = [], [], []
for n in range(31, 41):
    q = "q%d" % n
    body = os.path.join(HERE, "code", "body", q + ".py")
    text = os.path.join(HERE, "texts", q + ".md")
    if not (os.path.exists(body) and os.path.exists(text)):
        print(q, "missing"); continue
    code = prelude + open(body, encoding="utf-8").read()
    cpath = os.path.join(HERE, "code", q + ".py")
    open(cpath, "w", encoding="utf-8").write(code)
    r = subprocess.run([sys.executable, "-I", cpath], capture_output=True, text=True, timeout=600)
    if r.returncode != 0:
        print(q, "FAILED", r.stderr[-800:]); failed.append(n); continue
    i = next(k for k, l in enumerate(lines) if l.startswith("### Q%d " % n))
    head, asked = lines[i], lines[i + 1]
    assert asked.startswith("**Asked at:**")
    t = open(text, encoding="utf-8").read().strip()
    t = t.replace("{{CODE}}", "```python\n" + code.rstrip() + "\n```").replace("{{OUTPUT}}", "```\n" + r.stdout.rstrip() + "\n```")
    out.append(head + "\n" + asked + "\n\n" + t + "\n")
    done.append(n)
open(os.path.join(HERE, "answers.md"), "w", encoding="utf-8").write("\n".join(out))
print("complete:", done, "failed:", failed)
