import sys, re
n = sys.argv[1]
src = open('../../Book2_GenAI/Book2_GenAI_Part07.md').read().split('\n')
i = next(k for k, l in enumerate(src) if l.startswith(f'### Q{n} '))
head, asked = src[i], src[i + 1]
body = open(f'body/q{n}.md').read().strip('\n')
code = open(f'code/q{n}.py').read().rstrip('\n')
body = body.replace('@@CODE@@', '```python\n' + code + '\n```')
assert 'ANSWER_PENDING' not in body and '**Example:**' in body
blk = f'{head}\n{asked}\n{body}\n'
try: old = open('answers.md').read()
except FileNotFoundError: old = ''
if re.search(rf'^### Q{n} ', old, re.M): sys.exit('already present')
open('answers.md', 'a').write(('\n' if old else '') + blk)
