import re,subprocess,sys
p=sys.argv[1]
t=open(p,encoding='utf-8').read()
qs=re.split(r'(?m)^(?=### Q\d+ )',t)[1:]
nums=[int(re.match(r'### Q(\d+)',q).group(1)) for q in qs]
print('questions',len(qs),'continuous',nums==list(range(1,len(qs)+1)),'pending',t.count('ANSWER_PENDING'))
stars=[len(re.match(r'### Q\d+ (⭐+)',q).group(1)) for q in qs]
print('star order ok',stars==sorted(stars,reverse=True),[stars.count(s) for s in (3,2,1)])
bad=[]
for q,n in zip(qs,nums):
    for k in ['Say this first','Schema and sample data','SQL answer','pandas answer','Example','Output (my run)','Edge cases','Then explain','Follow-ups','Common mistakes']:
        if k not in q: bad.append((n,'missing',k))
    prog=[b for b in re.findall(r'(?ms)^```python\n(.*?)^```',q) if 'sqlite3' in b]
    if len(prog)!=1: bad.append((n,'programs',len(prog))); continue
    r=subprocess.run(['python3','-I','-c',prog[0]],capture_output=True,text=True,timeout=180)
    if r.returncode: bad.append((n,'rc',r.stderr[-150:]))
print('FAILS',bad)
