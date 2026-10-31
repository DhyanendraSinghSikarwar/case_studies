import re,subprocess,sys,os
n=int(sys.argv[1]); base=os.path.dirname(os.path.abspath(__file__))
t=open(base+'/../../Book2_GenAI/Book2_GenAI_Part08.md').read()
m=re.search(r'^(### Q%d .*)\n(\*\*Asked at:\*\*.*)\n'%n,t,re.M)
body=open(f'{base}/body{n}.md').read().strip('\n')
if '@@CODE@@' in body:
    code=open(f'{base}/code/q{n}.py').read().rstrip('\n')
    out=subprocess.run(['python3','-I',f'{base}/code/q{n}.py'],capture_output=True,text=True,timeout=120)
    assert out.returncode==0,out.stderr
    body=body.replace('@@CODE@@','```python\n'+code+'\n```\nOutput (my run):\n```\n'+out.stdout.rstrip('\n')+'\n```')
blk=m.group(1)+'\n'+m.group(2)+'\n'+body+'\n'
f=base+'/answers.md'
cur=open(f).read() if os.path.exists(f) else ''
parts=[p for p in re.split(r'\n\n(?=### Q)',cur.strip('\n')) if p.strip()]
parts=[p for p in parts if not p.startswith('### Q%d '%n)]+[blk.strip('\n')]
parts.sort(key=lambda p:int(re.match(r'### Q(\d+)',p).group(1)))
open(f,'w').write('\n\n'.join(parts)+'\n')
print('ok',n)
