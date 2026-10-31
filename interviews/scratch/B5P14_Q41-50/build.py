# Assembles answers.md from parts/qNN.md + code/qNN.py; re-runs every code file with python3 -I and pastes the real output.
# Run: python3 build.py   (from anywhere). Headings and Asked-at lines are copied verbatim from the part file.
import os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
PART = os.path.join(HERE, '..', '..', 'Book5_DSA', 'Book5_DSA_Part14.md')
lines = open(PART, encoding='utf-8').read().split('\n')
out = []; failures = []
for q in range(41, 51):
    h = next(i for i, l in enumerate(lines) if l.startswith('### Q%d ' % q))
    asked = next(i for i in range(h, h + 6) if lines[i].startswith('**Asked at:**'))
    code = open(os.path.join(HERE, 'code', 'q%d.py' % q), encoding='utf-8').read().rstrip('\n')
    r = subprocess.run([sys.executable, '-I', os.path.join(HERE, 'code', 'q%d.py' % q)], capture_output=True, text=True, timeout=300)
    if r.returncode != 0:
        failures.append(q); print('FAILED Q%d' % q, r.stderr[-500:])
    outp = r.stdout.rstrip('\n')
    body = open(os.path.join(HERE, 'parts', 'q%d.md' % q), encoding='utf-8').read().rstrip('\n')
    body = body.replace('@@CODE@@', '```python\n' + code + '\n```').replace('@@OUTPUT@@', '```\n' + outp + '\n```')
    out.append(lines[h] + '\n' + lines[asked] + '\n' + body + '\n')
    print('Q%d ok' % q)
open(os.path.join(HERE, 'answers.md'), 'w', encoding='utf-8').write('\n'.join(out))
for d, _, fs in os.walk(HERE):
    if d.endswith('__pycache__'):
        for f in fs: os.remove(os.path.join(d, f))
        os.rmdir(d)
sys.exit(1 if failures else 0)
