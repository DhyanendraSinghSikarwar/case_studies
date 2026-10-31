import re,subprocess,tempfile,sys,os
f=sys.argv[1]
t=open(f,encoding='utf-8').read()
bl=re.split(r'(?m)^(?=### Q\d+ )',t)[1:]
labs=['Say this first','Clarifying questions','Approach','Metrics','Risks','What the interviewer scores','Example','Code','Output (my run)','Follow-ups','Common mistakes']
bad=[]
for b in bl:
    n=re.match(r'### Q(\d+)',b).group(1)
    pos=[b.find('\n**'+l) for l in labs]
    if -1 in pos or pos!=sorted(pos): bad.append((n,pos))
    if b.count('```')%2: bad.append((n,'fence'))
print(len(bl),'blocks; bad:',bad,'pending',t.count('ANSWER_PENDING'))
st=[b.split('\n')[0].count('⭐') for b in bl]; print('stars sorted',st==sorted(st,reverse=True),[st.count(i) for i in (3,2,1)])
fail=[];n=0
for b in bl:
    q=re.match(r'### Q(\d+)',b).group(1)
    blocks=re.findall(r'```python\n(.*?)```',b,re.S)
    if len(blocks)>1: fail.append((q,'python blocks',len(blocks)))
    for c in blocks:
        n+=1;d=tempfile.mkdtemp();open(d+'/x.py','w').write(c)
        try:
            r=subprocess.run(['python3','-I','x.py'],cwd=d,capture_output=True,text=True,timeout=120,stdin=subprocess.DEVNULL)
            if r.returncode: fail.append((q,(r.stderr.strip().splitlines() or ['rc'])[-1][:90]))
        except Exception as e: fail.append((q,'TO'))
print(n,'python blocks run; failures:',fail)
