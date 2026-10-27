import re, subprocess, pathlib, sys
H = pathlib.Path(__file__).parent
part = (H.parent.parent / "Book5_DSA/Book5_DSA_Part01.md").read_text().splitlines()
out = []
for n in range(1, 11):
    i = next(k for k, l in enumerate(part) if l.startswith(f"### Q{n} "))
    head, asked = part[i], part[i + 1]
    assert asked.startswith("**Asked at:**")
    f = H / f"parts/q{n:02d}.md"
    if not f.exists():
        continue
    code = (H / f"code/q{n:02d}.py").read_text().rstrip()
    r = subprocess.run(["python3", "-I", str(H / f"code/q{n:02d}.py")], capture_output=True, text=True, timeout=300)
    assert r.returncode == 0, (n, r.stderr)
    body = f.read_text().replace("{{CODE}}", "```python\n" + code + "\n```").replace("{{OUTPUT}}", "```text\n" + r.stdout.rstrip() + "\n```")
    out.append(head + "\n" + asked + "\n\n" + body.strip() + "\n")
(H / "answers.md").write_text("\n".join(out))
print("built", len(out))
