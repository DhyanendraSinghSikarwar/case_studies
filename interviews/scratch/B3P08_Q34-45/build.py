import re, subprocess, sys, os
here = os.path.dirname(os.path.abspath(__file__))
part = open('/home/user/case_studies/interviews/Book3_SQL/Book3_SQL_Part08.md', encoding='utf-8').read().split('\n')
def head(n):
    for i, l in enumerate(part):
        if l.startswith(f'### Q{n} '):
            return l + '\n' + part[i+1]
def grab(code, name):
    m = re.search(name + r' = """\n?(.*?)"""', code, re.S)
    return m.group(1).strip('\n')
def pd_block(code):
    m = re.search(r'# pd:main\n(.*?)# pd:end', code, re.S)
    return m.group(1).rstrip('\n')
out = []
fails = 0
for n in range(34, 46):
    code = open(f'{here}/q{n}.py', encoding='utf-8').read()
    r = subprocess.run(['python3', '-I', f'{here}/q{n}.py'], capture_output=True, text=True, timeout=300, cwd='/tmp')
    if r.returncode:
        print('Q', n, 'FAILED', r.stderr[-1500:]); fails += 1
        outp = 'FAILED'
    else:
        outp = r.stdout.rstrip('\n')
    open(f'{here}/q{n}.out', 'w').write(outp)
    md = open(f'{here}/q{n}.md', encoding='utf-8').read()
    md = md.replace('@@HEAD@@', head(n))
    md = md.replace('@@SCHEMA@@', '```sql\n' + grab(code, 'SCHEMA') + '\n```')
    md = md.replace('@@SQL@@', '```sql\n' + grab(code, 'SQL_MAIN') + '\n```')
    md = md.replace('@@PD@@', '```py\n' + pd_block(code) + '\n```')
    md = md.replace('@@CODE@@', '```python\n' + code.rstrip('\n') + '\n```')
    md = md.replace('@@OUT@@', '```text\n' + outp + '\n```')
    out.append(md.strip('\n'))
open(f'{here}/answers.md', 'w', encoding='utf-8').write('\n\n'.join(out) + '\n')
print('built, fails', fails)
