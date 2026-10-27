# Assembles answers.md and re-runs every code file with python3 -I. Run: python3 build.py
import re, subprocess, sys, os, glob
HERE = os.path.dirname(os.path.abspath(__file__))
PART = os.path.join(HERE, '..', '..', 'Book5_DSA', 'Book5_DSA_Part06.md')
src = open(PART, encoding='utf-8').read().split('\n')
pre = open(os.path.join(HERE, 'code', 'preamble.py')).read()
def head_block(n):
    i = next(k for k, l in enumerate(src) if l.startswith(f'### Q{n} '))
    j = next(k for k in range(i + 1, len(src)) if src[k].startswith('**Asked at:**'))
    return src[i] + '\n\n' + src[j]
out = []; ran = []
for n in range(10, 19):
    body_p = os.path.join(HERE, 'code', f'q{n}_body.py')
    md_p = os.path.join(HERE, 'md', f'q{n}.md')
    if not (os.path.exists(body_p) and os.path.exists(md_p)): print('missing Q', n); continue
    code = pre + '\n' + open(body_p).read()
    cp = os.path.join(HERE, 'code', f'q{n}.py'); open(cp, 'w').write(code)
    r = subprocess.run([sys.executable, '-I', cp], capture_output=True, text=True, timeout=300)
    if r.returncode != 0: print('Q', n, 'FAILED\n', r.stderr[-1500:]); continue
    md = open(md_p, encoding='utf-8').read().rstrip('\n')
    md = md.replace('{{CODE}}', code.rstrip('\n')).replace('{{OUTPUT}}', r.stdout.rstrip('\n'))
    out.append(head_block(n) + '\n\n' + md + '\n'); ran.append(n)
open(os.path.join(HERE, 'answers.md'), 'w', encoding='utf-8').write('\n'.join(out))
print('assembled Qs', ran)
for d in glob.glob(os.path.join(HERE, '**', '__pycache__'), recursive=True):
    import shutil; shutil.rmtree(d)
