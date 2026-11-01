import re
base='/home/user/case_studies/interviews/'
t=open(base+'Book4_MLOps/Book4_MLOps_Part08.md').read()
out=[]
def fill(body):
    def code(m):
        return "\n\n".join(("# ---- file: %s ----\n"%f if '|' in m.group(1) else "")+open(base+'scratch/B4P08_Q13-23/code/'+f).read().rstrip() for f in m.group(1).split('|'))
    body=re.sub(r'\{\{code:([^}]+)\}\}',code,body)
    body=re.sub(r'\{\{out:([^}]+)\}\}',lambda m:open(base+'scratch/B4P08_Q13-23/out/'+m.group(1)).read().rstrip(),body)
    return body
for n in range(13,24):
    m=re.search(r'^(### Q%d .*)\n(\*\*Asked at:\*\*.*)\n'%n,t,re.M)
    out.append(m.group(1)+"\n"+m.group(2)+"\n"+fill(open('/tmp/claude-0/b8_q13_23/bodies/q%d.md'%n).read()).rstrip()+"\n")
open(base+'scratch/B4P08_Q13-23/answers.md','w').write("\n".join(out))
