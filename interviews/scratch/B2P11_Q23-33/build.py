import re, subprocess, sys
P11 = open('/home/user/case_studies/interviews/Book2_GenAI/Book2_GenAI_Part11.md', encoding='utf-8').read().split('\n')
def head(n):
    for i, l in enumerate(P11):
        if l.startswith(f'### Q{n} '):
            assert P11[i+1].startswith('**Asked at:**'); return l + '\n' + P11[i+1]
def run(n):
    r = subprocess.run(['python3', '-I', f'code/q{n}.py'], capture_output=True, text=True, check=True); return r.stdout.rstrip('\n')
T = {}
exec(open('texts.py', encoding='utf-8').read())
out = []
for n in range(23, 34):
    t = T[n]; code = open(f'code/q{n}.py', encoding='utf-8').read().rstrip('\n')
    out.append(head(n) + '\n' + t['say'].strip() + '\n\n**Then explain:**\n' + t['explain'].strip() + '\n\n**Example:** ' + t['example'].strip() +
      '\n\n**Code:** ' + t['codenote'].strip() + '\n```python\n' + code + '\n```\n**Output (my run):**\n```\n' + run(n) + '\n```\n\n**Follow-ups:**\n' + t['fu'].strip() +
      '\n\n**Common mistakes:** ' + t['mist'].strip() + '\n')
open('answers.md', 'w', encoding='utf-8').write('\n'.join(out))
