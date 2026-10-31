import re,sys
f=sys.argv[1]
t=open(f,encoding='utf-8').read()
bl=re.split(r'(?m)^(?=### R\d+ )',t)[1:]
labs=['Evidence level','Market snapshot for data and ML roles (as reported)','Hiring process norms (as reported)','Round formats','Culture and communication style in interviews','CV and application format','Language and location notes','Work authorisation: where to check',"Process differences for candidates coming from India's process",'How to use Books 1-7 for this market','Preparation checklist (2 weeks)','Common mistakes','Recent changes and AI-era notes','Sources','Confidence and what to verify']
bad=[]
for b in bl:
    n=b.split('\n')[0][:40]
    pos=[b.find('\n**'+l+':**') for l in labs]
    if -1 in pos or pos!=sorted(pos): bad.append((n,'labels',[labs[i] for i,p in enumerate(pos) if p==-1]))
    if b.count('```')%2: bad.append((n,'fence'))
    if '**Sources:**' not in b: continue
    body=b.split('**Sources:**')[0]
    src=b.split('**Sources:**')[1].split('**Confidence')[0]
    if len(re.findall(r'\[(?:S\d+|G|U)\]',body))<10: bad.append((n,'few evidence tags'))
    urls=re.findall(r'https?://[^\s)>\]]+',src)
    if len(urls)<3: bad.append((n,'few source urls',len(urls)))
    have=set(re.findall(r'(?m)^\s*(?:[-*]|\d+\.)?\s*S(\d+)\s*[.:]',src))
    used=set(re.findall(r'S(\d+)',' '.join(re.findall(r'\[[^\]]*\]',body))))
    if used-have: bad.append((n,'tags without a source',sorted(used-have)))
    if have-used: bad.append((n,'sources never cited',sorted(have-used)))
pat=re.compile(r'(?i)\bLPA\b|\blakhs?\b|\bcrores?\b|\bCTC\b|\bsalary\b|\bsalaries\b|compensation|base pay|per annum|[$€₹£]\s?\d|\b(?:USD|EUR|INR|GBP|SGD|AED|CHF|CAD|SEK)\s?\d|\d\s?(?:USD|EUR|INR|GBP|SGD|AED|CHF|CAD|SEK)\b')
sal=[(m.group(0),t[max(0,m.start()-40):m.end()+40].replace('\n',' ')) for m in pat.finditer(t)]
vis=re.compile(r'(?i)(?:visa|permit|sponsorship|work authori[sz]ation|blue card|immigration)[^.\n]{0,60}\d|\d[^.\n]{0,40}(?:visa|permit|sponsorship)')
vz=[t[max(0,m.start()-30):m.end()+30].replace('\n',' ') for m in vis.finditer(t)]
print(len(bl),'profiles; bad:',bad)
print('pay-pattern hits:',len(sal),sal[:5])
print('visa-digit flags (manual review):',len(vz),vz[:6])
print('pending markers:',t.count('ANSWER_PENDING'))
