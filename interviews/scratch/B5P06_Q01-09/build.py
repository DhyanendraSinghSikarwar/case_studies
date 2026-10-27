# Assembles answers.md from the part file headings + text/qNN.md + code/qNN.py (re-runs every code file with python3 -I).
import re, subprocess, pathlib, shutil, sys
root = pathlib.Path(__file__).resolve().parent
part = (root.parents[1] / 'Book5_DSA' / 'Book5_DSA_Part06.md').read_text().split('\n')
out = []
for n in range(1, 10):
    i = next(k for k, l in enumerate(part) if l.startswith('### Q%d ' % n))
    assert part[i + 1].startswith('**Asked at:**')
    code = (root / 'code' / ('q%02d.py' % n)).read_text().rstrip('\n')
    r = subprocess.run([sys.executable, '-I', str(root / 'code' / ('q%02d.py' % n))], capture_output=True, text=True, timeout=300)
    assert r.returncode == 0, (n, r.stderr)
    body = (root / 'text' / ('q%02d.md' % n)).read_text().rstrip('\n')
    assert '@@CODE@@' in body and '@@OUT@@' in body
    body = body.replace('@@CODE@@', code).replace('@@OUT@@', r.stdout.rstrip('\n'))
    out.append(part[i] + '\n' + part[i + 1] + '\n\n' + body + '\n')
    print('Q%d ok' % n)
(root / 'answers.md').write_text('\n'.join(out))
for p in root.rglob('__pycache__'): shutil.rmtree(p)
