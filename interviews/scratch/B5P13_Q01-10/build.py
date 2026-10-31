# Assembles answers.md from parts/qNN.md (answer text with {{CODE}} / {{OUT}} markers), code/qNN.py (re-run with python3 -I) and the
# heading + Asked-at lines copied verbatim from the part file.
import re, subprocess, os, sys, shutil
here = os.path.dirname(os.path.abspath(__file__))
root = os.path.abspath(os.path.join(here, '..', '..'))
part = open(os.path.join(root, 'Book5_DSA', 'Book5_DSA_Part13.md'), encoding='utf-8').read()
out = []
for q in range(1, 11):
    m = re.search(r'^### Q%d .*$' % q, part, re.M); head = m.group(0)
    asked = re.search(r'^\*\*Asked at:\*\*.*$', part[m.end():], re.M).group(0)
    code = open(os.path.join(here, 'code', 'q%02d.py' % q), encoding='utf-8').read().rstrip('\n')
    r = subprocess.run([sys.executable, '-I', os.path.join(here, 'code', 'q%02d.py' % q)], capture_output=True, text=True, cwd='/')
    assert r.returncode == 0, (q, r.stderr)
    tpl = open(os.path.join(here, 'parts', 'q%02d.md' % q), encoding='utf-8').read().strip('\n')
    assert '{{CODE}}' in tpl and '{{OUT}}' in tpl, q
    body = tpl.replace('{{CODE}}', code).replace('{{OUT}}', r.stdout.rstrip('\n'))
    out.append(head + '\n' + asked + '\n\n' + body + '\n')
    print('Q%d ok' % q)
open(os.path.join(here, 'answers.md'), 'w', encoding='utf-8').write('\n---\n\n'.join(out))
shutil.rmtree(os.path.join(here, 'code', '__pycache__'), ignore_errors=True)
