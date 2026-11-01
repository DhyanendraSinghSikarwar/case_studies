import re, subprocess, os, glob
H = os.path.dirname(os.path.abspath(__file__))
part = open(os.path.join(H, '../../Book6_Scenarios/Book6_Scenarios_Part08.md'), encoding='utf-8').read().split('\n')
head = {}
for i, l in enumerate(part):
    m = re.match(r'### Q(\d+) ', l)
    if m:
        assert part[i+1].startswith('**Asked at:**')
        head[int(m.group(1))] = l + '\n' + part[i+1]
out = []
for n in range(1, 10):
    md, py = f'{H}/q{n:02d}.md', f'{H}/q{n:02d}.py'
    if not os.path.exists(md): continue
    body = open(md, encoding='utf-8').read().strip('\n')
    code = open(py, encoding='utf-8').read().rstrip('\n')
    r = subprocess.run(['python3', '-I', py], capture_output=True, text=True, cwd=H, timeout=300)
    assert r.returncode == 0, (n, r.stderr)
    body = body.replace('@@CODE@@', '```python\n' + code + '\n```').replace('@@OUT@@', '```text\n' + r.stdout.rstrip('\n') + '\n```')
    out.append(head[n] + '\n' + body + '\n')
open(f'{H}/answers.md', 'w', encoding='utf-8').write('\n'.join(out))
for d in glob.glob(H + '/__pycache__'): subprocess.run(['rm', '-rf', d])
print('built', len(out))
