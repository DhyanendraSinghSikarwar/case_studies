import re, pathlib, subprocess, sys
base = pathlib.Path(__file__).parent
part = base.parent.parent / "Book6_Scenarios" / "Book6_Scenarios_Part02.md"
lines = part.read_text().splitlines()
out = []
for n in range(11, 21):
    i = next(k for k, l in enumerate(lines) if l.startswith(f"### Q{n} "))
    head, asked = lines[i], lines[i + 1]
    assert asked.startswith("**Asked at:**")
    body = (base / "body" / f"q{n}.md").read_text().rstrip("\n")
    code = (base / "code" / f"q{n}.py").read_text().rstrip("\n")
    output = (base / "out" / f"q{n}.txt").read_text().rstrip("\n")
    body = body.replace("{{CODE}}", "```python\n" + code + "\n```").replace("{{OUTPUT}}", "```text\n" + output + "\n```")
    out.append("\n".join([head, asked, body]) + "\n")
(base / "answers.md").write_text("\n".join(out))
print("built", len(out))
