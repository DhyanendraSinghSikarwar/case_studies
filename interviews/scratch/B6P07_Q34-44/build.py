import os, re, subprocess, glob
os.chdir('/home/user/case_studies/interviews/scratch/B6P07_Q34-44')
part = open('../../Book6_Scenarios/Book6_Scenarios_Part07.md', encoding='utf-8').read()
blocks = {int(re.match(r'### Q(\d+)', b).group(1)): b for b in re.split(r'(?m)^(?=### Q\d+ )', part)[1:]}
out = ''
done = []
for n in range(34, 45):
    tp = f'q{n}.md'; cp = f'q{n}.py'
    if not (os.path.exists(tp) and os.path.exists(cp)):
        continue
    lines = blocks[n].split('\n')
    head = lines[0] + '\n' + lines[1] + '\n'
    assert lines[1].startswith('**Asked at:**')
    code = open(cp).read().rstrip('\n')
    r = subprocess.run(['python3', '-I', cp], capture_output=True, text=True, timeout=120)
    assert r.returncode == 0, (n, r.stderr)
    body = open(tp).read()
    assert '{{CODE}}' in body and '{{OUTPUT}}' in body
    body = body.replace('{{CODE}}', '```python\n' + code + '\n```').replace('{{OUTPUT}}', '```text\n' + r.stdout.rstrip('\n') + '\n```')
    out += head + body.strip('\n') + '\n\n'
    done.append(n)
open('answers.md', 'w', encoding='utf-8').write(out.rstrip('\n') + '\n')
for p in glob.glob('__pycache__'): pass
print('built', done)
