import json, re, os, sys
sys.path.insert(0, '.')
from bodies1 import B as B1
from bodies2 import B as B2
B = {**B1, **B2}
heads = {int(k): v for k, v in json.load(open('/tmp/claude-0/b5p05_q31_40/heads.json')).items()}
base = 'code/'
def sub(m):
    kind, lang, files = m.group(1), m.group(2), m.group(3)
    if kind == 'out':
        return '```text\n' + open(base + files).read().rstrip('\n') + '\n```'
    parts = []
    for f in files.split(','):
        txt = open(base + f).read().rstrip('\n')
        if len(files.split(',')) > 1:
            cm = '#' 
            txt = f'{cm} ===== {f} =====\n' + txt
        parts.append(txt)
    return f'```{lang}\n' + '\n\n'.join(parts) + '\n```'
out = []
for q in range(31, 41):
    body = re.sub(r'@@(code):(\w+):([^@]+)@@', sub, B[q])
    body = re.sub(r'@@(out):()([^@]+)@@', sub, body)
    out.append(heads[q][0] + '\n' + heads[q][1] + '\n' + body.strip() + '\n')
open('answers.md', 'w').write('\n'.join(out))
print(len(open('answers.md').read()))
