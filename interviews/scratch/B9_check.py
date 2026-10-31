import re,sys
kind=sys.argv[1]; f=sys.argv[2]
t=open(f,encoding='utf-8').read()
H={'q':r'### Q\d+ ','s':r'### S\d+ ','p':r'### P\d+ '}[kind]
bl=re.split(r'(?m)^(?='+H+')',t)[1:]
LABS={'q':['Say this first','Structure','Strong sample answer (spoken)','Weak version (and why it fails)','What the interviewer scores','Make it yours','Follow-ups','Common mistakes'],
 's':['Situation','Weak response','Strong response','Why it works','What the interviewer scores','Say it like this','If they push back','Common mistakes'],
 'p':['What good looks like','Self-assessment','Daily and weekly practice','30-day plan','Resources','How to show it in interviews','Common traps','Measures of progress']}[kind]
bad=[];long_=[]
for b in bl:
    n=b.split('\n')[0][:45]
    pos=[b.find('\n**'+l+':**') for l in LABS]
    if -1 in pos or pos!=sorted(pos): bad.append((n,'labels',[LABS[i] for i,p in enumerate(pos) if p==-1]))
    if b.count('```')%2: bad.append((n,'fence'))
    if kind=='q':
        sp=b.find('\n**Script (copy and adapt):**')
        if sp!=-1 and not (b.find('\n**Make it yours:**')<sp<b.find('\n**Follow-ups:**')): bad.append((n,'script position'))
        s=b.split('**Strong sample answer (spoken):**')[1].split('\n**')[0] if '**Strong sample answer (spoken):**' in b else ''
        w=len(re.findall(r"[A-Za-z']+",s))
        if not 50<=w<=260: long_.append((n,w))
    if kind=='s':
        s=b.split('**Say it like this:**')[1].split('\n**')[0] if '**Say it like this:**' in b else ''
        w=len(re.findall(r"[A-Za-z']+",s))
        if not 25<=w<=260: long_.append((n,w))
pay=re.compile(r"(?i)\bLPA\b|\blakhs?\b|\bcrores?\b|\bCTC\b|\bsalary\b|\bsalaries\b|compensation|base pay|per annum|[$€₹£]\s?\d|\b(?:USD|EUR|INR|GBP|SGD|AED|CHF|CAD|SEK)\s?\d|\d\s?(?:USD|EUR|INR|GBP|SGD|AED|CHF|CAD|SEK)\b|(?:raise|hike|increase|bump|counter(?:-| )?offer)[^.\n]{0,25}\d")
sal=[(m.group(0),t[max(0,m.start()-40):m.end()+40].replace('\n',' ')) for m in pay.finditer(t)]
leg=re.compile(r"(?i)\billegal\b|\bunlawful\b|\blegally\b|\bby law\b|law requires|\bright to\b")
lz=[t[max(0,m.start()-40):m.end()+40].replace('\n',' ') for m in leg.finditer(t)]
print(len(bl),'items; bad:',bad)
print('word-count outliers (sample answer or script):',long_)
print('pay-pattern hits:',len(sal),sal[:5])
print('legal-word flags (manual review):',len(lz),lz[:6])
print('pending markers:',t.count('ANSWER_PENDING'))
