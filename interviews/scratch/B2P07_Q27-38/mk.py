import sys
# usage: mk.py block.txt -> appends the block, replacing {{CODE:file}} and {{OUT:file}} markers
import re
d='/tmp/claude-0/s/'
t=open(sys.argv[1]).read()
t=re.sub(r"\{\{CODE:(\S+)\}\}",lambda m:open(d+m.group(1)).read().rstrip(),t)
t=re.sub(r"\{\{OUT:(\S+)\}\}",lambda m:open(d+m.group(1)).read().rstrip(),t)
p='/home/user/case_studies/interviews/scratch/B2P07_Q27-38/answers.md'
import os
pre='\n\n' if os.path.exists(p) and os.path.getsize(p) else ''
open(p,'a').write(pre+t.strip()+'\n')
