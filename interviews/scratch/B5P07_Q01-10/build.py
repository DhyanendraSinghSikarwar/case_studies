# Assembles answers.md from the part file headings + text/qNN.md + code/qNN.py (regenerates code from parts/, re-runs every code file with python3 -I).
import subprocess, pathlib, shutil, sys
root = pathlib.Path(__file__).resolve().parent
subprocess.run([sys.executable, str(root / 'gen.py')], check=True)
part = (root.parents[1] / 'Book5_DSA' / 'Book5_DSA_Part07.md').read_text().split('\n')
out = []
for n in range(1, 11):
    tf = root / 'text' / ('q%02d.md' % n)
    if not tf.exists():
        print('Q%d missing' % n); continue
    i = next(k for k, l in enumerate(part) if l.startswith('### Q%d ' % n))
    assert part[i + 1].startswith('**Asked at:**')
    cf = root / 'code' / ('q%02d.py' % n)
    r = subprocess.run([sys.executable, '-I', str(cf)], capture_output=True, text=True, timeout=600)
    assert r.returncode == 0, (n, r.stderr)
    body = tf.read_text().rstrip('\n')
    assert '@@CODE@@' in body and '@@OUT@@' in body
    body = body.replace('@@CODE@@', cf.read_text().rstrip('\n')).replace('@@OUT@@', r.stdout.rstrip('\n'))
    out.append(part[i] + '\n' + part[i + 1] + '\n\n' + body + '\n')
    print('Q%d ok' % n)
(root / 'answers.md').write_text('\n'.join(out))
for p in root.rglob('__pycache__'): shutil.rmtree(p)
