"""Assemble answers.md from qNN.md (text with @@CODE@@ and @@OUTPUT@@ markers) + code/qNN.py.
Re-runs every code file with python3 -I and pastes the real output. Heading and Asked-at lines are copied verbatim from the part file."""
import os, re, subprocess, sys, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
PART = os.path.join(HERE, '..', '..', 'Book5_DSA', 'Book5_DSA_Part10.md')
text = open(PART, encoding='utf-8').read()
parts = []
bad = []
for n in range(1, 11):
    m = re.search(r'^### Q%d .*\n\*\*Asked at:\*\*.*$' % n, text, re.M)
    assert m, n
    head = m.group(0)
    md = os.path.join(HERE, 'q%02d.md' % n)
    code = os.path.join(HERE, 'code', 'q%02d.py' % n)
    if not (os.path.exists(md) and os.path.exists(code)):
        print('Q%d: missing, skipped' % n); continue
    r = subprocess.run([sys.executable, '-I', code], capture_output=True, text=True, timeout=300)
    if r.returncode != 0:
        bad.append(n); print('Q%d FAILED\n%s' % (n, r.stderr[-800:]))
    out = r.stdout.rstrip('\n')
    open(os.path.join(HERE, 'code', 'q%02d.out' % n), 'w').write(out + '\n')
    body = open(md, encoding='utf-8').read().strip('\n')
    assert '@@CODE@@' in body and '@@OUTPUT@@' in body, n
    body = body.replace('@@CODE@@', '```python\n' + open(code, encoding='utf-8').read().rstrip('\n') + '\n```')
    body = body.replace('@@OUTPUT@@', '```\n' + out + '\n```')
    parts.append(head + '\n\n' + body)
    print('Q%d ok (%d output lines)' % (n, out.count('\n') + 1))
open(os.path.join(HERE, 'answers.md'), 'w', encoding='utf-8').write('\n\n'.join(parts) + '\n')
for root, dirs, _ in os.walk(HERE):
    for d in dirs:
        if d == '__pycache__':
            shutil.rmtree(os.path.join(root, d))
print('assembled', len(parts), 'answers; failures:', bad)
