import re, subprocess, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
PART = os.path.join(HERE, '..', '..', 'Book5_DSA', 'Book5_DSA_Part14.md')
lines = open(PART).read().split('\n')
out = ['# Book 5 Part 14: answers to Q21-Q30 (Wave B agent)', '']
bad = []
for q in range(21, 31):
    i = next(k for k, l in enumerate(lines) if l.startswith('### Q%d ' % q))
    heading, asked = lines[i], lines[i + 1]
    assert asked.startswith('**Asked at:**')
    code_path = os.path.join(HERE, 'code', 'q%d.py' % q)
    r = subprocess.run([sys.executable, '-I', code_path], capture_output=True, text=True, cwd=os.path.join(HERE, 'code'), timeout=600)
    if r.returncode != 0:
        bad.append(q); print('FAIL q%d' % q, r.stderr[-500:])
    code = open(code_path).read()
    if not code.endswith('\n'): code += '\n'
    outp = r.stdout if r.stdout.endswith('\n') else r.stdout + '\n'
    tpl = open(os.path.join(HERE, 'tpl', 'q%d.md' % q)).read()
    body = tpl.replace('{{CODE}}', code).replace('{{OUTPUT}}', outp)
    out += [heading, asked, '', body.rstrip('\n'), '', '---', '']
    print('ok q%d' % q if q not in bad else '')
open(os.path.join(HERE, 'answers.md'), 'w').write('\n'.join(out))
for root, dirs, files in os.walk(HERE):
    if '__pycache__' in dirs:
        import shutil; shutil.rmtree(os.path.join(root, '__pycache__'))
print('FAILED:', bad if bad else 'none')
