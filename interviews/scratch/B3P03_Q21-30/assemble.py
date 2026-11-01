import re, subprocess, sys, os
D = os.path.dirname(os.path.abspath(__file__))
part = open('/home/user/case_studies/interviews/Book3_SQL/Book3_SQL_Part03.md', encoding='utf-8').read().split('\n')
def head(n):
    for i, l in enumerate(part):
        if l.startswith(f'### Q{n} '):
            assert part[i+1].startswith('**Asked at:**')
            return l + '\n' + part[i+1]
def var(code, name):
    m = re.search(r'(?ms)^' + name + r' = """(.*?)"""', code)
    assert m, name
    return m.group(1).strip('\n')
def pd_block(code):
    m = re.search(r'(?ms)^# pd:main\n(.*?)^# pd:end', code)
    assert m
    return m.group(1).rstrip('\n')
out = []
for n in range(21, 31):
    code = open(f'{D}/q{n}.py', encoding='utf-8').read()
    r = subprocess.run(['python3', '-I', f'{D}/q{n}.py'], capture_output=True, text=True)
    if r.returncode:
        print('Q', n, 'FAILED', r.stderr[-1500:]); sys.exit(1)
    prose = open(f'{D}/q{n}.md', encoding='utf-8').read()
    prose = re.sub(r'@@VAR:(\w+)@@', lambda m: var(code, m.group(1)), prose)
    prose = prose.replace('@@PD@@', pd_block(code))
    prose = prose.replace('@@CODE@@', code.rstrip('\n')).replace('@@OUT@@', r.stdout.rstrip('\n'))
    out.append(head(n) + '\n' + prose.strip('\n') + '\n')
open(f'{D}/answers.md', 'w', encoding='utf-8').write('\n'.join(out))
print('ok')
