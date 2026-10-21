import re, subprocess, sys
txt = open('../../Book1_DS_ML/Book1_DS_ML_Part13.md', encoding='utf-8').read()
parts = re.split(r'(?m)^### Q(\d+) ', txt)
# parts: [pre, num, body, num, body...]
for i in range(1, len(parts), 2):
    n = int(parts[i])
    if n > 31: break
    for j, m in enumerate(re.findall(r'```python\n(.*?)```', parts[i+1], re.S)):
        open(f'snip_q{n:02d}_{j}.py', 'w', encoding='utf-8').write(m)
