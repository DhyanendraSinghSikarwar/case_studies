import re,sys
sys.path.insert(0,'body'); from bodies import B
t=open('/home/user/case_studies/interviews/Book4_MLOps/Book4_MLOps_Part12.md').read()
parts={int(re.match(r'### Q(\d+)',p).group(1)):p for p in re.split(r'\n(?=### Q)',t)[1:]}
out=[]
for n in range(34,46):
    p=parts[n].split('\n')
    head,asked=p[0],p[1]; assert asked.startswith('**Asked at:**')
    body=B[n].replace('{{CODE}}',open(f'code/q{n}.py').read().rstrip('\n')+'\n').replace('{{OUT}}',open(f'out/q{n}.txt').read().rstrip('\n')+'\n')
    out.append(head+'\n'+asked+'\n'+body)
open('answers.md','w').write('\n'.join(out))
