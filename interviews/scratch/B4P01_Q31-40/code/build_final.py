from build_c import *
parts = ["<!-- Wave B answers, Book 4 Part 1, Q31-Q40 (no edits to the part file) -->\n"]
for n in range(31, 41):
    parts.append(head(n) + "\n" + A[n].strip() + "\n")
out_p = HERE.parent / "answers.md"
out_p.write_text("\n".join(parts))
print("wrote", out_p, out_p.stat().st_size)
