import re
part = open('/home/user/case_studies/interviews/Book4_MLOps/Book4_MLOps_Part11.md').read()
bodies = open('/home/user/case_studies/interviews/scratch/B4P11_Q10-18/bodies.md').read()
code = '/home/user/case_studies/interviews/scratch/B4P11_Q10-18/code/'
def head(n):
    m = re.search(r'^(### Q%d .*)\n(\*\*Asked at:\*\*.*)' % n, part, re.M)
    return m.group(1) + '\n' + m.group(2) + '\n'
def sub(m):
    kind = m.group(1)
    if kind == 'CODE':
        lang = {'py': 'python', 'yaml': 'yaml'}[m.group(3)]
        return '```%s\n%s```' % (lang, open(code + m.group(2)).read().rstrip('\n') + '\n')
    return '```text\n%s```' % (open(code + m.group(2)).read().rstrip('\n') + '\n')
out = ['# Book 4 Part 11 answers Q10-Q18\n']
for chunk in re.split(r'^@@Q(\d+)@@\n', bodies, flags=re.M)[1:]:
    pass
parts = re.split(r'^@@Q(\d+)@@\n', bodies, flags=re.M)
for i in range(1, len(parts), 2):
    n = int(parts[i]); body = parts[i+1]
    body = re.sub(r'@@(CODE) (\S+) (\w+)@@', sub, body)
    body = re.sub(r'@@(OUT) (\S+)@@', sub, body)
    out.append(head(n) + body.rstrip() + '\n')
open('/home/user/case_studies/interviews/scratch/B4P11_Q10-18/answers.md', 'w').write('\n'.join(out))
