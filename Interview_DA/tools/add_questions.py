"""Add gap-fill questions to a frozen-format question part, safely.

Usage:
  python tools/add_questions.py BOOK_DIR BOOK_NUM PART items.json [--dry-run]
    BOOK_DIR  e.g. Book04_PowerBI_Viz        BOOK_NUM e.g. 4        PART e.g. 5
    items.json: [{"stars": 2, "diff": "🟡", "q": "Question text?"}, ...]   (stars 1-3; diff one of 🟢 🟡 🔴)

What it does: rejects any new question whose token-overlap (Jaccard) with ANY existing question in the book
is >= 0.5 (prints the clash and exits without writing); otherwise inserts the questions, re-sorts the part
(stars descending, then 🟢 -> 🟡 -> 🔴, stable), renumbers Q1..Qn, updates the 'Actual' count in the header,
and rewrites research/index_rows/B<book>P<part>.md. Existing questions keep their text; only numbers change.
Run from /home/user/case_studies/Interview_DA.
"""
import glob, json, re, sys

STOP = set('the a an in of to and or for how do does is are what why when which with on from by as it you your i can if this that be at using use'.split())
tok = lambda s: {w for w in re.findall(r'[a-z0-9#!]+', s.lower()) if w not in STOP}


def main():
    book_dir, book, part, items_path = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    dry = '--dry-run' in sys.argv
    items = json.load(open(items_path, encoding='utf-8'))
    existing = []
    for f in glob.glob(f'{book_dir}/Book{book:02d}_Part*.md'):
        for m in re.finditer(r'(?m)^### Q\d+ ⭐+ (?:🟢|🟡|🔴) (.*)$', open(f, encoding='utf-8').read()):
            existing.append((f, m.group(1)))
    bad = False
    for it in items:
        for f, q in existing:
            a, b = tok(it['q']), tok(q)
            j = len(a & b) / max(1, len(a | b))
            if j >= 0.5:
                print(f'CLASH {j:.2f}: "{it["q"][:80]}" vs {f[-8:-3]}: "{q[:80]}"'); bad = True
    if bad:
        sys.exit('rejected: reword or replace the clashing questions')
    f = f'{book_dir}/Book{book:02d}_Part{part:02d}.md'
    t = open(f, encoding='utf-8').read()
    segs = re.split(r'(?m)^(?=### Q\d+ )', t)
    head, body = segs[0], segs[1:]
    for it in items:
        body.append(f"### Q0 {'⭐' * it['stars']} {it['diff']} {it['q']}\n<!-- ANSWER_PENDING -->\n\n")
    key = lambda s: (-len(re.match(r'### Q\d+ (⭐+)', s).group(1)), '🟢🟡🔴'.index(re.match(r'### Q\d+ ⭐+ (🟢|🟡|🔴)', s).group(1)))
    body = sorted(body, key=key)
    out, rows = [], []
    for i, s in enumerate(body, 1):
        s = re.sub(r'^### Q\d+', f'### Q{i}', s, count=1)
        if not s.endswith('\n\n'): s = s.rstrip('\n') + '\n\n'
        out.append(s)
        rows.append(f"| B{book}P{part:02d}Q{i} | {book} | {part} | {s.split(chr(10))[0].split(' ', 4)[4]} |")
    head = re.sub(r'\*\*Actual:\*\* \d+ questions', f'**Actual:** {len(body)} questions', head)
    if dry:
        print('dry run ok:', len(body), 'questions after insert'); return
    open(f, 'w', encoding='utf-8').write(head + ''.join(out).rstrip('\n') + '\n')
    open(f'research/index_rows/B{book}P{part:02d}.md', 'w', encoding='utf-8').write(
        '| Q-ID | Book | Part | Canonical question |\n|---|---|---|---|\n' + '\n'.join(rows) + '\n')
    print('inserted', len(items), '->', len(body), 'questions in part', part)


main()
