# Assembles answers.md for Book 5 Part 8, Q12-Q22, and re-runs every code file with python3 -I.
# Heading and Asked-at lines are copied verbatim from the part file; code and output are pasted from the real run.
import os, re, subprocess, sys, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
PART = os.path.join(HERE, '..', '..', 'Book5_DSA', 'Book5_DSA_Part08.md')
lines = open(PART, encoding='utf-8').read().split('\n')
idx = {}
for i, l in enumerate(lines):
    m = re.match(r'### Q(\d+) ', l)
    if m: idx[int(m.group(1))] = i
out = []
for q in range(12, 23):
    head = lines[idx[q]]
    asked = lines[idx[q] + 1]
    assert asked.startswith('**Asked at:**'), q
    code = open(os.path.join(HERE, 'code', 'q%d.py' % q), encoding='utf-8').read().rstrip('\n')
    r = subprocess.run([sys.executable, '-I', os.path.join(HERE, 'code', 'q%d.py' % q)], capture_output=True, text=True, timeout=600)
    assert r.returncode == 0, (q, r.stderr)
    md = open(os.path.join(HERE, 'md', 'q%d.md' % q), encoding='utf-8').read().rstrip('\n')
    assert '@@CODE@@' in md and '@@OUTPUT@@' in md
    md = md.replace('@@CODE@@', code).replace('@@OUTPUT@@', r.stdout.rstrip('\n'))
    for lab in ['**Pattern:**', '**Say this first (1 line):**', '**Brute force:**', '**Optimal:**', '**Complexity:**', '**Dry run:**',
                '**Code:**', '**Output (my run):**', '**Edge cases:**', '**Follow-ups:**', '**Common mistakes:**']:
        assert md.count(lab) == 1, (q, lab)
    out.append(head + '\n' + asked + '\n\n' + md + '\n')
    print('Q%d ok' % q)
open(os.path.join(HERE, 'answers.md'), 'w', encoding='utf-8').write('\n'.join(out))
for root, dirs, files in os.walk(HERE):
    for d in dirs:
        if d == '__pycache__': shutil.rmtree(os.path.join(root, d))
