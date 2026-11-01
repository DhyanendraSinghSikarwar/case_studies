import sys,re
n=sys.argv[1]
src=open('/home/user/case_studies/interviews/Book2_GenAI/Book2_GenAI_Part03.md',encoding='utf8').read().split('\n')
i=[k for k,l in enumerate(src) if l.startswith(f'### Q{n} ')][0]
head=src[i]; asked=src[i+1]; assert asked.startswith('**Asked at:**')
body=open(f'/home/user/case_studies/interviews/scratch/B2P03_Q34-44/body/Q{n}.md',encoding='utf8').read().strip('\n')
assert 'ANSWER_PENDING' not in body
out='/home/user/case_studies/interviews/scratch/B2P03_Q34-44/answers.md'
try: cur=open(out,encoding='utf8').read()
except FileNotFoundError: cur=''
assert f'### Q{n} ' not in cur
with open(out,'a',encoding='utf8') as f:
    f.write(('\n' if cur else '')+head+'\n'+asked+'\n'+body+'\n')
