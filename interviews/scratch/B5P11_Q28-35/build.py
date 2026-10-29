"""Assemble answers.md for Book 5 Part 11, Q28-Q35.
For each question: copy the heading and Asked-at lines verbatim from the part file, take the body
(body_qNN.md) with <<CODE>> / <<OUTPUT>> markers, re-run code/qNN.py with python3 -I and paste the real
output. Writes qNN.md per question (progress on disk) and answers.md. Run: python3 build.py"""
import os, re, subprocess, sys, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
PART = os.path.join(ROOT, "Book5_DSA", "Book5_DSA_Part11.md")
QS = range(28, 36)
LABELS = ["**Pattern:**", "**Say this first (1 line):**", "**Brute force:**", "**Optimal:**", "**Complexity:**",
          "**Dry run:**", "**Code:**", "**Output (my run):**", "**Edge cases:**", "**Follow-ups:**", "**Common mistakes:**"]

lines = open(PART, encoding="utf-8").read().split("\n")
parts, ok = [], []
for q in QS:
    idx = next(i for i, l in enumerate(lines) if re.match(rf"### Q{q} ", l))
    heading = lines[idx]
    asked = next(l for l in lines[idx + 1: idx + 6] if l.startswith("**Asked at:**"))
    body_path = os.path.join(HERE, f"body_q{q}.md")
    code_path = os.path.join(HERE, "code", f"q{q}.py")
    if not (os.path.exists(body_path) and os.path.exists(code_path)):
        print(f"Q{q}: missing body or code, skipped"); continue
    body = open(body_path, encoding="utf-8").read().rstrip("\n")
    code = open(code_path, encoding="utf-8").read().rstrip("\n")
    r = subprocess.run([sys.executable, "-I", code_path], capture_output=True, text=True, cwd="/")
    if r.returncode != 0:
        print(f"Q{q}: CODE FAILED\n{r.stderr}"); sys.exit(1)
    out = r.stdout.rstrip("\n")
    assert "<<CODE>>" in body and "<<OUTPUT>>" in body, q
    body = body.replace("<<CODE>>", "```python\n" + code + "\n```").replace("<<OUTPUT>>", "```\n" + out + "\n```")
    last = -1
    for lab in LABELS:
        p = body.find(lab)
        assert p > last, f"Q{q}: label {lab} missing or out of order"
        last = p
    text = heading + "\n" + asked + "\n\n" + body + "\n"
    open(os.path.join(HERE, f"q{q}.md"), "w", encoding="utf-8").write(text)
    parts.append(text); ok.append(q)
    print(f"Q{q}: ok ({len(out.splitlines())} output lines)")
open(os.path.join(HERE, "answers.md"), "w", encoding="utf-8").write("\n".join(parts))
print("assembled", ok)
for dp, dn, fn in os.walk(HERE):
    for d in dn:
        if d == "__pycache__": shutil.rmtree(os.path.join(dp, d), ignore_errors=True)
