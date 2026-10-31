# Assembles answers.md from q*.md templates + code, re-running every code file with python3 -I.
import re, subprocess, glob, os
here = os.path.dirname(os.path.abspath(__file__))
part = open(os.path.join(here, '../../Book5_DSA/Book5_DSA_Part06.md'), encoding='utf-8').read().split('\n')
prelude = open(f'{here}/code/prelude.py').read()
out_parts = []
for q in range(19, 28):
    qfile = f'{here}/q{q}.md'
    if not os.path.exists(qfile):
        print('missing', q); continue
    idx = next(i for i, l in enumerate(part) if l.startswith(f'### Q{q} '))
    heading, asked = part[idx], part[idx + 1]
    assert asked.startswith('**Asked at:**')
    body = open(f'{here}/code/q{q}_body.py').read()
    full = prelude + '\n' + body
    open(f'{here}/code/q{q}.py', 'w').write(full)
    r = subprocess.run(['python3', '-I', f'{here}/code/q{q}.py'], capture_output=True, text=True, timeout=300)
    assert r.returncode == 0, (q, r.stdout, r.stderr)
    open(f'{here}/code/q{q}.out', 'w').write(r.stdout)
    txt = open(qfile, encoding='utf-8').read()
    txt = txt.replace('@@CODE@@', '```python\n' + full.rstrip() + '\n```').replace('@@OUTPUT@@', '```\n' + r.stdout.rstrip() + '\n```')
    out_parts.append(heading + '\n' + asked + '\n\n' + txt.strip() + '\n')
    print('Q', q, 'ok')
open(f'{here}/answers.md', 'w', encoding='utf-8').write('\n'.join(out_parts))
for d in glob.glob(f'{here}/**/__pycache__', recursive=True):
    subprocess.run(['rm', '-rf', d])
