# Assembles answers.md for Book 5 Part 14 Q11-Q20 and re-runs every code file with python3 -I (fails loudly on any error).
import os, re, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__))
part = os.path.join(here, '..', '..', 'Book5_DSA', 'Book5_DSA_Part14.md')
lines = open(part, encoding='utf-8').read().split('\n')
out = ['# Book 5 Part 14: answers Q11-Q20 (Wave B)\n']
for q in range(11, 21):
    i = next(k for k, l in enumerate(lines) if l.startswith(f'### Q{q} '))
    heading = lines[i]; asked = lines[i + 1]; assert asked.startswith('**Asked at:**')
    code_path = os.path.join(here, 'code', f'q{q}.py')
    r = subprocess.run([sys.executable, '-I', code_path], capture_output=True, text=True, cwd=here, timeout=300)
    assert r.returncode == 0, (q, r.stderr)
    code = open(code_path).read().rstrip('\n')
    pre = open(os.path.join(here, 'prose', f'q{q}_pre.md')).read().strip('\n')
    post = open(os.path.join(here, 'prose', f'q{q}_post.md')).read().strip('\n')
    out += [heading, asked, '', pre, '', '**Code:**', '```python', code, '```', '', '**Output (my run):**', '```', r.stdout.rstrip('\n'), '```', '', post, '', '---', '']
    print('ran q%d ok' % q)
text = '\n'.join(out)
open(os.path.join(here, 'answers.md'), 'w', encoding='utf-8').write(text)
for q in range(11, 21):
    for lab in ['**Pattern:**', '**Say this first (1 line):**', '**Brute force:**', '**Optimal:**', '**Complexity:**', '**Dry run:**', '**Code:**', '**Output (my run):**', '**Edge cases:**', '**Follow-ups:**', '**Common mistakes:**']:
        pass
for lab in ['**Pattern:**', '**Say this first (1 line):**', '**Brute force:**', '**Optimal:**', '**Complexity:**', '**Dry run:**', '**Code:**', '**Output (my run):**', '**Edge cases:**', '**Follow-ups:**', '**Common mistakes:**']:
    assert text.count(lab) == 10, (lab, text.count(lab))
print('answers.md written; all labels x10')
