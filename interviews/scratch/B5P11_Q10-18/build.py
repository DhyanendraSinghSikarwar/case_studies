# Assembles answers.md from parts/qNN.md + code/qNN.py (re-runs each code file with python3 -I; pastes real output).
# Headings and Asked-at lines are copied verbatim from Book5_DSA/Book5_DSA_Part11.md. Run: python3 build.py
import os, re, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__))
part = open(os.path.join(here, '..', '..', 'Book5_DSA', 'Book5_DSA_Part11.md'), encoding='utf-8').read()
out, done, missing = [], [], []
for q in range(10, 19):
    m = re.search(r'^(### Q%d .*)\n(\*\*Asked at:\*\*.*)\n' % q, part, re.M)
    assert m, q
    pf = os.path.join(here, 'parts', 'q%02d.md' % q)
    cf = os.path.join(here, 'code', 'q%02d.py' % q)
    if not (os.path.exists(pf) and os.path.exists(cf)):
        missing.append(q); continue
    r = subprocess.run([sys.executable, '-I', cf], capture_output=True, text=True, cwd=os.path.join(here, 'code'))
    assert r.returncode == 0, (q, r.stderr[-800:])
    body = open(pf, encoding='utf-8').read().replace('@@CODE@@', open(cf, encoding='utf-8').read().rstrip('\n')).replace('@@OUTPUT@@', r.stdout.rstrip('\n'))
    out.append(m.group(1) + '\n' + m.group(2) + '\n\n' + body.strip('\n') + '\n')
    done.append(q)
open(os.path.join(here, 'answers.md'), 'w', encoding='utf-8').write('\n'.join(out))
print('assembled', done, 'missing', missing)
