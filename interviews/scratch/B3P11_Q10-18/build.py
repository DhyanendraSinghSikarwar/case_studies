import re
part = open('/home/user/case_studies/interviews/Book3_SQL/Book3_SQL_Part11.md').read().split('\n')
out = []
for n in range(10, 19):
    for i, l in enumerate(part):
        if re.match(r'### Q%d ' % n, l):
            head, asked = l, part[i + 1]
            assert asked.startswith('**Asked at:**')
            break
    prose = open('prose/Q%d.md' % n).read().rstrip('\n')
    code = open('code/Q%d.py' % n).read().rstrip('\n')
    o = open('code/Q%d.out' % n).read().rstrip('\n')
    assert '```' not in code and '```' not in o
    prose = prose.replace('{{CODE}}', '```python\n' + code + '\n```').replace('{{OUT}}', '```text\n' + o + '\n```')
    out.append(head + '\n' + asked + '\n' + prose + '\n')
open('answers.md', 'w').write('\n'.join(out))
