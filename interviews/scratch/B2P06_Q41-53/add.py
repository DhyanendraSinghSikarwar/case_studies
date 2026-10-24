import sys,re
n=sys.argv[1]
src=open('/home/user/case_studies/interviews/Book2_GenAI/Book2_GenAI_Part06.md').read().split('\n')
i=[k for k,l in enumerate(src) if l.startswith(f'### Q{n} ')][0]
head=src[i]+'\n'+src[i+1]+'\n'
body=open(f'w/q{n}.md').read().strip('\n')
code=open(f'w/q{n}.py').read().strip('\n')
body=body.replace('{{CODE}}',code)
assert 'ANSWER_PENDING' not in body and '**Example:**' in body
out=open('answers.md','a'); 
import os
pre='\n' if os.path.getsize('answers.md')>0 else ''
out.write(pre+head+body+'\n')
