# Assembles answers.md from text/qNN.md + code/qNN.py (re-run with python3 -I) + headings from the part file. Run: python3 build.py
import os, re, subprocess, sys, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
PART = os.path.join(HERE, '..', '..', 'Book5_DSA', 'Book5_DSA_Part11.md')
src = open(PART, encoding='utf-8').read()
blocks = re.split(r'(?m)^(?=### Q\d+ )', src)
head = {}
for b in blocks:
    m = re.match(r'### Q(\d+) ', b)
    if m:
        lines = b.split('\n')
        asked = [l for l in lines if l.startswith('**Asked at:**')]
        assert len(asked) == 1
        head[int(m.group(1))] = (lines[0], asked[0])
out, done, bad = [], [], []
for q in range(19, 28):
    tp = os.path.join(HERE, 'text', f'q{q:02d}.md'); cp = os.path.join(HERE, 'code', f'q{q:02d}.py')
    if not (os.path.exists(tp) and os.path.exists(cp)):
        bad.append(q); continue
    r = subprocess.run([sys.executable, '-I', cp], capture_output=True, text=True, cwd=os.path.join(HERE, 'code'))
    if r.returncode:
        print('FAIL', q, r.stderr[-500:]); bad.append(q); continue
    text = open(tp, encoding='utf-8').read()
    code = open(cp, encoding='utf-8').read().rstrip('\n')
    assert '{{CODE}}' in text and '{{OUTPUT}}' in text
    text = text.replace('{{CODE}}', '```python\n' + code + '\n```').replace('{{OUTPUT}}', '```\n' + r.stdout.rstrip('\n') + '\n```')
    for lab in ['**Pattern:**', '**Say this first (1 line):**', '**Brute force:**', '**Optimal:**', '**Complexity:**', '**Dry run:**', '**Code:**', '**Output (my run):**', '**Edge cases:**', '**Follow-ups:**', '**Common mistakes:**']:
        assert text.count(lab) == 1, (q, lab)
    out.append(head[q][0] + '\n' + head[q][1] + '\n\n' + text.strip() + '\n')
    done.append(q)
open(os.path.join(HERE, 'answers.md'), 'w', encoding='utf-8').write('\n'.join(out))
print('assembled', done, 'missing/failed', bad)
for root, ds, fs in os.walk(HERE):
    for d in ds:
        if d == '__pycache__':
            shutil.rmtree(os.path.join(root, d))
