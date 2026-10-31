import re, subprocess, os, sys
base = os.path.dirname(os.path.abspath(__file__))
part = os.path.join(base, "..", "..", "Book6_Scenarios", "Book6_Scenarios_Part01.md")
lines = open(part, encoding="utf-8").read().split("\n")
out = []
for q in range(34, 45):
    for i, l in enumerate(lines):
        if re.match(rf"### Q{q} ", l):
            head, asked = l, lines[i+1]; break
    assert asked.startswith("**Asked at:**")
    code = open(os.path.join(base, f"q{q}.py")).read().rstrip()
    r = subprocess.run([sys.executable, "-I", os.path.join(base, f"q{q}.py")], capture_output=True, text=True, cwd=base)
    assert r.returncode == 0, (q, r.stderr)
    body = open(os.path.join(base, f"q{q}.md")).read().rstrip()
    body = body.replace("@@CODE@@", "```python\n" + code + "\n```").replace("@@OUTPUT@@", "```text\n" + r.stdout.rstrip() + "\n```")
    out.append(head + "\n" + asked + "\n" + body + "\n")
open(os.path.join(base, "answers.md"), "w", encoding="utf-8").write("\n".join(out))
print("built", len(out))
