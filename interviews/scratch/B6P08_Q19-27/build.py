import os, re, subprocess, sys, tempfile
os.chdir('/home/user/case_studies/interviews/scratch/B6P08_Q19-27')
PART = '/home/user/case_studies/interviews/Book6_Scenarios/Book6_Scenarios_Part08.md'
part = open(PART, encoding='utf-8').read()
out = []
done = []
for n in range(19, 28):
    tf, cf = f'q{n}.md', f'q{n}.py'
    if not (os.path.exists(tf) and os.path.exists(cf)):
        continue
    m = re.search(rf'(?m)^(### Q{n} .*)\n(\*\*Asked at:\*\*.*)\n', part)
    code = open(cf, encoding='utf-8').read()
    r = subprocess.run(['python3', '-I', os.path.abspath(cf)], capture_output=True, text=True, timeout=300, stdin=subprocess.DEVNULL)
    assert r.returncode == 0, (n, r.stderr[-800:])
    text = open(tf, encoding='utf-8').read()
    assert '@@CODE@@' in text and '@@OUTPUT@@' in text
    text = text.replace('@@CODE@@', '```python\n' + code.rstrip() + '\n```').replace('@@OUTPUT@@', '```text\n' + r.stdout.rstrip() + '\n```')
    out.append(m.group(1) + '\n' + m.group(2) + '\n' + text.strip() + '\n')
    done.append(n)
open('answers.md', 'w', encoding='utf-8').write('\n'.join(out))
open('progress.txt', 'w').write('complete: ' + ','.join(map(str, done)) + '\n')
print('built', done)
