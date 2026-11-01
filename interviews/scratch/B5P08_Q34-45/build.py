# Assembles answers.md: verbatim heading + Asked-at lines from the part file, text/qNN.md with {{CODE}} / {{OUTPUT}}
# placeholders filled from code/qNN.py and its real run (python3 -I). Re-run: python3 build.py
import os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
PART = os.path.join(HERE, '..', '..', 'Book5_DSA', 'Book5_DSA_Part08.md')
src = open(PART, encoding='utf-8').read()
blocks = {}
for m in re.finditer(r'^### Q(\d+) .*?(?=^### Q|\Z)', src, re.S | re.M):
    blocks[int(m.group(1))] = m.group(0)
out, done, fail = [], [], []
for n in range(34, 46):
    tp = os.path.join(HERE, 'text', f'q{n}.md'); cp = os.path.join(HERE, 'code', f'q{n}.py')
    if not (os.path.exists(tp) and os.path.exists(cp)): continue
    lines = blocks[n].split('\n')
    head = [l for l in lines if l.startswith('### Q') or l.startswith('**Asked at:**')]
    assert len(head) == 2, n
    r = subprocess.run([sys.executable, '-I', cp], capture_output=True, text=True, timeout=300, cwd=os.path.join(HERE, 'code'))
    if r.returncode != 0:
        fail.append(n); print('FAIL Q%d' % n, r.stderr[-800:]); continue
    body = open(tp, encoding='utf-8').read().strip()
    body = body.replace('{{CODE}}', open(cp, encoding='utf-8').read().rstrip()).replace('{{OUTPUT}}', r.stdout.rstrip())
    out.append('\n'.join(head) + '\n\n' + body + '\n'); done.append(n)
open(os.path.join(HERE, 'answers.md'), 'w', encoding='utf-8').write('\n'.join(out))
print('complete:', done, 'failed:', fail)
for d, _, fs in os.walk(HERE):
    if d.endswith('__pycache__'):
        import shutil; shutil.rmtree(d)
