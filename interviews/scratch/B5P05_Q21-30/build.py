# Assembles answers.md: headings + Asked-at copied verbatim from the part file; code/qNN.py re-run with python3 -I
# and the real output pasted; prose from qNN.md (markers @@CODE@@ and @@OUTPUT@@). Run: python3 build.py
import os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
PART = os.path.join(HERE, '..', '..', 'Book5_DSA', 'Book5_DSA_Part05.md')
txt = open(PART, encoding='utf-8').read()
out, status = [], []
for n in range(21, 31):
    m = re.search(rf'^### Q{n} .*\n\*\*Asked at:\*\*.*$', txt, re.M)
    head = m.group(0)
    code_f = os.path.join(HERE, 'code', f'q{n}.py')
    prose_f = os.path.join(HERE, f'q{n}.md')
    if not (os.path.exists(code_f) and os.path.exists(prose_f)):
        status.append((n, 'MISSING')); continue
    code = open(code_f, encoding='utf-8').read().rstrip('\n')
    r = subprocess.run([sys.executable, '-I', code_f], capture_output=True, text=True, cwd=os.path.join(HERE, 'code'), timeout=300)
    assert r.returncode == 0, (n, r.stderr[-800:])
    prose = open(prose_f, encoding='utf-8').read().strip('\n')
    assert '@@CODE@@' in prose and '@@OUTPUT@@' in prose, n
    body = prose.replace('@@CODE@@', '```python\n' + code + '\n```').replace('@@OUTPUT@@', '```\n' + r.stdout.rstrip('\n') + '\n```')
    for lab in ['**Pattern:**', '**Say this first (1 line):**', '**Brute force:**', '**Optimal:**', '**Complexity:**', '**Dry run:**', '**Code:**', '**Output (my run):**', '**Edge cases:**', '**Follow-ups:**', '**Common mistakes:**']:
        assert lab in body, (n, lab)
    assert body.count('```python') == 1, n
    out.append(head + '\n\n' + body + '\n')
    status.append((n, 'ok'))
open(os.path.join(HERE, 'answers.md'), 'w', encoding='utf-8').write('\n'.join(out))
for s in status: print(s)
for root, ds, fs in os.walk(HERE):
    for d in ds:
        if d == '__pycache__':
            import shutil; shutil.rmtree(os.path.join(root, d))
