# Assembles answers.md for Book 5 Part 12 Q28-Q35: copies each heading and Asked-at line verbatim from the part file,
# re-runs every code/qNN.py with python3 -I and pastes the real output next to the code. Run: python3 build.py
import os, re, subprocess, sys, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
PART = os.path.join(HERE, '..', '..', 'Book5_DSA', 'Book5_DSA_Part12.md')
lines = open(PART, encoding='utf-8').read().split('\n')
out = []
for n in range(28, 36):
    idx = next(i for i, l in enumerate(lines) if l.startswith(f'### Q{n} '))
    head, asked = lines[idx], lines[idx + 1]
    assert asked.startswith('**Asked at:**')
    code = open(os.path.join(HERE, 'code', f'q{n}.py'), encoding='utf-8').read()
    r = subprocess.run([sys.executable, '-I', os.path.join(HERE, 'code', f'q{n}.py')], capture_output=True, text=True, timeout=600)
    assert r.returncode == 0, (n, r.stderr)
    if not r.stdout.endswith('\n'): r.stdout += '\n'
    body = open(os.path.join(HERE, 'body', f'q{n}.md'), encoding='utf-8').read()
    assert '{{CODE}}' in body and '{{OUTPUT}}' in body
    body = body.replace('{{CODE}}', code).replace('{{OUTPUT}}', r.stdout)
    out.append(head + '\n' + asked + '\n\n' + body.rstrip('\n') + '\n')
    print('Q%d ok' % n)
open(os.path.join(HERE, 'answers.md'), 'w', encoding='utf-8').write('\n'.join(out))
for d in ('code', '.'):
    shutil.rmtree(os.path.join(HERE, d, '__pycache__'), ignore_errors=True)
print('answers.md written')
