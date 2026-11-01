import re, subprocess, sys, pathlib
root = pathlib.Path(__file__).parent
part = (root / '../../Book5_DSA/Book5_DSA_Part05.md').resolve().read_text()
out = []
for n in range(1, 11):
    m = re.search(r'^(### Q%d .*)\n(\*\*Asked at:\*\*.*)\n' % n, part, re.M)
    head, asked = m.group(1), m.group(2)
    code = (root / 'code' / f'q{n:02d}.py').read_text().rstrip('\n')
    r = subprocess.run([sys.executable, '-I', str(root / 'code' / f'q{n:02d}.py')],
                       capture_output=True, text=True, cwd='/tmp')
    assert r.returncode == 0, (n, r.stderr)
    body = (root / 'body' / f'q{n:02d}.md').read_text().rstrip('\n')
    body = body.replace('@@CODE@@', '```python\n' + code + '\n```')
    body = body.replace('@@OUTPUT@@', '```\n' + r.stdout.rstrip('\n') + '\n```')
    out.append(f'{head}\n{asked}\n\n{body}\n')
(root / 'answers.md').write_text('\n'.join(out))
print('built', len(out))
